-- YouTube Automation Database Schema
-- Run this in your Supabase SQL editor

-- Channels table
CREATE TABLE IF NOT EXISTS channels (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    niche VARCHAR(50) NOT NULL,
    youtube_channel_id VARCHAR(100),
    description TEXT,
    target_audience TEXT,
    upload_frequency VARCHAR(20) DEFAULT 'daily',
    video_length_range VARCHAR(20) DEFAULT '60-120',
    style VARCHAR(50) DEFAULT 'faceless',
    monetization_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Video ideas table
CREATE TABLE IF NOT EXISTS video_ideas (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    niche VARCHAR(50) NOT NULL,
    viral_score INTEGER DEFAULT 50 CHECK (viral_score >= 1 AND viral_score <= 100),
    target_audience TEXT,
    why_trending TEXT,
    search_demand VARCHAR(20) DEFAULT 'medium',
    competition_level VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'idea',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Scripts table
CREATE TABLE IF NOT EXISTS scripts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    hook TEXT,
    intro TEXT,
    main_points JSONB,
    conclusion TEXT,
    call_to_action TEXT,
    scenes JSONB,
    voice_tone VARCHAR(100),
    estimated_duration INTEGER DEFAULT 90,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Thumbnails table
CREATE TABLE IF NOT EXISTS thumbnails (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    thumbnail_text VARCHAR(255),
    background_idea TEXT,
    colors JSONB,
    visual_concept TEXT,
    thumbnail_variations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Videos table
CREATE TABLE IF NOT EXISTS videos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    channel_id UUID REFERENCES channels(id) ON DELETE CASCADE,
    video_idea_id UUID REFERENCES video_ideas(id) ON DELETE SET NULL,
    script_id UUID REFERENCES scripts(id) ON DELETE SET NULL,
    thumbnail_id UUID REFERENCES thumbnails(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    tags JSONB,
    duration INTEGER,
    file_path TEXT,
    youtube_video_id VARCHAR(100),
    status VARCHAR(20) DEFAULT 'idea',
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    watch_time INTEGER DEFAULT 0,
    ctr DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE
);

-- Analytics table
CREATE TABLE IF NOT EXISTS analytics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    watch_time INTEGER DEFAULT 0,
    ctr DECIMAL(5,2) DEFAULT 0.0,
    audience_retention DECIMAL(5,2) DEFAULT 0.0,
    revenue DECIMAL(10,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trending topics table
CREATE TABLE IF NOT EXISTS trending_topics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    niche VARCHAR(50) NOT NULL,
    search_volume INTEGER DEFAULT 0,
    competition_score INTEGER DEFAULT 50,
    trending_score INTEGER DEFAULT 50,
    keywords JSONB,
    related_topics JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Monetization strategies table
CREATE TABLE IF NOT EXISTS monetization_strategies (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    channel_id UUID REFERENCES channels(id) ON DELETE CASCADE,
    strategy_type VARCHAR(100),
    affiliate_links JSONB DEFAULT '[]',
    sponsorship_opportunities JSONB DEFAULT '[]',
    digital_products JSONB DEFAULT '[]',
    courses JSONB DEFAULT '[]',
    revenue_streams JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Automation logs table
CREATE TABLE IF NOT EXISTS automation_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    channel_id UUID REFERENCES channels(id) ON DELETE CASCADE,
    video_id UUID REFERENCES videos(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    metadata JSONB,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_channels_niche ON channels(niche);
CREATE INDEX IF NOT EXISTS idx_video_ideas_niche ON video_ideas(niche);
CREATE INDEX IF NOT EXISTS idx_video_ideas_viral_score ON video_ideas(viral_score DESC);
CREATE INDEX IF NOT EXISTS idx_videos_channel_id ON videos(channel_id);
CREATE INDEX IF NOT EXISTS idx_videos_status ON videos(status);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_video_id ON analytics(video_id);
CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics(date);
CREATE INDEX IF NOT EXISTS idx_trending_topics_niche ON trending_topics(niche);
CREATE INDEX IF NOT EXISTS idx_automation_logs_channel_id ON automation_logs(channel_id);
CREATE INDEX IF NOT EXISTS idx_automation_logs_started_at ON automation_logs(started_at DESC);

-- Row Level Security (RLS) policies
ALTER TABLE channels ENABLE ROW LEVEL SECURITY;
ALTER TABLE video_ideas ENABLE ROW LEVEL SECURITY;
ALTER TABLE scripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE thumbnails ENABLE ROW LEVEL SECURITY;
ALTER TABLE videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;
ALTER TABLE trending_topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE monetization_strategies ENABLE ROW LEVEL SECURITY;
ALTER TABLE automation_logs ENABLE ROW LEVEL SECURITY;

-- Public access policies (adjust as needed for your security requirements)
CREATE POLICY "Enable read access for all users" ON channels FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON channels FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON channels FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON channels FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON video_ideas FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON video_ideas FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON video_ideas FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON video_ideas FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON scripts FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON scripts FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON scripts FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON scripts FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON thumbnails FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON thumbnails FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON thumbnails FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON thumbnails FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON videos FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON videos FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON videos FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON videos FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON analytics FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON analytics FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON analytics FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON analytics FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON trending_topics FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON trending_topics FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON trending_topics FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON trending_topics FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON monetization_strategies FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON monetization_strategies FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON monetization_strategies FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON monetization_strategies FOR DELETE USING (true);

CREATE POLICY "Enable read access for all users" ON automation_logs FOR SELECT USING (true);
CREATE POLICY "Enable insert for all users" ON automation_logs FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update for all users" ON automation_logs FOR UPDATE USING (true);
CREATE POLICY "Enable delete for all users" ON automation_logs FOR DELETE USING (true);

-- Functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_channels_updated_at BEFORE UPDATE ON channels FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_video_ideas_updated_at BEFORE UPDATE ON video_ideas FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_trending_topics_updated_at BEFORE UPDATE ON trending_topics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_monetization_strategies_updated_at BEFORE UPDATE ON monetization_strategies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
