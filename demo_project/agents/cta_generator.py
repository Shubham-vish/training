"""
CTA Generator Agent - Conversion Optimization Specialist
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from workflow.state_schema import ContentCreationState
from agents.agent_prompts import get_agent_system_prompt
from utils.display import demo_print, agent_thinking, agent_output
from utils.llm_client import get_llm_client


class CTAOutput(BaseModel):
    """Structured output for CTA generation"""
    cta: str = Field(description="Complete call-to-action with emojis and action items")
    engagement_hooks: List[str] = Field(description="5 specific engagement hooks")


def _display_cta_summary(hooks_count: int, execution_time: float):
    """Display CTA summary"""
    agent_output(f"✅ Call-to-action created")
    demo_print(f"   Engagement hooks: {hooks_count} conversion strategies", "green")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")


def cta_generator_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Conversion Optimization Specialist Agent - Node 7 (Final)
    
    Creates compelling calls-to-action that drive engagement and conversions.
    """
    start_time = time.time()
    llm_client = get_llm_client()
    
    demo_print(f"🎭 CTA Generator is working...", "blue")
    agent_thinking("Crafting compelling calls-to-action for maximum conversion...")
    
    system_prompt = get_agent_system_prompt("cta_generator")
    user_prompt = f"""
Create compelling call-to-action for short-form educational video:

Topic: {state.topic}
Script: {state.script}

Generate 2-3 CTA variations optimized for Reels/Shorts engagement."""
    
    result = llm_client.generate_structured(
        system_prompt,
        user_prompt,
        CTAOutput,
        "cta_generator",
        state.topic,
        temperature=0.7
    )
    
    execution_time = time.time() - start_time
    
    updates = {
        "cta": result.cta,
        "engagement_hooks": result.engagement_hooks,
        "current_step": "content_creation_complete"
    }
    
    state.add_agent_execution("cta_generator", "CTA Generator", updates, execution_time)
    
    _display_cta_summary(len(result.engagement_hooks), execution_time)
    
    return updates


if __name__ == "__main__":
    """Test this node independently"""
    from workflow.state_schema import ContentCreationState
    
    print("\n" + "="*70)
    print("🧪 TESTING CTA GENERATOR NODE")
    print("="*70 + "\n")
    
    # Create test state
    state = ContentCreationState(
        topic="Mental Health in Tech",
        style="Empathetic and actionable"
    )
    
    state.script = """
    📱 2025 Marketing Trends You Can't Ignore
    
    1. AI-powered personalization is standard, not premium
    2. Short-form video dominates (TikTok, Reels, Shorts)
    3. Privacy-first marketing builds trust
    4. Community > Followers
    5. Interactive content wins engagement
    
    Adapt or fall behind! 🚀
    """
    
    # Execute node
    print("▶️  Executing cta_generator_node...\n")
    result = cta_generator_node(state)
    
    # Apply updates
    for key, value in result.items():
        setattr(state, key, value)
    
    # Display result
    print("\n" + "="*70)
    print("📣 CALL-TO-ACTION")
    print("="*70)
    print(state.cta)
    print("\n" + "="*70)
    print("🎯 ENGAGEMENT HOOKS")
    print("="*70)
    for i, hook in enumerate(state.engagement_hooks, 1):
        print(f"{i}. {hook}")
    print("="*70)
    print(f"✅ Success! Generated CTA with {len(state.engagement_hooks)} hooks")
    print("="*70 + "\n")