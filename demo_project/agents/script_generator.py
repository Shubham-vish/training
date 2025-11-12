"""
Script Generator Agent - Content Writer
"""

import time
from typing import Dict, Any
from workflow.state_schema import ContentCreationState
from agents.agent_prompts import get_agent_system_prompt
from utils.display import demo_print, agent_thinking, agent_output
from utils.llm_client import get_llm_client
from rich.console import Console
from rich.panel import Panel

console = Console()


def _display_script_summary(word_count: int, execution_time: float):
    """Display script summary"""
    agent_output(f"✅ Content script created")
    demo_print(f"   Word count: ~{word_count} words", "green")
    demo_print(f"   Structure: Hook → Problem → Solution → Proof → CTA", "green")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")


def script_generator_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Content Writer Agent - Node 4
    
    Transforms research and strategy into engaging, well-structured content.
    """
    start_time = time.time()
    llm_client = get_llm_client()
    
    demo_print(f"🎭 Script Generator is working...", "blue")
    agent_thinking("Crafting engaging content based on strategy and research...")
    
    system_prompt = get_agent_system_prompt("script_generator")
    user_prompt = f"""
    
Create engaging content for: "
{state.topic}"

Content Strategy: {state.content_outline}
Research Data: {state.research_data}

Requirements:
- Style: {state.style}
- Structure: Hook → Problem → Solution → Proof → CTA
- Integrate research statistics"""
    
    script = llm_client.generate_response(
        system_prompt,
        user_prompt,
        "script_generator",
        state.topic,
        temperature=0.8
    )
    
    execution_time = time.time() - start_time
    word_count = len(script.split())
    
    updates = {
        "script": script,
        "content_structure": {},
        "current_step": "script_complete"
    }
    
    state.add_agent_execution("script_generator", "Script Generator", updates, execution_time)
    
    _display_script_summary(word_count, execution_time)
    
    return updates


if __name__ == "__main__":
    """Test this node independently"""
    from workflow.state_schema import ContentCreationState
    
    print("\n" + "="*70)
    print("🧪 TESTING SCRIPT GENERATOR NODE")
    print("="*70 + "\n")
    
    # Create test state
    state = ContentCreationState(
        topic="Artificial Intelligence",
        style="Professional and engaging",
    )
    
    # Set required fields
    state.content_outline = """
    Goal 1: Educate about AI trends and impact
    Goal 2: Provide actionable insights
    Goal 3: Drive engagement and discussion
    
    Structure:
    - Hook: Surprising AI statistic
    - Problem: Current AI challenges
    - Solution: Benefits of AI adoption
    - Proof: Real-world success stories
    - CTA: Encourage conversation
    """
    
    state.research_data = """
    Statistics:
    - AI market projected to reach $190B by 2025
    - 77% of companies using or exploring AI
    - 40% productivity increase with AI tools
    
    Trends:
    - Generative AI transforming content creation
    - AI-powered automation in business processes
    - Ethical AI gaining importance
    
    Challenges:
    - Skills gap in AI expertise
    - Data privacy concerns
    - Integration complexity
    """

    
    # Execute node
    print("▶️  Executing script_generator_node...\n")
    result = script_generator_node(state)
    
    # Apply updates
    for key, value in result.items():
        setattr(state, key, value)
    
    # Display result
    print("\n" + "="*70)
    print("📄 GENERATED SCRIPT")
    print("="*70)
    print(state.script)
    print("="*70)
    print(f"✅ Success! Generated {len(state.script.split())} words")
    print("="*70 + "\n")
