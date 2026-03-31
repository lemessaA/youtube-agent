# Quick Start Guide

Get your AI YouTube Automation system running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add:
```bash
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
```

### 3. Set Up Database
1. Go to [Supabase](https://supabase.com) and create a new project
2. Open the SQL editor in your Supabase project
3. Copy and paste the contents of `database/schema.sql`
4. Run the SQL to create all tables

### 4. Start the Server
```bash
python -m app.main
```

The API will be running at `http://localhost:8000`

## 🎯 Test the System

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

## 📊 API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🤖 Daily Automation

The system will automatically:
1. Research trending topics
2. Select the best topic
3. Write an engaging script
4. Generate thumbnails
5. Create the video
6. Optimize title and description
7. Analyze performance potential
8. Suggest monetization strategies

## 🔧 Common Issues

### OpenAI API Key
Make sure your OpenAI API key has sufficient credits. The system uses GPT-4 for best results.

### Supabase Connection
- Double-check your Supabase URL and key
- Ensure you ran the schema.sql file
- Check that RLS policies are enabled

### Video Generation
The system creates placeholder videos by default. For production, integrate with:
- Stock footage APIs (Storyblocks, Shutterstock)
- Text-to-speech services
- Professional video editing tools

## 📈 Next Steps

1. **Set up daily scheduling**: Use cron jobs or the built-in scheduler
2. **Connect YouTube API**: Enable automatic uploads
3. **Configure monetization**: Set up affiliate links and sponsorships
4. **Monitor analytics**: Track performance and optimize
5. **Scale to multiple channels**: Duplicate success across niches

## 🆘 Need Help?

- Check the logs for detailed error messages
- Visit `/health` endpoint to check system status
- Review the full README.md for detailed documentation
- Create an issue on GitHub for bugs or feature requests

## 🎉 You're Ready!

Your AI YouTube Automation system is now running. It will generate daily videos automatically and help you grow your YouTube channel with AI-powered content!
