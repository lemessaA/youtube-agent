# AI YouTube Automation System

Complete AI-powered YouTube automation system that generates daily videos automatically and grows revenue.

## Features

### 🤖 AI Agents
- **Trend Research Agent**: Finds trending video ideas in your niche
- **Script Writing Agent**: Creates engaging 60-120 second scripts
- **Thumbnail Generator Agent**: Designs clickable thumbnails
- **Video Generation Agent**: Creates faceless videos with stock footage
- **Title & Description Generator**: Optimizes for SEO and CTR
- **Analytics Agent**: Analyzes performance and suggests improvements
- **Monetization Agent**: Suggests revenue strategies
- **Daily Automation Agent**: Orchestrates the entire workflow

### 🎯 Supported Niches
- AI Tools
- Startup Ideas  
- Tech Explainers
- Make Money Online
- Side Hustles

### 📊 Video Specifications
- **Length**: 60-120 seconds
- **Style**: Faceless automation
- **Upload Frequency**: Daily
- **Format**: Short educational content

## Tech Stack

- **Backend**: FastAPI
- **AI/ML**: LangChain, LangGraph, Ollama (Local Models)
- **Database**: Supabase
- **Video Processing**: MoviePy
- **Image Processing**: Pillow
- **Task Queue**: Celery with Redis
- **Scheduling**: APScheduler
- **Local AI**: Ollama with Llama, Qwen, CodeLlama models

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd youtube-agent
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Set up Supabase:
- Create a new Supabase project
- Run the SQL schema (see `database/schema.sql`)
- Update `.env` with your Supabase credentials

## 🚀 Quick Start

### Prerequisites
- **Ollama** installed and running (for local AI models)
- **Python 3.8+**
- **Supabase** account (for database)

### 1. Install Ollama (Local AI Models)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve

# Pull recommended model
ollama pull llama3.1:8b

# Or use our setup script
python scripts/setup_ollama.py
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add:
```bash
# Ollama Local Models
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TEMPERATURE=0.7

# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
```

### 4. Set Up Database
1. Go to [Supabase](https://supabase.com) and create a new project
2. Open the SQL editor in your Supabase project
3. Copy and paste the contents of `database/schema.sql`
4. Run the SQL to create all tables

### 5. Quick Setup Script
```bash
python scripts/setup_database.py
```

### 6. Test the System
```bash
python scripts/test_system.py
```

### 7. Start the Server
```bash
# Option 1: Run from project root
python -m app.main

# Option 2: Use the run script (recommended)
python run.py

# Option 3: Direct uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be running at `http://localhost:8000`

## Test the System

### Create a Test Channel
```bash
curl -X POST "http://localhost:8000/channels" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Tools Daily",
    "niche": "ai_tools",
    "description": "Daily AI tools and tips",
    "target_audience": "Developers and tech enthusiasts"
  }'
```

### Generate Your First Video
```bash
curl -X POST "http://localhost:8000/test/generation"
```

### Check Results
```bash
curl "http://localhost:8000/videos"
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Production Deployment

For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) for complete setup instructions.

### Quick Production Start
```bash
# Production server
python scripts/run_production.py

# Or with Docker
docker-compose up -d
```

The API will be available at `http://localhost:8000`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## Configuration

### Required Environment Variables

```bash
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# YouTube API (optional)
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_CHANNEL_ID=your_channel_id_here

# Redis for Celery (optional)
REDIS_URL=redis://localhost:6379/0

# Application Settings
DEBUG=True
SECRET_KEY=your_secret_key_here
```

## Usage

### Start the API Server

```bash
python -m app.main
```

The API will be available at `http://localhost:8000`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

#### Create a Channel
```bash
curl -X POST "http://localhost:8000/channels" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Tools Daily",
    "niche": "ai_tools",
    "description": "Daily AI tools and tips",
    "target_audience": "Developers and tech enthusiasts"
  }'
```

#### Generate a Video
```bash
curl -X POST "http://localhost:8000/videos/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "your-channel-id"
  }'
```

#### Research Trends
```bash
curl -X POST "http://localhost:8000/trends/research" \
  -H "Content-Type: application/json" \
  -d '{
    "niche": "ai_tools",
    "limit": 10
  }'
```

#### Get Analytics
```bash
curl -X POST "http://localhost:8000/analytics/video" \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "your-video-id"
  }'
```

## Daily Automation Workflow

The system runs this workflow automatically for each channel:

1. **Trend Research**: Find 10 trending topics in your niche
2. **Topic Selection**: Choose the topic with highest viral score
3. **Script Writing**: Create engaging 60-120 second script
4. **Thumbnail Generation**: Design 5 clickable thumbnail variations
5. **Video Creation**: Generate faceless video with stock footage
6. **Title & Description**: Optimize for SEO and engagement
7. **Analytics**: Predict performance and suggest improvements
8. **Monetization**: Suggest revenue strategies

## Database Schema

### Tables
- `channels`: Channel information and settings
- `video_ideas`: Trending topic research results
- `videos`: Generated videos and metadata
- `analytics`: Video performance data
- `monetization_strategies`: Revenue optimization plans

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
```bash
black app/ agents/ models/ config/ utils/
flake8 app/ agents/ models/ config/ utils/
```

### Adding New Agents

1. Create a new agent class in `agents/`
2. Inherit from `BaseAgent`
3. Implement the `get_system_prompt()` method
4. Add your agent methods
5. Import and register in `__init__.py`

Example:
```python
from .base_agent import BaseAgent

class MyAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return "You are my custom agent..."
    
    async def my_method(self, input_data: str) -> Dict[str, Any]:
        prompt = f"Process this: {input_data}"
        response = self.invoke_llm(prompt)
        return self.parse_response(response)
```

## Deployment

### Docker
```bash
docker build -t youtube-agent .
docker run -p 8000:8000 --env-file .env youtube-agent
```

### Environment Variables for Production
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
OPENAI_API_KEY=your-production-openai-key
SUPABASE_URL=your-production-supabase-url
SUPABASE_KEY=your-production-supabase-key
```

## Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Automation Status
```bash
curl http://localhost:8000/automation/status
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the logs for detailed error information

## Roadmap

- [ ] YouTube API integration for automatic uploads
- [ ] Advanced video editing with transitions
- [ ] Multi-language support
- [ ] Custom voice integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app for monitoring
- [ ] Integration with more video platforms
- [ ] AI-powered thumbnail design
- [ ] Advanced monetization features
