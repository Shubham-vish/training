"""
Reflection Agent - Content Quality Reviewer
"""

import time
from typing import Dict, Any
from pydantic import BaseModel, Field
from workflow.state_schema import ContentCreationState
from agents.agent_prompts import get_agent_system_prompt
from utils.display import demo_print, agent_thinking, agent_output
from utils.llm_client import get_llm_client
from rich.console import Console
from rich.table import Table

console = Console()


class QualityAssessment(BaseModel):
    """Structured output for quality assessment"""
    engagement: float = Field(description="Engagement score 1-10")
    accuracy: float = Field(description="Accuracy score 1-10")
    structure: float = Field(description="Structure score 1-10")
    actionability: float = Field(description="Actionability score 1-10")
    audience_fit: float = Field(description="Audience fit score 1-10")
    critique: str = Field(description="Detailed critique with strengths and improvements")


def _display_quality_table(quality_factors: Dict[str, float], quality_score: float, execution_time: float):
    """Display quality assessment table with rich formatting"""
    table = Table(
        show_header=True,
        header_style="bold magenta on black",
        border_style="cyan",
        title="[bold cyan]Quality Assessment[/bold cyan]",
        title_style="bold cyan"
    )
    table.add_column("Quality Factor", style="cyan bold", width=20)
    table.add_column("Score", justify="center", style="yellow bold", width=10)
    table.add_column("Status", justify="center", width=10)
    
    for factor, score in quality_factors.items():
        status = "[green]✅[/green]" if score >= 8.0 else "[yellow]⚠️[/yellow]" if score >= 7.0 else "[red]❌[/red]"
        score_style = "green" if score >= 8.0 else "yellow" if score >= 7.0 else "red"
        table.add_row(
            factor.replace('_', ' ').title(),
            f"[{score_style}]{score}/10[/{score_style}]",
            status
        )
    
    console.print(table)
    
    decision = "✅ APPROVED - Proceeding to final steps" if quality_score >= 7.0 else "⚠️ NEEDS REVISION - Looping back"
    demo_print(f"\n   Decision: {decision}", "green" if quality_score >= 7.0 else "red")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")


def reflection_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Content Quality Reviewer Agent - Node 5 (Critical Decision Point)
    
    Evaluates content quality, accuracy, and effectiveness.
    """
    start_time = time.time()
    llm_client = get_llm_client()
    
    demo_print(f"🎭 Reflection is working...", "blue")
    agent_thinking("Evaluating content quality and providing improvement recommendations...")
    
    # Get quality assessment with structured output
    system_prompt = get_agent_system_prompt("reflection")
    user_prompt = f"""
Evaluate this content for quality and effectiveness:

Topic: {state.topic}
Style: {state.style}
Content Script: {state.script}

Provide scores (1-10) for: engagement, accuracy, structure, actionability, audience_fit
Include detailed critique with strengths and improvements."""
    
    assessment = llm_client.generate_structured(
        system_prompt,
        user_prompt,
        QualityAssessment,
        "reflection",
        state.topic,
        temperature=0.3
    )
    
    # Calculate overall quality score
    quality_factors = {
        "engagement": assessment.engagement,
        "accuracy": assessment.accuracy,
        "structure": assessment.structure,
        "actionability": assessment.actionability,
        "audience_fit": assessment.audience_fit
    }
    quality_score = sum(quality_factors.values()) / len(quality_factors)
    
    execution_time = time.time() - start_time
    
    updates = {
        "quality_score": quality_score,
        "critique": assessment.critique,
        "improvement_suggestions": [],
        "current_step": "quality_review_complete"
    }
    
    state.add_agent_execution("reflection", "Reflection", updates, execution_time)
    
    agent_output(f"✅ Quality assessment completed")
    demo_print(f"   Overall Score: {quality_score:.1f}/10", "green" if quality_score >= 7.0 else "yellow")
    
    _display_quality_table(quality_factors, quality_score, execution_time)
    
    return updates


if __name__ == "__main__":
    """Test this node independently"""
    from workflow.state_schema import ContentCreationState
    
    print("\n" + "="*70)
    print("🧪 TESTING REFLECTION NODE")
    print("="*70 + "\n")
    
    # Create test state
    state = ContentCreationState(
        topic="Remote Work Productivity",
        style="Professional and practical",
    )
    
    state.script = """
    🏡 Remote Work: The New Reality
    
    Did you know 73% of teams will have remote workers by 2028?
    
    The challenge? Maintaining productivity and collaboration without the office.
    
    The solution: Smart tools, clear communication, and trust-based culture.
    Companies with strong remote policies see 25% higher productivity.
    
    Example: GitLab, 100% remote with 1300+ employees, built a $1B+ company.
    
    💡 What's your #1 remote work tip? Share below!
    """
    
    state.content_outline = "Structure: Hook → Problem → Solution → Proof → CTA"

    # Execute node
    print("▶️  Executing reflection_node...\n")
    result = reflection_node(state)
    
    # Apply updates
    for key, value in result.items():
        setattr(state, key, value)
    
    # Display result
    print("\n" + "="*70)
    print("📊 QUALITY ASSESSMENT RESULTS")
    print("="*70)
    print(f"Overall Score: {state.quality_score:.1f}/10")
    print(f"\nCritique:\n{state.critique}")
    print("="*70)
    print(f"✅ Success! Quality score: {state.quality_score:.1f}/10")
    print("="*70 + "\n")
