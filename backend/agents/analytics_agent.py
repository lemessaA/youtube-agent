from typing import Dict, Any, List, Optional
from .base_agent_groq import BaseAgent
from models.video import Analytics, Video
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AnalyticsAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are YouTube analytics agent. Analyze video performance and provide insights.

Input data:
- Views
- Click-through rate (CTR)
- Watch time
- Engagement metrics
- Audience retention

Analyze:
- Performance summary
- Success factors
- Improvement areas
- Next video recommendations
- Trend patterns

Output as JSON:
{
    "performance_summary": "Summary of how video performed",
    "success_factors": ["factor1", "factor2"],
    "improvement_suggestions": ["suggestion1", "suggestion2"],
    "next_video_ideas": ["idea1", "idea2"],
    "trend_insights": ["insight1", "insight2"],
    "performance_score": 85
}"""
    
    async def analyze_video_performance(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Analyze this YouTube video performance:

Title: {video_data.get('title', 'Unknown')}
Views: {video_data.get('views', 0)}
Likes: {video_data.get('likes', 0)}
Comments: {video_data.get('comments', 0)}
Watch Time: {video_data.get('watch_time', 0)} minutes
CTR: {video_data.get('ctr', 0)}%
Duration: {video_data.get('duration', 0)} seconds

Provide:
1. Performance summary vs industry benchmarks
2. What worked well
3. What needs improvement
4. Recommendations for next videos
5. Trend insights

Be specific and actionable."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error analyzing video performance: {e}")
            return self._create_fallback_analysis(video_data)
    
    def _create_fallback_analysis(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic analysis if AI fails"""
        views = video_data.get('views', 0)
        ctr = video_data.get('ctr', 0)
        
        performance_score = min(100, (views / 1000) + (ctr * 10))
        
        return {
            "performance_summary": f"Video got {views} views with {ctr}% CTR",
            "success_factors": ["Content published", "Video uploaded"],
            "improvement_suggestions": ["Improve thumbnail", "Optimize title"],
            "next_video_ideas": ["Follow-up content", "Related topic"],
            "trend_insights": ["Video was uploaded", "Content exists"],
            "performance_score": performance_score
        }
    
    def calculate_performance_metrics(self, video_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate key performance metrics"""
        views = video_data.get('views', 0)
        likes = video_data.get('likes', 0)
        comments = video_data.get('comments', 0)
        watch_time = video_data.get('watch_time', 0)
        duration = video_data.get('duration', 1)
        
        # Calculate metrics
        engagement_rate = ((likes + comments) / views * 100) if views > 0 else 0
        retention_rate = (watch_time / (duration * views / 60)) if views > 0 and duration > 0 else 0
        like_ratio = (likes / views * 100) if views > 0 else 0
        comment_ratio = (comments / views * 100) if views > 0 else 0
        
        return {
            "engagement_rate": round(engagement_rate, 2),
            "retention_rate": round(retention_rate, 2),
            "like_ratio": round(like_ratio, 2),
            "comment_ratio": round(comment_ratio, 2),
            "views_per_hour": round(views / 24, 2) if video_data.get('hours_published', 1) > 0 else views
        }
    
    def compare_to_benchmarks(self, metrics: Dict[str, float], niche: str) -> Dict[str, Any]:
        prompt = f"""Compare these video metrics to {niche} niche benchmarks:

Metrics: {metrics}

Provide:
- How each metric compares to industry average
- Overall performance rating
- Key strengths and weaknesses
- Specific improvement recommendations

Return as JSON with detailed comparison."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error comparing to benchmarks: {e}")
            return {"comparison": "Unable to compare due to error"}
    
    def generate_performance_report(self, videos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive performance report for multiple videos"""
        if not videos:
            return {"error": "No videos to analyze"}
        
        total_views = sum(v.get('views', 0) for v in videos)
        total_likes = sum(v.get('likes', 0) for v in videos)
        total_comments = sum(v.get('comments', 0) for v in videos)
        avg_ctr = sum(v.get('ctr', 0) for v in videos) / len(videos)
        
        # Find best and worst performing videos
        best_video = max(videos, key=lambda x: x.get('views', 0))
        worst_video = min(videos, key=lambda x: x.get('views', 0))
        
        report = {
            "summary": {
                "total_videos": len(videos),
                "total_views": total_views,
                "total_likes": total_likes,
                "total_comments": total_comments,
                "average_ctr": round(avg_ctr, 2),
                "average_views_per_video": round(total_views / len(videos), 2)
            },
            "best_performing": {
                "title": best_video.get('title', 'Unknown'),
                "views": best_video.get('views', 0),
                "ctr": best_video.get('ctr', 0)
            },
            "worst_performing": {
                "title": worst_video.get('title', 'Unknown'),
                "views": worst_video.get('views', 0),
                "ctr": worst_video.get('ctr', 0)
            },
            "trends": self._identify_trends(videos)
        }
        
        return report
    
    def _identify_trends(self, videos: List[Dict[str, Any]]) -> List[str]:
        """Identify performance trends across videos"""
        trends = []
        
        if len(videos) < 2:
            return ["Need more data for trend analysis"]
        
        # Sort videos by date (assuming they have created_at)
        sorted_videos = sorted(videos, key=lambda x: x.get('created_at', ''))
        
        # Compare recent vs older videos
        recent_videos = sorted_videos[-3:]  # Last 3 videos
        older_videos = sorted_videos[:-3] if len(sorted_videos) > 3 else []
        
        if older_videos:
            recent_avg_views = sum(v.get('views', 0) for v in recent_videos) / len(recent_videos)
            older_avg_views = sum(v.get('views', 0) for v in older_videos) / len(older_videos)
            
            if recent_avg_views > older_avg_views * 1.2:
                trends.append("Views are increasing over time")
            elif recent_avg_views < older_avg_views * 0.8:
                trends.append("Views are decreasing over time")
            else:
                trends.append("Views are stable")
        
        return trends
    
    def predict_video_potential(self, video_data: Dict[str, Any], historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict potential performance based on historical data"""
        if not historical_data:
            return {"prediction": "No historical data available"}
        
        # Calculate averages from historical data
        avg_views = sum(v.get('views', 0) for v in historical_data) / len(historical_data)
        avg_ctr = sum(v.get('ctr', 0) for v in historical_data) / len(historical_data)
        
        # Analyze video characteristics
        title_length = len(video_data.get('title', ''))
        description_length = len(video_data.get('description', ''))
        
        # Simple prediction based on factors
        prediction_score = 50  # Base score
        
        # Title length factor (optimal 50-60 chars)
        if 40 <= title_length <= 70:
            prediction_score += 10
        
        # Description length factor (optimal 200-500 words)
        if 100 <= description_length <= 1000:
            prediction_score += 5
        
        # Predicted metrics
        predicted_views = avg_views * (prediction_score / 50)
        predicted_ctr = avg_ctr * (prediction_score / 50)
        
        return {
            "prediction_score": min(100, prediction_score),
            "predicted_views": round(predicted_views),
            "predicted_ctr": round(predicted_ctr, 2),
            "confidence": "medium" if len(historical_data) >= 5 else "low",
            "factors": {
                "title_optimization": "good" if 40 <= title_length <= 70 else "needs_improvement",
                "description_optimization": "good" if 100 <= description_length <= 1000 else "needs_improvement"
            }
        }
    
    def get_audience_insights(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Based on this video data, provide audience insights:

Title: {video_data.get('title', '')}
Views: {video_data.get('views', 0)}
Engagement: {video_data.get('likes', 0)} likes, {video_data.get('comments', 0)} comments
Watch Time: {video_data.get('watch_time', 0)} minutes

Analyze:
- Demographic preferences
- Engagement patterns
- Content preferences
- Best posting times
- Audience behavior insights

Return as JSON with actionable insights."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error getting audience insights: {e}")
            return {"insights": "Unable to generate insights due to error"}
