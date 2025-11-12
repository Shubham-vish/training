"""
Hashtag Generator Agent - Social Media Optimization Specialist
"""

import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from workflow.state_schema import ContentCreationState
from agents.agent_prompts import get_agent_system_prompt
from utils.display import demo_print, agent_thinking, agent_output
from utils.llm_client import get_llm_client
from rich.console import Console
from rich.panel import Panel

console = Console()


class HashtagOutput(BaseModel):
    """Structured output for hashtag generation"""
    hashtags: List[str] = Field(description="List of 8-10 strategic hashtags with # symbol")
    seo_keywords: List[str] = Field(description="5 SEO keywords for content optimization")
    rationale: str = Field(description="Brief explanation of hashtag strategy")


def _display_hashtags(hashtags: List[str], seo_keywords: List[str], execution_time: float):
    """Display generated hashtags in a styled panel"""
    agent_output(f"✅ SEO optimization completed")
    demo_print(f"   Hashtags: {len(hashtags)} strategic tags generated", "green")
    
    # Display hashtags in a panel
    hashtag_text = " ".join(hashtags)
    panel = Panel(
        hashtag_text,
        title="[bold blue]🏷️ Generated Hashtags[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )
    console.print(panel)
    
    # Display SEO keywords
    demo_print(f"   SEO Keywords: {', '.join(seo_keywords)}", "cyan")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")


def hashtag_generator_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Social Media Optimization Specialist Agent - Node 6
    
    Optimizes content for discoverability and platform-specific engagement.
    """
    start_time = time.time()
    llm_client = get_llm_client()
    
    demo_print(f"🎭 Hashtag Generator is working...", "blue")
    agent_thinking("Optimizing content for maximum discoverability and engagement...")
    
    # Get hashtags with structured output
    system_prompt = get_agent_system_prompt("hashtag_generator")
    user_prompt = f"""
Create strategic hashtags for this content:

Topic: {state.topic}
Content Script: {state.script}

Provide 8-10 hashtags (with # symbol), 5 SEO keywords, and brief rationale."""
    
    result = llm_client.generate_structured(
        system_prompt,
        user_prompt,
        HashtagOutput,
        "hashtag_generator",
        state.topic,
        temperature=0.6
    )
    
    execution_time = time.time() - start_time
    
    updates = {
        "hashtags": result.hashtags[:10],  # Limit to 10
        "seo_keywords": result.seo_keywords,
        "current_step": "seo_optimization_complete"
    }
    
    state.add_agent_execution("hashtag_generator", "Hashtag Generator", updates, execution_time)
    
    _display_hashtags(result.hashtags, result.seo_keywords, execution_time)
    
    return updates


if __name__ == "__main__":
    """Test this node independently"""
    from workflow.state_schema import ContentCreationState
    
    print("\n" + "="*70)
    print("🧪 TESTING HASHTAG GENERATOR NODE")
    print("="*70 + "\n")
    
    # Create test state
    state = ContentCreationState(
        topic="Sustainable Technology",
        style="Inspiring and eco-conscious",
    )
    
    state.script = """
    🌱 Tech + Sustainability = Future
    
    Green tech isn't just good for the planet—it's good for business.
    Companies investing in sustainable tech see 2x customer loyalty.
    
    From solar-powered data centers to biodegradable electronics,
    innovation is making tech greener every day.
    
    Join the movement! 🌍
    """
    
    # Execute node
    print("▶️  Executing hashtag_generator_node...\n")
    result = hashtag_generator_node(state)
    
    # Apply updates
    for key, value in result.items():
        setattr(state, key, value)
    
    # Display result
    print("\n" + "="*70)
    print("🏷️  GENERATED HASHTAGS")
    print("="*70)
    print(" ".join(state.hashtags))
    print("\n" + "="*70)
    print("🔑 SEO KEYWORDS")
    print("="*70)
    print(", ".join(state.seo_keywords))
    print("="*70)
    print(f"✅ Success! Generated {len(state.hashtags)} hashtags")
    print("="*70 + "\n")
