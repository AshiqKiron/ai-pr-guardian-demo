"""
MIT License - Copyright 2024 AI-PR Guardian Demo

Secure application example following best practices
"""

import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_api_key():
    """Safely retrieve API key from environment variables"""
    return os.environ.get('API_KEY')


def process_safe_input(user_input):
    """Safely process user input without eval/exec"""
    try:
        data = json.loads(user_input)
        logger.info("Successfully parsed user input")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input: {e}")
        return {}


if __name__ == '__main__':
    logger.info("Secure application started")
