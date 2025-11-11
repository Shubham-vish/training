"""CTA generator agent node."""
from langchain_core.messages import SystemMessage, HumanMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from typing import Optional
import logging

logger = logging.getLogger(__name__)

CTA_GENERATOR_PROMPT = """
You are a CTA (Call To Action) generator tasked with creating an engaging call to action for a short-form video.

Topic: __state__{topic}__state__
Content Type: __state__{content_type}__state__
Style: __state__{style}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Script:
__state__{script}__state__

Generate a compelling call to action that:
1. Naturally flows from the script content
2. Encourages viewer engagement (like, comment, share)
3. Is concise and actionable
4. Maintains the style and tone of the content

If global custom instructions are provided, ensure your CTA aligns with any specific engagement goals, brand voice, or call-to-action preferences mentioned.
"""

def cta_generator_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
) -> dict:
    """Generate call to action based on the script
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
    """
    ctx.start_conversation("🔄 Starting CTA generation...")
    
    try:
        script = ctx.state.get('script', '')
        topic = ctx.state.get('topic', 'default topic')
        content_type = ctx.state.get('content_type', 'Short (60 seconds)')
        style = ctx.state.get('style', 'Educational')

        ctx.log_progress("📝 Analyzing script and preparing CTA...")

        prompt_template = ctx.prompts.get('cta_generator', CTA_GENERATOR_PROMPT)
        base_prompt = replace_state_placeholders(prompt_template, ctx.state)

        messages = [
            SystemMessage(content=base_prompt),
            HumanMessage(content="Generate the CTA now.")
        ]

        if custom_user_message:
            messages.append(HumanMessage(content=f"Additional user instructions: {custom_user_message}"))

        ctx.log_progress("✍️ Generating CTA...")
        response = ctx.invoke_model_with_temperature(messages)
        token_usage = response.response_metadata["token_usage"]
        
        result = {
            "cta": response.content,
            "lnode": "cta_generator",
            "token_usage": token_usage
        }
        logger.info("---------    CTA generated    ---------")
        logger.info("--------------------------------")
        logger.info(f"CTA: {result}")
        logger.info("--------------------------------")
        logger.info("--------------------------------")
        ctx.finalize_conversation({
            "summary": "✅ CTA generated successfully",
            "cta": response.content,
            "token_usage": token_usage,
            "node": "cta_generator"
        })

        return result
        
    except Exception as e:
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "cta_generator"
        })
        raise 