"""
LangGraph Workflow Builder for Multi-Agent Content Creation

This module builds the LangGraph workflow that orchestrates specialized agents
for content creation. It demonstrates graph-based workflow management with
conditional routing, state management, and revision loops.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from workflow.state_schema import ContentCreationState
from agents.planner import planner_node
from agents.research_planner import research_planner_node
from agents.search_executor import search_executor_node
from agents.script_generator import script_generator_node
from agents.reflection import reflection_node
from agents.hashtag_generator import hashtag_generator_node
from agents.cta_generator import cta_generator_node
from utils.display import demo_print, workflow_step, section_header


def should_revise(state: ContentCreationState) -> str:
    if state.needs_revision():
        demo_print("🔄 Quality score below threshold - triggering revision", "yellow")
        return "research_planner"  # Loop back for revision
    else:
        demo_print("✅ Quality approved - proceeding to final steps", "green")
        return "hashtag_generator"


def build_content_creation_graph() -> StateGraph:
    workflow = StateGraph(ContentCreationState)
    
    # Add nodes (each represents a specialized agent)
    workflow.add_node("planner", planner_node)
    workflow.add_node("research_planner", research_planner_node) 
    workflow.add_node("search_executor", search_executor_node)
    workflow.add_node("script_generator", script_generator_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("hashtag_generator", hashtag_generator_node)
    workflow.add_node("cta_generator", cta_generator_node)
    
    # Define the workflow edges (agent collaboration flow)
    workflow.add_edge("planner", "research_planner")
    workflow.add_edge("research_planner", "search_executor") 
    workflow.add_edge("search_executor", "script_generator")
    workflow.add_edge("script_generator", "reflection")
    
    # Conditional edge - LangGraph's conditional routing capability
    workflow.add_conditional_edges(
        "reflection",
        should_revise,
        {
            "research_planner": "research_planner",  # Revision loop
            "hashtag_generator": "hashtag_generator"  # Continue to completion
        }
    )
    
    workflow.add_edge("hashtag_generator", "cta_generator")
    workflow.add_edge("cta_generator", END)
    
    # Set entry point
    workflow.set_entry_point("planner")
    
    return workflow


def execute_content_creation_demo(topic: str, style: str = "Educational") -> ContentCreationState:
    section_header("🚀 Multi-Agent Content Creation Demo", "bright_blue")
    
    # Build the workflow graph
    demo_print("🏗️  Building LangGraph workflow...", "cyan")
    workflow_graph = build_content_creation_graph()
    
    # Compile the workflow
    demo_print("⚙️  Compiling workflow graph...", "cyan")  
    compiled_workflow = workflow_graph.compile()
    
    # Create initial state
    demo_print(f"📝 Initializing workflow for topic: '{topic}'", "blue")
    initial_state = ContentCreationState(
        topic=topic,
        style=style,
        current_step="workflow_initialized"
    )
    
    section_header("🎭 Agent Collaboration in Action", "magenta")
    
    # Execute the workflow
    try:
        demo_print("▶️  Starting multi-agent workflow execution...", "green", bold=True)
        
        # The workflow will automatically coordinate all agents
        result = compiled_workflow.invoke(initial_state)
        
        # Convert result back to ContentCreationState if needed
        if isinstance(result, dict):
            final_state = ContentCreationState(**result)
        else:
            final_state = result
        
        section_header("🎉 Workflow Execution Complete", "bright_green")
        
        return final_state
        
    except Exception as e:
        demo_print(f"❌ Error during workflow execution: {str(e)}", "red")
        raise

def get_workflow_summary() -> Dict[str, Any]:
    """
    Get a summary of the workflow architecture for presentation.
    """
    return {
        "framework_integration": {
            "primary": "LangGraph - Workflow orchestration and state management",
            "secondary": "CrewAI - Role-based agent collaboration patterns",
            "benefit": "Best of both worlds - structured workflows + specialized roles"
        },
        "agent_count": 7,
        "workflow_features": [
            "Conditional routing based on quality assessment",
            "Persistent state management across all agents",
            "Automatic revision loops for quality improvement",
            "Modular architecture for easy agent addition"
        ],
        "crewai_benefits": [
            "Clear role definitions and responsibilities",
            "Specialized system prompts for each role",
            "Professional team collaboration patterns",
            "Goal-oriented agent design"
        ],
        "business_value": [
            "Scalable content creation process",
            "Consistent quality with built-in review",
            "Reduced human workload and faster execution",
            "Easily adaptable to different content types"
        ]
    }


if __name__ == "__main__":
    # Demo the workflow building process
    demonstrate_workflow_features()
    
    summary = get_workflow_summary()
    section_header("📊 Workflow Architecture Summary", "cyan")
    print(f"Integration: {summary['framework_integration']['benefit']}")
    print(f"Agent Count: {summary['agent_count']}")
    print(f"Key Features: {len(summary['workflow_features'])} workflow capabilities")
    print(f"CrewAI Benefits: {len(summary['crewai_benefits'])} collaboration enhancements")