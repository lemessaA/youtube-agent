from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
import asyncio
import logging
from datetime import datetime

from .trend_research_agent import TrendResearchAgent
from .script_writing_agent import ScriptWritingAgent
from .thumbnail_generator_agent import ThumbnailGeneratorAgent
from .video_generation_agent import VideoGenerationAgent
from .title_description_agent import TitleGeneratorAgent, DescriptionGeneratorAgent
from .analytics_agent import AnalyticsAgent
from .monetization_agent import MonetizationAgent
from models.video import VideoIdea, Script, Thumbnail, Video, Channel, NicheType
from config.database import db

logger = logging.getLogger(__name__)

class AutomationState(TypedDict):
    messages: Annotated[list, add_messages]
    channel: Optional[Channel]
    selected_topic: Optional[str]
    video_idea: Optional[VideoIdea]
    script: Optional[Script]
    thumbnail: Optional[Thumbnail]
    video_plan: Optional[Dict[str, Any]]
    titles: List[str]
    description_data: Optional[Dict[str, Any]]
    final_video: Optional[Video]
    analytics: Optional[Dict[str, Any]]
    monetization: Optional[Dict[str, Any]]
    error: Optional[str]
    status: str

class DailyAutomationAgent:
    def __init__(self):
        self.trend_agent = TrendResearchAgent()
        self.script_agent = ScriptWritingAgent()
        self.thumbnail_agent = ThumbnailGeneratorAgent()
        self.video_agent = VideoGenerationAgent()
        self.title_agent = TitleGeneratorAgent()
        self.description_agent = DescriptionGeneratorAgent()
        self.analytics_agent = AnalyticsAgent()
        self.monetization_agent = MonetizationAgent()
        
        self.graph = self._create_automation_graph()
    
    def _create_automation_graph(self) -> StateGraph:
        """Create the LangGraph workflow for daily automation"""
        workflow = StateGraph(AutomationState)
        
        # Add nodes
        workflow.add_node("start", self._start_automation)
        workflow.add_node("research_trends", self._research_trends)
        workflow.add_node("select_topic", self._select_topic)
        workflow.add_node("write_script", self._write_script)
        workflow.add_node("generate_thumbnail", self._generate_thumbnail)
        workflow.add_node("create_video_plan", self._create_video_plan)
        workflow.add_node("generate_titles", self._generate_titles)
        workflow.add_node("generate_description", self._generate_description)
        workflow.add_node("create_video", self._create_video)
        workflow.add_node("analyze_performance", self._analyze_performance)
        workflow.add_node("monetization_strategy", self._monetization_strategy)
        workflow.add_node("finalize", self._finalize_video)
        
        # Add edges
        workflow.set_entry_point("start")
        workflow.add_edge("start", "research_trends")
        workflow.add_edge("research_trends", "select_topic")
        workflow.add_edge("select_topic", "write_script")
        workflow.add_edge("write_script", "generate_thumbnail")
        workflow.add_edge("generate_thumbnail", "create_video_plan")
        workflow.add_edge("create_video_plan", "generate_titles")
        workflow.add_edge("generate_titles", "generate_description")
        workflow.add_edge("generate_description", "create_video")
        workflow.add_edge("create_video", "analyze_performance")
        workflow.add_edge("analyze_performance", "monetization_strategy")
        workflow.add_edge("monetization_strategy", "finalize")
        workflow.add_edge("finalize", END)
        
        # Add conditional edges for error handling
        workflow.add_conditional_edges(
            "research_trends",
            self._check_for_errors,
            {
                "error": END,
                "continue": "select_topic"
            }
        )
        
        workflow.add_conditional_edges(
            "create_video",
            self._check_for_errors,
            {
                "error": END,
                "continue": "analyze_performance"
            }
        )
        
        return workflow.compile()
    
    async def run_daily_automation(self, channel_id: str) -> Dict[str, Any]:
        """Run the complete daily automation workflow"""
        try:
            # Get channel information
            channels = db.get_channels()
            channel = next((c for c in channels if c.get('id') == channel_id), None)
            
            if not channel:
                return {"error": "Channel not found"}
            
            # Initialize state
            initial_state = AutomationState(
                messages=[],
                channel=Channel(**channel),
                selected_topic=None,
                video_idea=None,
                script=None,
                thumbnail=None,
                video_plan=None,
                titles=[],
                description_data=None,
                final_video=None,
                analytics=None,
                monetization=None,
                error=None,
                status="starting"
            )
            
            # Run the workflow
            result = await self.graph.ainvoke(initial_state)
            
            return {
                "status": "completed",
                "video": result.get("final_video"),
                "analytics": result.get("analytics"),
                "monetization": result.get("monetization"),
                "error": result.get("error")
            }
            
        except Exception as e:
            logger.error(f"Error in daily automation: {e}")
            return {"error": str(e), "status": "failed"}
    
    async def _start_automation(self, state: AutomationState) -> AutomationState:
        """Start the automation process"""
        logger.info(f"Starting daily automation for channel: {state['channel'].name}")
        state["status"] = "researching_trends"
        return state
    
    async def _research_trends(self, state: AutomationState) -> AutomationState:
        """Research trending topics"""
        try:
            niche = state["channel"].niche
            video_ideas = await self.trend_agent.research_trends(niche)
            
            if not video_ideas:
                state["error"] = "No video ideas generated"
                return state
            
            # Store ideas in database
            for idea in video_ideas:
                idea_data = {
                    "title": idea.title,
                    "description": idea.description,
                    "niche": idea.niche.value,
                    "viral_score": idea.viral_score,
                    "target_audience": idea.target_audience,
                    "why_trending": idea.why_trending,
                    "search_demand": idea.search_demand,
                    "competition_level": idea.competition_level,
                    "status": "idea"
                }
                db.insert_video_idea(idea_data)
            
            state["video_ideas"] = video_ideas
            state["status"] = "selecting_topic"
            return state
            
        except Exception as e:
            logger.error(f"Error researching trends: {e}")
            state["error"] = str(e)
            return state
    
    async def _select_topic(self, state: AutomationState) -> AutomationState:
        """Select the best topic from researched ideas"""
        try:
            video_ideas = state.get("video_ideas", [])
            
            if not video_ideas:
                state["error"] = "No video ideas available for selection"
                return state
            
            # Select the idea with highest viral score
            best_idea = max(video_ideas, key=lambda x: x.viral_score)
            state["selected_topic"] = best_idea.title
            state["video_idea"] = best_idea
            state["status"] = "writing_script"
            return state
            
        except Exception as e:
            logger.error(f"Error selecting topic: {e}")
            state["error"] = str(e)
            return state
    
    async def _write_script(self, state: AutomationState) -> AutomationState:
        """Write script for selected topic"""
        try:
            topic = state["selected_topic"]
            target_audience = state["video_idea"].target_audience
            
            script = await self.script_agent.write_script(topic, target_audience)
            script = self.script_agent.add_timing_cues(script)
            
            state["script"] = script
            state["status"] = "generating_thumbnail"
            return state
            
        except Exception as e:
            logger.error(f"Error writing script: {e}")
            state["error"] = str(e)
            return state
    
    async def _generate_thumbnail(self, state: AutomationState) -> AutomationState:
        """Generate thumbnail for video"""
        try:
            topic = state["selected_topic"]
            title = state["script"].title
            
            thumbnail = await self.thumbnail_agent.generate_thumbnails(topic, title)
            state["thumbnail"] = thumbnail
            state["status"] = "creating_video_plan"
            return state
            
        except Exception as e:
            logger.error(f"Error generating thumbnail: {e}")
            state["error"] = str(e)
            return state
    
    async def _create_video_plan(self, state: AutomationState) -> AutomationState:
        """Create video production plan"""
        try:
            script = state["script"]
            video_plan = await self.video_agent.generate_video_plan(script)
            
            state["video_plan"] = video_plan
            state["status"] = "generating_titles"
            return state
            
        except Exception as e:
            logger.error(f"Error creating video plan: {e}")
            state["error"] = str(e)
            return state
    
    async def _generate_titles(self, state: AutomationState) -> AutomationState:
        """Generate video titles"""
        try:
            topic = state["selected_topic"]
            target_audience = state["video_idea"].target_audience
            
            titles = await self.title_agent.generate_titles(topic, target_audience)
            state["titles"] = titles
            state["status"] = "generating_description"
            return state
            
        except Exception as e:
            logger.error(f"Error generating titles: {e}")
            state["error"] = str(e)
            return state
    
    async def _generate_description(self, state: AutomationState) -> AutomationState:
        """Generate video description"""
        try:
            title = state["titles"][0] if state["titles"] else state["selected_topic"]
            topic = state["selected_topic"]
            script_points = state["script"].main_points
            
            description_data = await self.description_agent.generate_description(title, topic, script_points)
            state["description_data"] = description_data
            state["status"] = "creating_video"
            return state
            
        except Exception as e:
            logger.error(f"Error generating description: {e}")
            state["error"] = str(e)
            return state
    
    async def _create_video(self, state: AutomationState) -> AutomationState:
        """Create the actual video file"""
        try:
            video_plan = state["video_plan"]
            output_path = f"/tmp/video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            
            video_file_path = await self.video_agent.create_video_file(video_plan, output_path)
            optimized_path = await self.video_agent.optimize_video_for_youtube(video_file_path)
            
            # Create video record
            video = Video(
                channel_id=state["channel"].id,
                video_idea_id=state["video_idea"].id,
                script_id=state["script"].id,
                thumbnail_id=state["thumbnail"].id,
                title=state["titles"][0] if state["titles"] else state["selected_topic"],
                description=state["description_data"].get("description", ""),
                tags=state["description_data"].get("tags", []),
                duration=state["script"].estimated_duration,
                file_path=optimized_path,
                status="video"
            )
            
            state["final_video"] = video
            state["status"] = "analyzing_performance"
            return state
            
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            state["error"] = str(e)
            return state
    
    async def _analyze_performance(self, state: AutomationState) -> AutomationState:
        """Analyze potential video performance"""
        try:
            video_data = {
                "title": state["final_video"].title,
                "duration": state["final_video"].duration,
                "description": state["final_video"].description
            }
            
            analytics = await self.analytics_agent.analyze_video_performance(video_data)
            state["analytics"] = analytics
            state["status"] = "monetization_strategy"
            return state
            
        except Exception as e:
            logger.error(f"Error analyzing performance: {e}")
            state["error"] = str(e)
            return state
    
    async def _monetization_strategy(self, state: AutomationState) -> AutomationState:
        """Generate monetization strategy"""
        try:
            channel_data = {
                "name": state["channel"].name,
                "niche": state["channel"].niche.value,
                "subscribers": 1000,  # Estimate
                "avg_views": 500,     # Estimate
                "engagement_rate": 5.0  # Estimate
            }
            
            monetization = await self.monetization_agent.analyze_monetization_potential(channel_data)
            state["monetization"] = monetization
            state["status"] = "finalizing"
            return state
            
        except Exception as e:
            logger.error(f"Error creating monetization strategy: {e}")
            state["error"] = str(e)
            return state
    
    async def _finalize_video(self, state: AutomationState) -> AutomationState:
        """Finalize video and save to database"""
        try:
            # Save video to database
            video_data = {
                "channel_id": state["final_video"].channel_id,
                "title": state["final_video"].title,
                "description": state["final_video"].description,
                "tags": state["final_video"].tags,
                "duration": state["final_video"].duration,
                "file_path": state["final_video"].file_path,
                "status": "video"
            }
            
            saved_video = db.insert_video(video_data)
            state["final_video"].id = saved_video["id"] if saved_video else None
            
            state["status"] = "completed"
            return state
            
        except Exception as e:
            logger.error(f"Error finalizing video: {e}")
            state["error"] = str(e)
            return state
    
    def _check_for_errors(self, state: AutomationState) -> str:
        """Check if there are any errors in the state"""
        if state.get("error"):
            return "error"
        return "continue"
    
    async def get_automation_status(self) -> Dict[str, Any]:
        """Get current automation status"""
        return {
            "status": "ready",
            "last_run": None,
            "next_run": None,
            "total_videos_created": 0,
            "success_rate": 100.0
        }
