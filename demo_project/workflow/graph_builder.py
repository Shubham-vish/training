"""
LangGraph Workflow Builder for Multi-Agent Content Creation

This module builds the LangGraph workflow that orchestrates specialized agents
for content creation. It demonstrates graph-based workflow management with
conditional routing, state management, and revision loops.
"""
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


def execute_content_creation(topic: str, style: str = "Educational") -> ContentCreationState:
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
    
if __name__ == "__main__":
    workflow_graph = build_content_creation_graph()
    compiled_workflow = workflow_graph.compile()
    
    
    from langchain_core.runnables.graph import MermaidDrawMethod
    from IPython.display import display, HTML, Image

    display(
        Image(
            compiled_workflow.get_graph().draw_mermaid_png(
                draw_method=MermaidDrawMethod.API,
            )
        )
    )

    # print(compiled_workflow.get_graph().draw_mermaid())
    
    
    topic = "The Future of Artificial Intelligence in Everyday Life"
    style = "Educational"
    
    initial_state = ContentCreationState(
        topic=topic,
        style=style,
        current_step="workflow_initialized"
    )
    
    result = compiled_workflow.invoke(initial_state)