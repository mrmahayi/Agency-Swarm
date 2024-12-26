import jwt
import datetime
import os

class SecurityManager:
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    
    def generate_token(self, agent_name):
        """Generate a JWT token for an agent"""
        payload = {
            'agent': agent_name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        """Verify a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['agent']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

security_manager = SecurityManager() 