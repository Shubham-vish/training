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
    
    # Create panels for each output with colorful styling
    if script:
        console.print(Panel(
            script, 
            title="[bold green]📝 Content Script[/bold green]", 
            border_style="green",
            style="green",
            padding=(1, 2)
        ))
    
    if hashtags:
        hashtag_text = " ".join(hashtags) if isinstance(hashtags, list) else str(hashtags)
        console.print(Panel(
            hashtag_text, 
            title="[bold blue]🏷️ Hashtags[/bold blue]", 
            border_style="blue",
            style="blue",
            padding=(1, 2)
        ))
    
    if cta:
        console.print(Panel(
            cta, 
            title="[bold magenta]🚀 Call-to-Action[/bold magenta]", 
            border_style="magenta",
            style="magenta",
            padding=(1, 2)
        ))
        
    # Performance summary
    total_time = sum(execution_time.values()) if execution_time else 0
    console.print(f"\n⚡ Total Execution Time: {total_time:.2f} seconds", style="bold yellow")
    console.print(f"🎯 Final Quality Score: {quality_score:.1f}/10", style="bold green")
