"""Research critique agent node."""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from agents.content_generation.agent_nodes.shared import Queries
from typing import Optional

RESEARCH_CRITIQUE_PROMPT = """
You are a researcher charged with providing information that can be used when making any requested revisions.

Critique:
__state__{critique}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Generate a list of search queries that will gather any relevant information. Only generate 3 queries max.

If global custom instructions are provided, ensure your research queries help address the critique while staying aligned with those specific requirements.
"""

def research_critique_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
) -> dict:
    """Research based on critiques
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
    """
    ctx.start_conversation("🔄 Starting critique-based research...")
    
    try:
        critique = ctx.state.get('critique', '')
        ctx.log_progress("🔍 Analyzing critique for research needs...")

        prompt_template = ctx.prompts.get('research_critique', RESEARCH_CRITIQUE_PROMPT)
        base_prompt = replace_state_placeholders(prompt_template, ctx.state)
        
        if custom_user_message:
            base_prompt += f"\n\nAdditional user instructions: {custom_user_message}"

        ctx.log_progress("🤔 Generating research queries...")
        queries_raw = ctx.model.with_structured_output(Queries, include_raw=True).invoke([
            SystemMessage(content=base_prompt),
            HumanMessage(content=critique)
        ])

        # Cast to dict and extract values
        result_dict = dict(queries_raw)
        queries = result_dict['parsed'].queries
        token_usage = result_dict['raw'].response_metadata['token_usage']

        result = {
            "queries": queries,
            "lnode": "research_critique",
            "token_usage": token_usage
        }

        ctx.finalize_conversation({
            "summary": "Generated research critique",
            "critique": critique,
            "token_usage": token_usage,
            "node": "research_critique"
        })

        return result
        
    except Exception as e:
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "research_critique"
        })
        raise 