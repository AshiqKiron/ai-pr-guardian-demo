/**
 * MIT License - Copyright 2024 AI-PR Guardian Demo
 * 
 * Clean JavaScript code example
 */

// Use environment variables for configuration
const apiKey = process.env.API_KEY;

async function fetchData(endpoint) {
    if (!apiKey) {
        throw new Error('API key not configured');
    }
    
    try {
        const response = await fetch(`https://api.example.com/${endpoint}`, {
            headers: {
                'Authorization': `Bearer ${apiKey}`
            }
        });
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch data:', error.message);
        throw error;
    }
}

module.exports = { fetchData };
