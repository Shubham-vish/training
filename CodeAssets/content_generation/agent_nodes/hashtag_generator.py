"""Hashtag generator agent node."""

from langchain_core.messages import SystemMessage, HumanMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from typing import Optional

HASHTAG_GENERATOR_PROMPT = """
You are a hashtag generator tasked with creating relevant hashtags for a short-form video.

Topic: __state__{topic}__state__
Content Type: __state__{content_type}__state__
Style: __state__{style}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Script:
__state__{script}__state__

Generate a mix of hashtags that:
1. Are relevant to the content
2. Include both broad and niche tags
3. Follow platform best practices
4. Have good discoverability potential

If global custom instructions are provided, ensure your hashtags align with any brand guidelines, target audience, or specific hashtag strategies mentioned.
"""

def hashtag_generator_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
) -> dict:
    """
    Generate hashtags based on the script
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
        prompt_template: Custom prompt template with state placeholders
    """
    ctx.start_conversation("🔄 Starting hashtag generation...")
    
    prompt_template = ctx.get_prompt('hashtag_generator')
    if not prompt_template:
        prompt_template = HASHTAG_GENERATOR_PROMPT
    
    try:
        ctx.log_progress("📝 Analyzing content for hashtag opportunities...")

        # Use prompt template if provided, otherwise use default
        base_prompt = replace_state_placeholders(prompt_template, ctx.state)

        messages = [
            SystemMessage(content=base_prompt),
        ]

        if custom_user_message:
            messages.append(HumanMessage(content=f"Additional user instructions: {custom_user_message}"))

        ctx.log_progress("✍️ Generating hashtags...")
        response = ctx.invoke_model_with_temperature(messages)
        token_usage = response.response_metadata["token_usage"]
        
        result = {
            "hashtags": response.content,
            "lnode": "hashtag_generator",
            "token_usage": token_usage
        }

        ctx.finalize_conversation({
            "summary": "Generated hashtags",
            "hashtags": response.content,
            "token_usage": token_usage,
            "node": "hashtag_generator"
        })

        return result
        
    except Exception as e:
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "hashtag_generator"
        })
        raise 