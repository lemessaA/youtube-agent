from typing import Dict, Any, List
from .base_agent_groq import BaseAgent
from models.video import MonetizationStrategy
import logging

logger = logging.getLogger(__name__)

class MonetizationAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are monetization agent for YouTube channels. Suggest revenue strategies.

Revenue streams to consider:
1. YouTube AdSense
2. Affiliate marketing
3. Sponsorships
4. Digital products
5. Online courses
6. Merchandise
7. Consulting services
8. Patreon/Membership

For each suggestion provide:
- Revenue potential
- Implementation difficulty
- Time to see results
- Required audience size
- Best practices

Output as JSON:
{
    "revenue_ideas": [
        {
            "method": "Affiliate Marketing",
            "potential": "high/medium/low",
            "difficulty": "easy/medium/hard",
            "time_to_results": "immediate/1-3months/3-6months",
            "min_audience": "1000 subscribers",
            "implementation": "Step-by-step guide",
            "expected_monthly": "$100-500"
        }
    ],
    "affiliate_ideas": ["product1", "product2"],
    "sponsor_ideas": ["company1", "company2"],
    "product_ideas": ["course", "ebook"]
}"""
    
    async def analyze_monetization_potential(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Analyze monetization potential for this YouTube channel:

Channel: {channel_data.get('name', 'Unknown')}
Niche: {channel_data.get('niche', 'Unknown')}
Subscribers: {channel_data.get('subscribers', 0)}
Average Views: {channel_data.get('avg_views', 0)}
Engagement Rate: {channel_data.get('engagement_rate', 0)}%

Provide:
1. Best monetization strategies for this niche
2. Revenue potential estimates
3. Implementation timeline
4. Required audience size for each method
5. Step-by-step action plan

Be specific and realistic."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error analyzing monetization potential: {e}")
            return self._create_fallback_monetization_plan(channel_data)
    
    def _create_fallback_monetization_plan(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic monetization plan if AI fails"""
        subscribers = channel_data.get('subscribers', 0)
        
        return {
            "revenue_ideas": [
                {
                    "method": "YouTube AdSense",
                    "potential": "medium",
                    "difficulty": "easy",
                    "time_to_results": "immediate",
                    "min_audience": "1000 subscribers, 4000 watch hours",
                    "implementation": "Enable monetization in YouTube Studio",
                    "expected_monthly": f"${min(100, subscribers * 0.1)}-{min(500, subscribers * 0.5)}"
                }
            ],
            "affiliate_ideas": ["Amazon products", "Software tools"],
            "sponsor_ideas": ["Tech companies", "Online services"],
            "product_ideas": ["Online course", "E-book guide"]
        }
    
    def generate_affiliate_opportunities(self, niche: str, audience_size: int) -> List[Dict[str, Any]]:
        prompt = f"""Generate affiliate marketing opportunities for {niche} YouTube channel:

Audience Size: {audience_size} subscribers
Niche: {niche}

Suggest:
1. Best affiliate programs for this niche
2. Specific products to promote
3. Commission rates
4. Promotion strategies
5. Expected conversion rates

Focus on products that align with the content and audience needs."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif "opportunities" in parsed_response:
                return parsed_response["opportunities"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error generating affiliate opportunities: {e}")
            return []
    
    def find_sponsorship_opportunities(self, niche: str, channel_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        prompt = f"""Find sponsorship opportunities for {niche} YouTube channel:

Channel Stats:
- Subscribers: {channel_stats.get('subscribers', 0)}
- Average Views: {channel_stats.get('avg_views', 0)}
- Engagement Rate: {channel_stats.get('engagement', 0)}%

Identify:
1. Types of companies that sponsor this niche
2. Expected sponsorship rates
3. How to approach sponsors
4. Sponsorship deal structures
5. Companies to target

Be realistic about audience size and niche."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif "sponsors" in parsed_response:
                return parsed_response["sponsors"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error finding sponsorship opportunities: {e}")
            return []
    
    def create_digital_product_ideas(self, niche: str, audience_needs: List[str]) -> List[Dict[str, Any]]:
        prompt = f"""Create digital product ideas for {niche} YouTube channel:

Audience Needs: {', '.join(audience_needs)}

Generate product ideas:
1. Online courses
2. E-books
3. Templates
4. Software tools
5. Membership programs

For each idea include:
- Product type
- Target audience pain point
- Price range
- Development difficulty
- Marketing strategy
- Revenue potential

Focus on solving real audience problems."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif "products" in parsed_response:
                return parsed_response["products"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error creating digital product ideas: {e}")
            return []
    
    def calculate_revenue_projections(self, monetization_plan: Dict[str, Any], channel_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate revenue projections based on monetization plan"""
        projections = {}
        
        # YouTube AdSense revenue
        avg_views = channel_stats.get('avg_views', 0)
        rpm = channel_stats.get('rpm', 2.0)  # Revenue per 1000 views
        
        projections["adsense"] = {
            "monthly_revenue": round((avg_views * 30 * rpm) / 1000, 2),
            "yearly_revenue": round((avg_views * 365 * rpm) / 1000, 2)
        }
        
        # Affiliate marketing (conservative 1% conversion rate)
        affiliate_products = monetization_plan.get("affiliate_ideas", [])
        if affiliate_products:
            projections["affiliate"] = {
                "monthly_revenue": round(avg_views * 30 * 0.01 * 10, 2),  # $10 avg commission
                "yearly_revenue": round(avg_views * 365 * 0.01 * 10, 2)
            }
        
        # Sponsorships (based on subscriber count)
        subscribers = channel_stats.get('subscribers', 0)
        if subscribers >= 1000:
            sponsorship_rate_per_1000 = 20  # Industry average
            sponsorship_months_per_year = 6  # Conservative estimate
            
            projections["sponsorships"] = {
                "monthly_revenue": round((subscribers / 1000) * sponsorship_rate_per_1000 * sponsorship_months_per_year / 12, 2),
                "yearly_revenue": round((subscribers / 1000) * sponsorship_rate_per_1000 * sponsorship_months_per_year, 2)
            }
        
        # Digital products (conservative estimates)
        digital_products = monetization_plan.get("product_ideas", [])
        if digital_products:
            monthly_sales = max(1, subscribers * 0.001)  # 0.1% conversion rate
            avg_product_price = 50
            
            projections["digital_products"] = {
                "monthly_revenue": round(monthly_sales * avg_product_price, 2),
                "yearly_revenue": round(monthly_sales * 12 * avg_product_price, 2)
            }
        
        # Total projections
        total_monthly = sum(projection.get("monthly_revenue", 0) for projection in projections.values())
        total_yearly = sum(projection.get("yearly_revenue", 0) for projection in projections.values())
        
        projections["total"] = {
            "monthly_revenue": round(total_monthly, 2),
            "yearly_revenue": round(total_yearly, 2)
        }
        
        return projections
    
    def create_monetization_roadmap(self, current_stats: Dict[str, Any], goals: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""Create monetization roadmap for YouTube channel:

Current Stats:
- Subscribers: {current_stats.get('subscribers', 0)}
- Average Views: {current_stats.get('avg_views', 0)}
- Niche: {current_stats.get('niche', 'Unknown')}

Goals:
- Target Monthly Revenue: ${goals.get('monthly_revenue', 1000)}
- Timeline: {goals.get('timeline', '12 months')}

Create step-by-step roadmap:
1. What to implement now (0-3 months)
2. What to implement next (3-6 months)
3. What to implement later (6-12 months)
4. Milestones to track
5. Required resources
6. Risk mitigation

Be realistic and actionable."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error creating monetization roadmap: {e}")
            return {"roadmap": "Unable to generate roadmap due to error"}
    
    def optimize_existing_revenue_streams(self, current_revenue: Dict[str, Any]) -> List[str]:
        prompt = f"""Optimize these existing revenue streams:

Current Revenue: {current_revenue}

Provide specific optimization strategies:
1. How to increase AdSense revenue
2. How to improve affiliate conversions
3. How to attract better sponsorships
4. How to sell more digital products
5. How to reduce revenue volatility

Focus on actionable improvements that can be implemented quickly."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif "strategies" in parsed_response:
                return parsed_response["strategies"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error optimizing revenue streams: {e}")
            return []
