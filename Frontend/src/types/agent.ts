export type AgentStatus = 'active' | 'idle' | 'busy' | 'error';

export interface Agent {
  id: string;
  name: string;
  type: 'TaskOrchestrator' | 'VisionAnalysis' | 'DesktopInteraction' | 'WebAutomation' | 'Research';
  status: AgentStatus;
  currentTask?: string;
  lastAction: string;
  tools: string[];
}