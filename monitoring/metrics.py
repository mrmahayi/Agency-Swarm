from prometheus_client import Counter, Gauge

# Define metrics
API_REQUESTS = Counter('api_requests_total', 'Total API requests', ['endpoint'])
AGENT_HEALTH = Gauge('agent_health', 'Agent health status', ['agent_name'])

def initialize_monitoring():
    """Initialize monitoring system"""
    # Reset health metrics
    for label in AGENT_HEALTH._metrics:
        AGENT_HEALTH.labels(**label[0]).set(0) 