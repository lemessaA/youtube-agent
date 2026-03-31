# Deployment Guide

Complete guide for deploying the AI YouTube Automation System to production.

## 🚀 Production Deployment

### 1. Server Requirements

**Minimum Requirements:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 50GB SSD
- Network: Stable internet connection

**Recommended Requirements:**
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 100GB+ SSD
- Network: High-speed internet

### 2. Environment Setup

#### Production Environment Variables

```bash
# Required
OPENAI_API_KEY=your_production_openai_key
SUPABASE_URL=your_production_supabase_url
SUPABASE_KEY=your_production_supabase_key
SECRET_KEY=your_unique_secret_key_here

# Optional but recommended
YOUTUBE_API_KEY=your_youtube_api_key
REDIS_URL=redis://localhost:6379/0

# Production settings
DEBUG=False
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

#### Security Configuration

```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set secure file permissions
chmod 600 .env
chmod 700 logs/
```

### 3. Database Setup

#### Supabase Production Setup

1. **Create Production Project**
   ```bash
   # Go to Supabase Dashboard
   # Create new project with production settings
   # Enable Row Level Security (RLS)
   # Configure connection pooling
   ```

2. **Run Database Schema**
   ```sql
   -- Copy contents of database/schema.sql
   -- Run in Supabase SQL Editor
   -- Verify all tables are created
   ```

3. **Configure Security**
   ```sql
   -- Update RLS policies for production
   -- Remove public access if needed
   -- Add authentication policies
   ```

### 4. Deployment Methods

#### Method 1: Direct Server Deployment

```bash
# Clone repository
git clone <your-repo-url>
cd youtube-agent

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with production values

# Setup database
python scripts/setup_database.py

# Test system
python scripts/test_system.py

# Start production server
python scripts/run_production.py
```

#### Method 2: Docker Deployment

```bash
# Build image
docker build -t youtube-agent:latest .

# Run container
docker run -d \
  --name youtube-agent \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/videos:/app/videos \
  youtube-agent:latest
```

#### Method 3: Docker Compose

```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f youtube-agent

# Stop services
docker-compose down
```

### 5. Reverse Proxy Setup

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # For file uploads
    client_max_body_size 100M;
}
```

#### SSL Certificate

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 6. Process Management

#### Systemd Service

```ini
# /etc/systemd/system/youtube-agent.service
[Unit]
Description=YouTube Automation System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/youtube-agent
Environment=PATH=/opt/youtube-agent/venv/bin
ExecStart=/opt/youtube-agent/venv/bin/python scripts/run_production.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable youtube-agent
sudo systemctl start youtube-agent
sudo systemctl status youtube-agent
```

### 7. Monitoring and Logging

#### Log Management

```bash
# Log rotation
sudo nano /etc/logrotate.d/youtube-agent

# Content:
/opt/youtube-agent/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
}
```

#### Health Monitoring

```bash
# Add to crontab for health checks
*/5 * * * * curl -f http://localhost:8000/health || echo "Service down" | mail -s "YouTube Agent Alert" admin@yourdomain.com
```

#### Performance Monitoring

```bash
# Monitor resource usage
htop
iostat -x 1
df -h

# Monitor application logs
tail -f logs/youtube_automation.log
```

### 8. Backup Strategy

#### Database Backups

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
pg_dump $DATABASE_URL > backups/db_backup_$DATE.sql
gzip backups/db_backup_$DATE.sql

# Keep only last 30 days
find backups/ -name "*.sql.gz" -mtime +30 -delete
```

#### File Backups

```bash
# Backup videos and logs
rsync -av /opt/youtube-agent/videos/ /backup/videos/
rsync -av /opt/youtube-agent/logs/ /backup/logs/
```

### 9. Scaling Considerations

#### Horizontal Scaling

```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  youtube-agent:
    image: youtube-agent:latest
    scale: 3
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - youtube-agent
```

#### Database Optimization

```sql
-- Add indexes for performance
CREATE INDEX CONCURRENTLY idx_videos_channel_created ON videos(channel_id, created_at DESC);
CREATE INDEX CONCURRENTLY idx_analytics_video_date ON analytics(video_id, date);

-- Partition large tables
CREATE TABLE analytics_y2024 PARTITION OF analytics FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### 10. Security Checklist

- [ ] Environment variables are set and secured
- [ ] SSL certificates are installed
- [ ] Firewall is configured
- [ ] Database access is restricted
- [ ] File permissions are correct
- [ ] Logging is enabled and monitored
- [ ] Backup strategy is implemented
- [ ] Security headers are configured
- [ ] Rate limiting is enabled
- [ ] Input validation is working

### 11. Performance Optimization

#### Application Optimization

```python
# Enable connection pooling
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Cache configuration
CACHE_TTL=3600
REDIS_POOL_SIZE=10
```

#### System Optimization

```bash
# Optimize system limits
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# Optimize network settings
echo "net.core.somaxconn = 65536" >> /etc/sysctl.conf
sysctl -p
```

### 12. Troubleshooting

#### Common Issues

1. **Service won't start**
   ```bash
   # Check logs
   sudo journalctl -u youtube-agent -f
   
   # Check environment
   python -c "from config.database import db; print(db.client)"
   ```

2. **Database connection issues**
   ```bash
   # Test connection
   python -c "from config.database import db; print(len(db.get_channels()))"
   ```

3. **High memory usage**
   ```bash
   # Monitor processes
   ps aux --sort=-%mem | head
   
   # Restart service if needed
   sudo systemctl restart youtube-agent
   ```

#### Emergency Procedures

1. **Service Down**
   ```bash
   # Quick restart
   sudo systemctl restart youtube-agent
   
   # Check if port is available
   sudo netstat -tlnp | grep :8000
   ```

2. **Database Issues**
   ```bash
   # Check database status
   python -c "from config.database import db; print(db.get_channels())"
   
   # Restore from backup if needed
   gunzip -c backups/db_backup_YYYYMMDD.sql.gz | psql $DATABASE_URL
   ```

### 13. Maintenance

#### Regular Tasks

```bash
# Weekly maintenance
0 2 * * 0 /opt/youtube-agent/scripts/weekly_maintenance.sh

# Monthly updates
0 3 1 * * /opt/youtube-agent/scripts/monthly_update.sh
```

#### Update Process

```bash
# Update application
git pull origin main
pip install -r requirements.txt
sudo systemctl restart youtube-agent

# Update database schema if needed
python scripts/migrate_database.py
```

---

## 🎯 Production Checklist

Before going live, ensure:

- [ ] All environment variables are configured
- [ ] Database schema is deployed
- [ ] SSL certificates are installed
- [ ] Monitoring is set up
- [ ] Backup strategy is implemented
- [ ] Security measures are in place
- [ ] Performance is optimized
- [ ] Documentation is updated
- [ ] Team is trained on procedures
- [ ] Emergency contacts are available

## 📞 Support

For deployment issues:
1. Check logs: `tail -f logs/youtube_automation.log`
2. Verify environment variables
3. Test database connection
4. Check system resources
5. Review this documentation

Your AI YouTube Automation System is now production-ready! 🚀
