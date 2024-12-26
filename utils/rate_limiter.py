import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    def is_allowed(self, endpoint):
        """Check if request is allowed under rate limit"""
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[endpoint] = [req for req in self.requests[endpoint] if req > minute_ago]
        
        # Check rate limit
        if len(self.requests[endpoint]) >= self.requests_per_minute:
            return False
        
        # Add new request
        self.requests[endpoint].append(now)
        return True

API_RATE_LIMITER = RateLimiter() 