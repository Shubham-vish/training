"""
Display utilities for demo visualization

Provides colorful, engaging output for the live demonstration.
"""

import time
import sys
from typing import Any, Dict, List
from colorama import init, Fore, Back, Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Initialize colorama for cross-platform color support
init()

# Rich console for enhanced output
console = Console()


def demo_print(text: str, color: str = "white", bold: bool = False):
    """Print colored text for demo visualization"""
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "blue": Fore.BLUE,
        "yellow": Fore.YELLOW,
        "cyan": Fore.CYAN,
        "magenta": Fore.MAGENTA,
        "white": Fore.WHITE,
        "bright_green": Fore.LIGHTGREEN_EX,
        "bright_blue": Fore.LIGHTBLUE_EX,
    }
    
    style = Style.BRIGHT if bold else ""
    color_code = color_map.get(color, Fore.WHITE)
    
    print(f"{style}{color_code}{text}{Style.RESET_ALL}")


def agent_thinking(message: str, duration: float = 0.5):
    """Simulate agent thinking with animated dots"""
    print(f"  🤔 {message}", end="", flush=True)
    for _ in range(3):
        time.sleep(duration / 3)
        print(".", end="", flush=True)
    print()  # New line


def agent_output(message: str):
    """Display agent output with formatting"""
    demo_print(f"  {message}", "bright_green")


def section_header(title: str, color: str = "blue"):
    """Display section header with formatting"""
    print("\n" + "=" * 60)
    demo_print(f"🎯 {title.upper()}", color, bold=True)
    print("=" * 60)


def workflow_step(step_number: int, step_name: str, description: str):
    """Display workflow step information"""
    demo_print(f"\n📍 Step {step_number}: {step_name}", "cyan", bold=True)
    demo_print(f"   {description}", "white")


def display_state_summary(state):
    """Display current state summary in a formatted table"""
    console.print("\n📊 Current Workflow State", style="bold blue")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    # Handle both ContentCreationState objects and dicts
    if hasattr(state, 'get_workflow_progress'):
        progress = state.get_workflow_progress()
        table.add_row("Progress", f"{progress['completed_agents']}/{progress['total_agents']} agents ({progress['progress_percentage']:.1f}%)")
        table.add_row("Current Step", progress['current_step'])
        table.add_row("Quality Score", f"{progress['quality_score']}/10")
        table.add_row("Revision #", str(progress['revision_number']))
        table.add_row("Ready", "✅ Yes" if state.is_content_ready() else "⏳ In Progress")
    else:
        # Handle dict state object
        agent_count = len(state.get('agent_history', []))
        table.add_row("Progress", f"{agent_count}/7 agents completed")
        table.add_row("Current Step", state.get('current_step', 'Unknown'))
        table.add_row("Quality Score", f"{state.get('quality_score', 0)}/10")
        table.add_row("Revision #", str(state.get('revision_number', 0)))
        table.add_row("Ready", "✅ Yes" if state.get('script') and state.get('hashtags') and state.get('cta') else "⏳ In Progress")
    
    console.print(table)


def display_agent_roles():
    """Display all agent roles in a formatted table"""
    console.print("\n🎭 Content Creation Agent Roles (CrewAI Integration)", style="bold blue")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Agent Role", style="cyan")
    table.add_column("LangGraph Node", style="yellow")
    table.add_column("Specialization", style="green")
    
    roles_data = [
        ("Content Strategy Manager", "planner", "Strategy & Planning"),
        ("Research Strategy Specialist", "research_planner", "Research Design"),
        ("Information Gathering Analyst", "search_executor", "Data Collection"),
        ("Content Creation Writer", "script_generator", "Content Writing"),
        ("Quality Assurance Specialist", "reflection", "Quality Review"),
        ("SEO & Hashtag Specialist", "hashtag_generator", "SEO Optimization"),
        ("Marketing & CTA Specialist", "cta_generator", "Conversion Optimization")
    ]
    
    for role, node, specialization in roles_data:
        table.add_row(role, node, specialization)
    
    console.print(table)


def display_workflow_diagram():
    """Display ASCII workflow diagram"""
    diagram = """
    ┌─────────────────────────────────────────────────────────────┐
    │                   🏭 CONTENT CREATION WORKFLOW              │
    │                     (CrewAI + LangGraph)                    │
    └─────────────────────────────────────────────────────────────┘
    
    📝 Topic Input
          ↓
    ┌─────────────────┐    🎭 Content Strategy Manager
    │   1. PLANNER    │ ←  Creates outline & strategy
    └─────────┬───────┘    
              ↓
    ┌─────────────────┐    🎭 Research Strategy Specialist  
    │ 2. RESEARCH     │ ←  Designs research approach
    │    PLANNER      │
    └─────────┬───────┘
              ↓
    ┌─────────────────┐    🎭 Information Gathering Analyst
    │ 3. SEARCH       │ ←  Collects & analyzes data
    │    EXECUTOR     │
    └─────────┬───────┘
              ↓
    ┌─────────────────┐    🎭 Content Creation Writer
    │ 4. SCRIPT       │ ←  Transforms research into content
    │    GENERATOR    │
    └─────────┬───────┘
              ↓
    ┌─────────────────┐    🎭 Quality Assurance Specialist
    │ 5. REFLECTION   │ ←  Reviews quality & suggests improvements
    └─────────┬───────┘
              ↓
         ⚡ Decision Point
              ↓
    ┌─────────────────┐    🎭 SEO & Hashtag Specialist
    │ 6. HASHTAG      │ ←  Optimizes for discoverability  
    │    GENERATOR    │
    └─────────┬───────┘
              ↓
    ┌─────────────────┐    🎭 Marketing & CTA Specialist
    │ 7. CTA          │ ←  Creates compelling calls-to-action
    │    GENERATOR    │
    └─────────┬───────┘
              ↓
         🎉 FINAL CONTENT
    """
    
    print("\n")
    demo_print(diagram, "cyan")


def display_final_output(state):
    """Display the final content creation output"""
    console.print("\n🎉 FINAL CONTENT OUTPUT", style="bold green")
    
    # Handle both ContentCreationState objects and dicts
    if hasattr(state, 'script'):
        # ContentCreationState object
        script = state.script
        hashtags = state.hashtags
        cta = state.cta
        quality_score = state.quality_score
        execution_time = state.execution_time
    else:
        # Dict object
        script = state.get('script', '')
        hashtags = state.get('hashtags', [])
        cta = state.get('cta', '')
        quality_score = state.get('quality_score', 0)
        execution_time = state.get('execution_time', {})
    
    # Create panels for each output
    if script:
        console.print(Panel(script, title="📝 Content Script", border_style="green"))
    
    if hashtags:
        hashtag_text = " ".join(hashtags) if isinstance(hashtags, list) else str(hashtags)
        console.print(Panel(hashtag_text, title="🏷️ Hashtags", border_style="blue"))
    
    if cta:
        console.print(Panel(cta, title="🚀 Call-to-Action", border_style="magenta"))
        
    # Performance summary
    total_time = sum(execution_time.values()) if execution_time else 0
    console.print(f"\n⚡ Total Execution Time: {total_time:.2f} seconds", style="bold yellow")
    console.print(f"🎯 Final Quality Score: {quality_score:.1f}/10", style="bold green")


def demo_introduction():
    """Display demo introduction"""
    intro_text = """
    🚀 MULTI-AGENT CONTENT CREATION SYSTEM
    
    🎭 CrewAI Role-Based Collaboration + 🔄 LangGraph Workflow Orchestration
    
    Today we'll see how 7 specialized AI agents work together like a professional
    content team to create engaging social media content from just a topic!
    
    Each agent has a specific CrewAI role (like Content Manager, Research Specialist)
    and operates within a LangGraph workflow for perfect coordination.
    """
    
    console.print(Panel(intro_text, title="🎬 Live Demo", border_style="bright_blue"))


def framework_comparison():
    """Display framework comparison table"""
    console.print("\n🔍 Multi-Agent Framework Comparison", style="bold blue")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Framework", style="cyan")
    table.add_column("Strengths", style="green")
    table.add_column("Best For", style="yellow")
    
    table.add_row(
        "CrewAI",
        "Role-based collaboration\nTask delegation\nHierarchical coordination",
        "Structured teams\nClear responsibilities\nRole specialization"
    )
    
    table.add_row(
        "LangGraph", 
        "Workflow orchestration\nState management\nConditional routing",
        "Complex workflows\nState persistence\nError handling"
    )
    
    table.add_row(
        "AutoGen",
        "Conversation-driven\nConsensus building\nGroup discussions",
        "Collaborative decisions\nIterative refinement\nDebate scenarios"
    )
    
    console.print(table)


def pause_for_audience():
    """Pause for audience interaction"""
    demo_print("\n⏸️  [Pausing for questions and audience engagement]", "yellow", bold=True)
    print("   💭 What questions do you have about what we just saw?")
    print("   🤝 How does this compare to your current content creation process?")
    time.sleep(2)  # Brief pause for effect