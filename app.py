"""
MIT License - Copyright 2024
Secure application example
"""
import os

def get_api_key():
    # Safe: Uses environment variables
    return os.environ.get('API_KEY')
