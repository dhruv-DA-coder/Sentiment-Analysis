import requests
from collections import Counter
import re
from openai import OpenAI
from langchain_xai import ChatXAI
import base64
import os

XAI_API_KEY ="xai-bdFATyf45nqQquAY1cgePLQcerzQYobci20181B1TFvWxOTbhpBUTefCYc6G1tCSTmR88mxVsthPWsos"
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)



def analyze_sentiment(text):
    """
    Analyze text sentiment using Grok API.
    
    Args:
        text (str): Input text
    Returns:
        dict: Sentiment analysis results and word frequencies
    """
    API_KEY = "xai-bdFATyf45nqQquAY1cgePLQcerzQYobci20181B1TFvWxOTbhpBUTefCYc6G1tCSTmR88mxVsthPWsos"
    API_URL = "https://api.x.ai/v1"

    try:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"text": text}
        )
        response.raise_for_status()
        
        # Get word frequencies for word cloud
        words = re.findall(r'\w+', text.lower())
        word_freq = Counter(words).most_common(50)
        
        result = response.json()
        result['word_frequencies'] = dict(word_freq)
        
        return result
        
    except Exception as e:
        raise Exception(f"API Error: {str(e)}")