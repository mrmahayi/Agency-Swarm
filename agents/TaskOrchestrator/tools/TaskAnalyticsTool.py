from agency_swarm.tools import BaseTool
from pydantic import Field
import json
from datetime import datetime
from typing import Optional, Dict, List, Any
from tools.database_manager import DatabaseManager

# Initialize database manager
db_manager = DatabaseManager()

class TaskAnalyticsTool(BaseTool):
    """
    Tool for analyzing task execution patterns, performance metrics, and agent workload.
    Provides insights into task completion rates, execution times, and resource utilization.
    """
    
    operation: str = Field(
        ...,
        description="Operation to perform: 'task_metrics', 'agent_performance', 'workload_analysis', 'completion_trends', 'error_analysis'"
    )
    
    agent: Optional[str] = Field(
        default=None,
        description="Agent name for agent-specific analytics"
    )
    
    task_id: Optional[str] = Field(
        default=None,
        description="Task ID for task-specific analytics"
    )
    
    time_range: Optional[Dict] = Field(
        default=None,
        description="Time range for analysis: {'start': ISO datetime, 'end': ISO datetime}"
    )
    
    def run(self):
        """Execute task analytics operations."""
        try:
            if self.operation == "task_metrics":
                with db_manager._get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Get task execution metrics
                    query = """
                        SELECT 
                            status,
                            COUNT(*) as task_count,
                            AVG(CAST(
                                (JULIANDAY(completion_time) - JULIANDAY(creation_time)) * 24 * 60 
                                AS REAL
                            )) as avg_completion_time,
                            AVG(CASE 
                                WHEN priority = 'high' THEN 3
                                WHEN priority = 'normal' THEN 2
                                ELSE 1
                            END) as avg_priority
                        FROM tasks
                    """
                    params = []
                    
                    if self.time_range:
                        query += " WHERE creation_time BETWEEN ? AND ?"
                        params.extend([self.time_range["start"], self.time_range["end"]])
                    
                    query += " GROUP BY status"
                    
                    cursor.execute(query, params)
                    metrics = []
                    for row in cursor.fetchall():
                        metrics.append({
                            "status": row[0],
                            "task_count": row[1],
                            "avg_completion_time_minutes": row[2],
                            "avg_priority": row[3]
                        })
                    
                    return json.dumps(metrics, indent=2)
            
            elif self.operation == "agent_performance":
                if not self.agent:
                    return "Error: Agent name required for performance analysis"
                
                with db_manager._get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Get agent performance metrics
                    cursor.execute("""
                        SELECT 
                            COUNT(*) as total_tasks,
                            COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
                            COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_tasks,
                            AVG(CASE WHEN status = 'completed' THEN
                                CAST(
                                    (JULIANDAY(completion_time) - JULIANDAY(start_time)) * 24 * 60 
                                    AS REAL
                                )
                            END) as avg_execution_time,
                            COUNT(DISTINCT task_type) as task_type_count
                        FROM tasks
                        WHERE assigned_agent = ?
                    """, (self.agent,))
                    
                    row = cursor.fetchone()
                    if row:
                        performance = {
                            "total_tasks": row[0],
                            "completed_tasks": row[1],
                            "failed_tasks": row[2],
                            "completion_rate": (row[1] / row[0] * 100) if row[0] > 0 else 0,
                            "avg_execution_time_minutes": row[3],
                            "task_type_diversity": row[4]
                        }
                        return json.dumps(performance, indent=2)
                    return "No tasks found for agent"
            
            elif self.operation == "workload_analysis":
                with db_manager._get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Get workload distribution
                    query = """
                        SELECT 
                            assigned_agent,
                            COUNT(*) as active_tasks,
                            AVG(CASE 
                                WHEN priority = 'high' THEN 3
                                WHEN priority = 'normal' THEN 2
                                ELSE 1
                            END) as avg_priority,
                            COUNT(DISTINCT task_type) as task_types
                        FROM tasks
                        WHERE status IN ('pending', 'in_progress')
                    """
                    params = []
                    
                    if self.time_range:
                        query += " AND creation_time BETWEEN ? AND ?"
                        params.extend([self.time_range["start"], self.time_range["end"]])
                    
                    query += " GROUP BY assigned_agent"
                    
                    cursor.execute(query, params)
                    workload = []
                    for row in cursor.fetchall():
                        workload.append({
                            "agent": row[0],
                            "active_tasks": row[1],
                            "avg_priority": row[2],
                            "task_type_count": row[3]
                        })
                    
                    return json.dumps(workload, indent=2)
            
            elif self.operation == "completion_trends":
                with db_manager._get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Get task completion trends
                    query = """
                        SELECT 
                            date(completion_time) as completion_date,
                            COUNT(*) as completed_tasks,
                            AVG(CAST(
                                (JULIANDAY(completion_time) - JULIANDAY(start_time)) * 24 * 60 
                                AS REAL
                            )) as avg_execution_time
                        FROM tasks
                        WHERE status = 'completed'
                    """
                    params = []
                    
                    if self.time_range:
                        query += " AND completion_time BETWEEN ? AND ?"
                        params.extend([self.time_range["start"], self.time_range["end"]])
                    
                    query += " GROUP BY date(completion_time) ORDER BY completion_date"
                    
                    cursor.execute(query, params)
                    trends = []
                    for row in cursor.fetchall():
                        trends.append({
                            "date": row[0],
                            "completed_tasks": row[1],
                            "avg_execution_time_minutes": row[2]
                        })
                    
                    return json.dumps(trends, indent=2)
            
            elif self.operation == "error_analysis":
                with db_manager._get_connection() as conn:
                    cursor = conn.cursor()
                    
                    # Get error patterns
                    query = """
                        SELECT 
                            error_type,
                            COUNT(*) as error_count,
                            COUNT(DISTINCT assigned_agent) as affected_agents,
                            AVG(CASE 
                                WHEN priority = 'high' THEN 3
                                WHEN priority = 'normal' THEN 2
                                ELSE 1
                            END) as avg_priority
                        FROM tasks
                        WHERE status = 'failed'
                        AND error_type IS NOT NULL
                    """
                    params = []
                    
                    if self.time_range:
                        query += " AND creation_time BETWEEN ? AND ?"
                        params.extend([self.time_range["start"], self.time_range["end"]])
                    
                    query += " GROUP BY error_type ORDER BY error_count DESC"
                    
                    cursor.execute(query, params)
                    errors = []
                    for row in cursor.fetchall():
                        errors.append({
                            "error_type": row[0],
                            "error_count": row[1],
                            "affected_agents": row[2],
                            "avg_priority": row[3]
                        })
                    
                    return json.dumps(errors, indent=2)
            
            else:
                return f"Error: Unknown operation {self.operation}"
            
        except Exception as e:
            return f"Error during {self.operation} operation: {str(e)}"

if __name__ == "__main__":
    # Test the analytics tool
    print("Testing TaskAnalyticsTool...")
    
    # Test task metrics
    print("\nTesting task_metrics...")
    tool = TaskAnalyticsTool(
        operation="task_metrics",
        time_range={
            "start": (datetime.now().replace(day=1)).isoformat(),
            "end": datetime.now().isoformat()
        }
    )
    result = tool.run()
    print(result)
    
    # Test agent performance
    print("\nTesting agent_performance...")
    tool = TaskAnalyticsTool(
        operation="agent_performance",
        agent="test_agent"
    )
    result = tool.run()
    print(result)
    
    # Test workload analysis
    print("\nTesting workload_analysis...")
    tool = TaskAnalyticsTool(
        operation="workload_analysis"
    )
    result = tool.run()
    print(result) 