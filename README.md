# AI YouTube Automation System

Complete AI-powered YouTube automation system that generates daily videos automatically and grows revenue.

## 🏗️ Project Structure

```
youtube-agent/
├── backend/              # FastAPI backend server
│   ├── agents/          # AI agents for different tasks
│   ├── app/            # FastAPI application
│   ├── config/         # Configuration files
│   ├── database/       # Database schemas and migrations
│   ├── models/         # Data models
│   ├── utils/          # Utility functions
│   ├── scripts/        # Setup and utility scripts
│   └── tests/          # Backend tests
├── frontend/           # Next.js frontend application
│   ├── src/           # Source code
│   │   ├── app/       # Next.js app router pages
│   │   ├── components/ # React components
│   │   └── lib/       # Utilities and API clients
│   └── public/        # Static assets
├── docs/              # Documentation
└── docker-compose.yml # Docker setup
```

## 🤖 AI Agents

- **Trend Research Agent**: Finds trending video ideas in your niche
- **Script Writing Agent**: Creates engaging 60-120 second scripts
- **Thumbnail Generator Agent**: Designs clickable thumbnails
- **Video Generation Agent**: Creates faceless videos with stock footage
- **Title & Description Generator**: Optimizes for SEO and CTR
- **Analytics Agent**: Analyzes performance and suggests improvements
- **Monetization Agent**: Suggests revenue strategies
- **Daily Automation Agent**: Orchestrates the entire workflow

## 🎯 Supported Niches

- AI Tools
- Startup Ideas  
- Tech Explainers
- Make Money Online
- Side Hustles

## 📊 Video Specifications

- **Length**: 60-120 seconds
- **Style**: Faceless automation
- **Upload Frequency**: Daily
- **Format**: Short educational content

## 🛠️ Tech Stack

### Backend
- **API Framework**: FastAPI
- **AI/ML**: LangChain, LangGraph, Groq (Cloud LLM)
- **Database**: Supabase
- **Video Processing**: MoviePy
- **Image Processing**: Pillow
- **Task Queue**: Celery with Redis
- **Scheduling**: APScheduler

### Frontend
- **Framework**: Next.js 15
- **UI**: React with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React hooks
- **API Client**: Fetch API with TypeScript

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 18+**
- **Groq API Key** (free at [console.groq.com](https://console.groq.com))
- **Supabase** account (for database)

### 1. Clone and Setup Backend

```bash
# Clone repository
git clone <repository-url>
cd youtube-agent

# Setup Python virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys (see setup instructions below)
```

### 2. Setup Frontend

```bash
# Install frontend dependencies
cd ../frontend
npm install

# Start development server
npm run dev
```

### 3. Configure API Keys

Edit `backend/.env` with your credentials:

```env
# Groq Configuration (Required)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama3-8b-8192

# Supabase Configuration (Required)
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# Optional APIs
YOUTUBE_API_KEY=your_youtube_api_key_here
```

### 4. Setup Database

1. Create a [Supabase](https://supabase.com) project
2. Run the SQL schema from `backend/database/schema.sql`
3. Update `.env` with your Supabase credentials

### 5. Start the Application

```bash
# Terminal 1: Start backend
cd backend
python run.py

# Terminal 2: Start frontend  
cd frontend
npm run dev
```

## 📚 API Documentation

- **Backend API**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## 🔧 Setup Guides

- [Groq API Setup](docs/GROQ_SETUP.md) - Get your free API key
- [Supabase Setup](docs/QUICK_START.md) - Database configuration
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment

## 🐳 Docker Setup

```bash
# Start with Docker Compose
docker-compose up --build

# Services will be available at:
# - Backend: http://localhost:8000
# - Redis: localhost:6379
```

## 📈 Usage

### Create a Channel
```bash
curl -X POST "http://localhost:8000/channels" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Tools Daily",
    "niche": "ai_tools",
    "description": "Daily AI tools and tips"
  }'
```

### Generate Content
```bash
curl -X POST "http://localhost:8000/test/generation"
```

### Check Results
```bash
curl "http://localhost:8000/videos"
```

## 🤖 Daily Automation

The system automatically:
1. **Research** trending topics in your niche
2. **Select** the best topics based on potential
3. **Write** engaging scripts optimized for retention
4. **Generate** eye-catching thumbnails
5. **Create** videos with stock footage and voiceover
6. **Optimize** titles and descriptions for SEO
7. **Analyze** performance potential
8. **Suggest** monetization strategies

## 🔍 Features

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ AI-powered content generation
- ✅ Database integration with Supabase
- ✅ Background task processing
- ✅ Rate limiting and security middleware
- ✅ Comprehensive error handling
- ✅ API documentation with Swagger

### Frontend Features (Coming Soon)
- 🚧 Modern React/Next.js dashboard
- 🚧 Channel management interface
- 🚧 Video generation workflow
- 🚧 Analytics and performance tracking
- 🚧 Real-time notifications
- 🚧 Responsive design

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

---

**Note**: This system is designed for educational and automation purposes. Please comply with YouTube's Terms of Service and Community Guidelines when using this tool.