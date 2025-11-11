"""
LangGraph Workflow Builder with CrewAI Integration

This module builds the LangGraph workflow that orchestrates CrewAI role-based agents
for content creation. It demonstrates the power of combining workflow orchestration
with role-based collaboration patterns.
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from workflow.state_schema import ContentCreationState
from agents.langgraph_nodes import (
    planner_node,
    research_planner_node,
    search_executor_node,
    script_generator_node,
    reflection_node,
    hashtag_generator_node,
    cta_generator_node
)
from utils.display import demo_print, workflow_step, section_header


def should_revise(state: ContentCreationState) -> str:
    """
    Conditional edge function to decide workflow routing based on quality assessment.
    
    This demonstrates LangGraph's conditional routing capability - one of its key
    advantages over simple linear agent chains.
    """
    if state.needs_revision():
        demo_print("🔄 Quality score below threshold - triggering revision", "yellow")
        return "research_planner"  # Loop back for revision
    else:
        demo_print("✅ Quality approved - proceeding to final steps", "green")
        return "hashtag_generator"


def build_content_creation_graph() -> StateGraph:
    """
    Build the complete LangGraph workflow with CrewAI role integration.
    
    This demonstrates how LangGraph provides workflow orchestration while
    CrewAI patterns provide role-based collaboration structure.
    """
    
    # Initialize the StateGraph with our custom state
    workflow = StateGraph(ContentCreationState)
    
    # Add nodes (each represents a CrewAI agent role)
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
    """
    Execute the complete content creation workflow for demo purposes.
    
    This function orchestrates the entire demo, showing the integration of
    CrewAI role patterns with LangGraph workflow management.
    """
    
    section_header("🚀 Multi-Agent Content Creation Demo", "bright_blue")
    
    # Build the workflow graph
    demo_print("🏗️  Building LangGraph workflow with CrewAI role integration...", "cyan")
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


def demonstrate_workflow_features():
    """
    Demonstrate key LangGraph features for educational purposes.
    """
    
    section_header("🔍 LangGraph Features Demonstration", "blue")
    
    features = [
        "🔄 State Management - Persistent state across all agents",
        "🎯 Conditional Routing - Quality-based revision loops", 
        "🎭 Node-Based Architecture - Each agent as a specialized node",
        "📊 Execution Tracking - Built-in monitoring and history",
        "⚡ Error Handling - Graceful failure recovery",
        "🔧 Modularity - Easy to add/modify agents"
    ]
    
    for i, feature in enumerate(features, 1):
        workflow_step(i, feature.split(" - ")[0][2:], feature.split(" - ")[1])
        

def demonstrate_crewai_integration():
    """
    Demonstrate how CrewAI concepts enhance the workflow.
    """
    
    section_header("🎭 CrewAI Integration Benefits", "magenta")
    
    benefits = [
        "👨‍💼 Role-Based Design - Each agent has clear responsibilities and expertise",
        "🤝 Collaboration Patterns - Agents work together like a professional team", 
        "📋 Task Delegation - Work flows naturally between specialized roles",
        "🎯 Goal-Oriented - Each role has specific objectives and success metrics",
        "🧠 Specialized Prompts - Role-specific system prompts for better outputs",
        "📈 Quality Assurance - Built-in review and improvement cycles"
    ]
    
    for i, benefit in enumerate(benefits, 1):
        workflow_step(i, benefit.split(" - ")[0][2:], benefit.split(" - ")[1])


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
    demonstrate_crewai_integration()
    
    # Show workflow summary
    summary = get_workflow_summary()
    section_header("📊 Workflow Architecture Summary", "cyan")
    print(f"Integration: {summary['framework_integration']['benefit']}")
    print(f"Agent Count: {summary['agent_count']}")
    print(f"Key Features: {len(summary['workflow_features'])} workflow capabilities")
    print(f"CrewAI Benefits: {len(summary['crewai_benefits'])} collaboration enhancements")