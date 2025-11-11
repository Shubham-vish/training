"""
State Schema for Content Creation Multi-Agent System

Defines the shared state structure that flows through the LangGraph workflow,
enhanced with CrewAI role-based collaboration patterns.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ContentCreationState(BaseModel):
    """
    Shared state for the content creation workflow.
    
    This state flows between all agents in the LangGraph workflow,
    with each agent (following CrewAI role patterns) contributing
    their specialized outputs.
    """
    
    # Input Parameters
    topic: str = Field(description="Main topic for content creation")
    content_type: str = Field(default="Short (60 seconds)", description="Type of content to generate")
    style: str = Field(default="Educational", description="Content style or tone")
    target_audience: str = Field(default="General", description="Target audience for the content")
    
    # Workflow State
    revision_number: int = Field(default=0, description="Current revision iteration")
    max_revisions: int = Field(default=2, description="Maximum allowed revisions")
    current_step: str = Field(default="", description="Current workflow step")
    
    # Agent Outputs (CrewAI Role-based)
    # Content Manager outputs
    content_outline: str = Field(default="", description="Content strategy and outline")
    content_goals: List[str] = Field(default_factory=list, description="Content objectives")
    
    # Research Specialist outputs  
    research_plan: str = Field(default="", description="Research strategy and approach")
    research_queries: List[str] = Field(default_factory=list, description="Specific research queries")
    
    # Data Analyst outputs
    research_data: str = Field(default="", description="Collected research information")
    key_insights: List[str] = Field(default_factory=list, description="Key research insights")
    
    # Content Writer outputs
    script: str = Field(default="", description="Generated content script")
    content_structure: Dict[str, str] = Field(default_factory=dict, description="Content structure breakdown")
    
    # Quality Assurance outputs
    quality_score: float = Field(default=0.0, description="Content quality assessment score")
    critique: str = Field(default="", description="Quality feedback and recommendations")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Specific improvement suggestions")
    
    # SEO Specialist outputs
    hashtags: List[str] = Field(default_factory=list, description="Generated hashtags")
    seo_keywords: List[str] = Field(default_factory=list, description="SEO-optimized keywords")
    
    # Marketing Specialist outputs
    cta: str = Field(default="", description="Call-to-action text")
    engagement_hooks: List[str] = Field(default_factory=list, description="Engagement strategies")
    
    # Metadata and Tracking
    agent_history: List[Dict[str, Any]] = Field(default_factory=list, description="Agent execution history")
    execution_time: Dict[str, float] = Field(default_factory=dict, description="Agent execution times")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    created_at: datetime = Field(default_factory=datetime.now, description="State creation timestamp")
    
    class Config:
        arbitrary_types_allowed = True
        
    def add_agent_execution(self, agent_name: str, role: str, output: Dict[str, Any], execution_time: float):
        """Record agent execution in history"""
        self.agent_history.append({
            "agent": agent_name,
            "role": role, 
            "timestamp": datetime.now().isoformat(),
            "execution_time": execution_time,
            "output_keys": list(output.keys())
        })
        self.execution_time[agent_name] = execution_time
        
    def get_workflow_progress(self) -> Dict[str, Any]:
        """Get current workflow progress summary"""
        completed_agents = len(self.agent_history)
        total_agents = 7  # Based on our agent count
        
        return {
            "completed_agents": completed_agents,
            "total_agents": total_agents,
            "progress_percentage": (completed_agents / total_agents) * 100,
            "current_step": self.current_step,
            "revision_number": self.revision_number,
            "quality_score": self.quality_score
        }
        
    def is_content_ready(self) -> bool:
        """Check if content creation is complete"""
        required_outputs = [
            bool(self.script),
            bool(self.hashtags),
            bool(self.cta)
        ]
        return all(required_outputs) and self.quality_score >= 7.0
        
    def needs_revision(self) -> bool:
        """Check if content needs revision"""
        return (
            self.quality_score < 7.0 and 
            self.revision_number < self.max_revisions and
            bool(self.script)  # Only revise if we have content to revise
        )


# State transformation helpers
def create_initial_state(
    topic: str,
    content_type: str = "Short (60 seconds)",
    style: str = "Educational",
    target_audience: str = "General"
) -> ContentCreationState:
    """Create initial state for content creation workflow"""
    return ContentCreationState(
        topic=topic,
        content_type=content_type,
        style=style,
        target_audience=target_audience,
        current_step="initialization"
    )


def state_summary_for_demo(state: ContentCreationState) -> Dict[str, Any]:
    """Create a demo-friendly summary of the current state"""
    return {
        "📝 Topic": state.topic,
        "🎯 Style": state.style,
        "👥 Audience": state.target_audience,
        "🔄 Progress": f"{len(state.agent_history)}/7 agents completed",
        "📊 Quality Score": f"{state.quality_score}/10",
        "✅ Ready": "Yes" if state.is_content_ready() else "No",
        "🔄 Needs Revision": "Yes" if state.needs_revision() else "No"
    }