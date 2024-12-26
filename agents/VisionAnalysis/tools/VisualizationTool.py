from agency_swarm.tools import BaseTool
from pydantic import Field
from typing import Dict, List, Optional
import json
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import os

# Mock database manager for testing
class DatabaseManager:
    def _get_connection(self):
        class Connection:
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                pass
        return Connection()

# Initialize database manager
db_manager = DatabaseManager()

class VisualizationTool(BaseTool):
    """
    Tool for creating visualizations of task and communication analytics.
    Generates interactive charts and graphs using Plotly.
    """
    
    visualization_type: str = Field(
        ...,
        description="Type of visualization to generate: 'workload_distribution', 'task_completion_trends', 'communication_patterns', 'agent_performance', 'message_volume', 'response_times'"
    )
    
    output_format: str = Field(
        default="html",
        description="Output format for the visualization: 'html' or 'json'"
    )
    
    time_range: Optional[Dict] = Field(
        default=None,
        description="Time range for the visualization: {'start': ISO datetime, 'end': ISO datetime}"
    )
    
    agent: Optional[str] = Field(
        default=None,
        description="Agent name for agent-specific visualizations"
    )

    def run(self):
        """Generate visualizations based on analytics data."""
        try:
            if self.visualization_type == "workload_distribution":
                with db_manager._get_connection() as conn:
                    # Get workload data
                    query = """
                        SELECT 
                            agent,
                            COUNT(*) as total_tasks,
                            SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_tasks,
                            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_tasks,
                            AVG(priority) as avg_priority
                        FROM tasks
                        GROUP BY agent
                    """
                    df = pd.read_sql_query(query, conn)
                    
                    # Create stacked bar chart
                    fig = go.Figure(data=[
                        go.Bar(name='Pending', x=df['agent'], y=df['pending_tasks']),
                        go.Bar(name='Completed', x=df['agent'], y=df['completed_tasks'])
                    ])
                    
                    fig.update_layout(
                        title='Agent Workload Distribution',
                        barmode='stack',
                        xaxis_title='Agent',
                        yaxis_title='Number of Tasks'
                    )
                    
                    return self._save_visualization(fig)
            
            elif self.visualization_type == "task_completion_trends":
                with db_manager._get_connection() as conn:
                    # Get completion trend data
                    query = """
                        SELECT 
                            date(updated_at) as completion_date,
                            COUNT(*) as completed_count,
                            AVG(priority) as avg_priority
                        FROM tasks
                        WHERE status = 'completed'
                    """
                    if self.time_range:
                        query += " AND updated_at BETWEEN ? AND ?"
                        df = pd.read_sql_query(query, conn, params=[
                            self.time_range["start"],
                            self.time_range["end"]
                        ])
                    else:
                        df = pd.read_sql_query(query, conn)
                    
                    # Create line chart
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df['completion_date'],
                        y=df['completed_count'],
                        mode='lines+markers',
                        name='Completed Tasks'
                    ))
                    
                    fig.update_layout(
                        title='Task Completion Trends',
                        xaxis_title='Date',
                        yaxis_title='Number of Completed Tasks'
                    )
                    
                    return self._save_visualization(fig)
            
            elif self.visualization_type == "communication_patterns":
                with db_manager._get_connection() as conn:
                    # Get communication data
                    query = """
                        SELECT 
                            from_agent,
                            to_agent,
                            COUNT(*) as message_count
                        FROM messages
                        WHERE to_agent != 'all'
                        GROUP BY from_agent, to_agent
                    """
                    df = pd.read_sql_query(query, conn)
                    
                    # Create network graph
                    fig = go.Figure(data=[go.Sankey(
                        node=dict(
                            pad=15,
                            thickness=20,
                            line=dict(color="black", width=0.5),
                            label=list(set(df['from_agent'].unique().tolist() + df['to_agent'].unique().tolist()))
                        ),
                        link=dict(
                            source=df['from_agent'].map(lambda x: list(set(df['from_agent'].unique().tolist() + df['to_agent'].unique().tolist())).index(x)),
                            target=df['to_agent'].map(lambda x: list(set(df['from_agent'].unique().tolist() + df['to_agent'].unique().tolist())).index(x)),
                            value=df['message_count']
                        )
                    )])
                    
                    fig.update_layout(title='Communication Flow Between Agents')
                    
                    return self._save_visualization(fig)
            
            elif self.visualization_type == "agent_performance":
                if not self.agent:
                    return "Error: Agent name required for performance visualization"
                
                with db_manager._get_connection() as conn:
                    # Get performance data
                    query = """
                        SELECT 
                            date(updated_at) as date,
                            COUNT(*) as task_count,
                            AVG(CASE 
                                WHEN status = 'completed' 
                                THEN CAST(
                                    (JULIANDAY(updated_at) - JULIANDAY(created_at)) * 24 * 60 
                                    AS REAL
                                )
                                ELSE NULL 
                            END) as avg_completion_time
                        FROM tasks
                        WHERE agent = ?
                        GROUP BY date(updated_at)
                    """
                    df = pd.read_sql_query(query, conn, params=[self.agent])
                    
                    # Create dual-axis chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=df['date'],
                        y=df['task_count'],
                        name='Task Count'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df['avg_completion_time'],
                        name='Avg Completion Time (min)',
                        yaxis='y2'
                    ))
                    
                    fig.update_layout(
                        title=f'Performance Metrics for {self.agent}',
                        yaxis=dict(title='Number of Tasks'),
                        yaxis2=dict(title='Average Completion Time (minutes)', overlaying='y', side='right')
                    )
                    
                    return self._save_visualization(fig)
            
            elif self.visualization_type == "message_volume":
                with db_manager._get_connection() as conn:
                    # Get message volume data
                    query = """
                        SELECT 
                            date(timestamp) as date,
                            COUNT(*) as message_count,
                            COUNT(DISTINCT thread_id) as thread_count
                        FROM messages
                    """
                    if self.time_range:
                        query += " WHERE timestamp BETWEEN ? AND ?"
                        df = pd.read_sql_query(query, conn, params=[
                            self.time_range["start"],
                            self.time_range["end"]
                        ])
                    else:
                        df = pd.read_sql_query(query, conn)
                    
                    # Create area chart
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df['message_count'],
                        fill='tozeroy',
                        name='Total Messages'
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=df['date'],
                        y=df['thread_count'],
                        fill='tonexty',
                        name='Unique Threads'
                    ))
                    
                    fig.update_layout(
                        title='Message Volume Over Time',
                        xaxis_title='Date',
                        yaxis_title='Count'
                    )
                    
                    return self._save_visualization(fig)
            
            elif self.visualization_type == "response_times":
                with db_manager._get_connection() as conn:
                    # Get response time data
                    query = """
                        WITH responses AS (
                            SELECT 
                                m1.from_agent,
                                m1.to_agent,
                                CAST(
                                    (JULIANDAY(m2.timestamp) - JULIANDAY(m1.timestamp)) * 24 * 60 
                                    AS REAL
                                ) as response_time
                            FROM messages m1
                            JOIN messages m2 ON m2.reply_to_id = m1.id
                        )
                        SELECT 
                            from_agent,
                            to_agent,
                            AVG(response_time) as avg_response_time,
                            MIN(response_time) as min_response_time,
                            MAX(response_time) as max_response_time
                        FROM responses
                        GROUP BY from_agent, to_agent
                    """
                    df = pd.read_sql_query(query, conn)
                    
                    # Create box plot
                    fig = go.Figure()
                    
                    for agent in df['to_agent'].unique():
                        agent_data = df[df['to_agent'] == agent]
                        fig.add_trace(go.Box(
                            y=agent_data['avg_response_time'],
                            name=agent,
                            boxpoints='all'
                        ))
                    
                    fig.update_layout(
                        title='Response Time Distribution by Agent',
                        yaxis_title='Response Time (minutes)'
                    )
                    
                    return self._save_visualization(fig)
            
            else:
                return f"Error: Unknown visualization type {self.visualization_type}"
            
        except Exception as e:
            return f"Error generating visualization: {str(e)}"
    
    def _save_visualization(self, fig):
        """Save the visualization and return the appropriate output."""
        if self.output_format == "html":
            # Create visualizations directory if it doesn't exist
            os.makedirs("visualizations", exist_ok=True)
            
            # Generate unique filename
            filename = f"visualizations/{self.visualization_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            
            # Save the figure
            fig.write_html(filename)
            return f"Visualization saved to {filename}"
        else:
            return fig.to_json()

if __name__ == "__main__":
    # Test the visualization tool
    print("Testing VisualizationTool...")
    
    # Test workload distribution visualization
    print("\nTesting workload_distribution visualization...")
    tool = VisualizationTool(
        visualization_type="workload_distribution",
        output_format="html"
    )
    result = tool.run()
    print(result)
    
    # Test task completion trends visualization
    print("\nTesting task_completion_trends visualization...")
    tool = VisualizationTool(
        visualization_type="task_completion_trends",
        output_format="html",
        time_range={
            "start": (datetime.now().replace(day=1)).isoformat(),
            "end": datetime.now().isoformat()
        }
    )
    result = tool.run()
    print(result)
    
    # Test communication patterns visualization
    print("\nTesting communication_patterns visualization...")
    tool = VisualizationTool(
        visualization_type="communication_patterns",
        output_format="html"
    )
    result = tool.run()
    print(result) 