from flask import Flask, render_template, request, jsonify
from SentimentAnalysis import analyze_sentiment
import time
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = ''

class RateLimiter:
    def __init__(self, max_requests=10, window_minutes=1):
        self.max_requests = max_requests
        self.window_minutes = window_minutes
        self.requests = {}
    
    def is_allowed(self, ip):
        now = datetime.now()
        self.requests = {k: v for k, v in self.requests.items() 
                        if v[-1] > now - timedelta(minutes=self.window_minutes)}
        
        if ip not in self.requests:
            self.requests[ip] = []
        
        if len(self.requests[ip]) >= self.max_requests:
            return False
        
        self.requests[ip].append(now)
        return True

rate_limiter = RateLimiter()

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not rate_limiter.is_allowed(request.remote_addr):
            return jsonify({'error': 'Rate limit exceeded'}), 429
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
@rate_limit
def analyze():
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if len(text) > 5000:
            return jsonify({'error': 'Text exceeds maximum length'}), 400
        
        time.sleep(0.5)  # Simulate API latency
        
        analysis_result = analyze_sentiment(text)
        return jsonify(analysis_result)
    
    except Exception as e:
        app.logger.error(f"Error during analysis: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)