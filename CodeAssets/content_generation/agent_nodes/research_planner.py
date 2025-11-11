"""Research planner agent node."""

from langchain_core.messages import SystemMessage, HumanMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from agents.content_generation.agent_nodes.shared import Queries
from typing import Optional

RESEARCH_PLANNER_PROMPT = """
You are a researcher charged with providing information that can be used when writing a short-form video script. 

Topic: __state__{topic}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Generate a list of search queries that will gather relevant information about the topic. Only generate 3 queries max.

If global custom instructions are provided, tailor your research queries to align with those specific requirements or preferences.
"""

def research_plan_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
) -> dict:
    """Generate research queries based on the plan
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
    """
    ctx.start_conversation("🔄 Starting research planning...")

    try:
        topic = ctx.state.get('topic', 'default topic')
        ctx.log_progress("🔍 Analyzing topic for research queries...")

        prompt_template = ctx.prompts.get('research_planner', RESEARCH_PLANNER_PROMPT)
        base_prompt = replace_state_placeholders(prompt_template, ctx.state)
        
        messages = [
            SystemMessage(content=base_prompt),
            HumanMessage(content=topic)
        ]

        if custom_user_message:
            messages.append(HumanMessage(content=f"Additional user instructions: {custom_user_message}"))

        queries_raw = ctx.model.with_structured_output(Queries, include_raw=True).invoke(messages)


        # Cast to dict and extract values
        result_dict = dict(queries_raw)
        queries = result_dict['parsed'].queries
        token_usage = result_dict['raw'].response_metadata['token_usage']

        result = {
            "queries": queries,
            "lnode": "research_plan",
            "token_usage": token_usage
        }

        ctx.finalize_conversation({
            "summary": "✅ Research queries generated",
            "queries": queries,
            "token_usage": token_usage,
            "node": "research_planner"
        })

        return result
        
    except Exception as e:
        ctx.add_step(
            title="❌ Error in research planning",
            status="failed",
            details={
                "error": str(e),
                "error_type": type(e).__name__
            }
        )
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "research_planner"
        })
        raise 