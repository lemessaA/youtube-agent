# Groq API Setup Guide

This project uses Groq as the LLM provider for all AI agents. Follow this guide to set up your Groq API key.

## Getting a Groq API Key

1. **Visit Groq Console**: Go to [console.groq.com](https://console.groq.com)

2. **Create Account**: Sign up for a free Groq account or log in if you already have one

3. **Generate API Key**:
   - Navigate to the "API Keys" section in your dashboard
   - Click "Create API Key"
   - Give it a descriptive name (e.g., "YouTube Automation System")
   - Copy the generated API key (starts with `gsk_...`)

4. **Update Environment Variables**:
   ```bash
   # In your backend/.env file, replace:
   GROQ_API_KEY=your_groq_api_key_here
   # With your actual API key:
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```

## Available Models

The system is configured to use `llama3-8b-8192` by default, but you can change this by updating the `GROQ_MODEL` environment variable:

### Recommended Models:
- `llama3-8b-8192` - Fast and efficient (Default)
- `llama3-70b-8192` - More capable but slower
- `mixtral-8x7b-32768` - Good for complex tasks

## Configuration Options

In your `backend/.env` file, you can configure:

```env
# Groq Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192
GROQ_TEMPERATURE=0.7
GROQ_MAX_TOKENS=1024
```

### Parameters:
- `GROQ_API_KEY`: Your Groq API key (required)
- `GROQ_MODEL`: Which model to use (optional, defaults to llama3-8b-8192)
- `GROQ_TEMPERATURE`: Randomness in responses (0.0-1.0, defaults to 0.7)
- `GROQ_MAX_TOKENS`: Maximum tokens per response (defaults to 1024)

## Pricing

Groq offers competitive pricing with a generous free tier:
- Free tier includes significant monthly usage
- Pay-per-use pricing for additional usage
- Check [Groq's pricing page](https://console.groq.com/pricing) for current rates

## Troubleshooting

### Common Issues:

1. **"LLM not available" Error**:
   - Check that your GROQ_API_KEY is set correctly
   - Verify your API key is valid at console.groq.com

2. **Rate Limiting**:
   - Groq has rate limits - if you hit them, requests will be queued
   - Consider upgrading your plan for higher limits

3. **Model Not Found**:
   - Ensure the model name in GROQ_MODEL is correct
   - Check available models at console.groq.com

### Testing Your Setup:

```bash
# Test the API connection
curl -X POST "http://localhost:8000/test/groq" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, this is a test!"}'
```

## Migration from Ollama

This system has been migrated from Ollama to Groq for better performance and reliability. The main changes:

- No need to install local models
- No local server requirements
- Faster response times
- Better model quality
- Cloud-based reliability

All agent functionality remains the same - only the underlying LLM provider has changed.