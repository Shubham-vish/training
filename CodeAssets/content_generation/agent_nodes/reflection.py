"""Reflection agent node."""

from langchain_core.messages import SystemMessage, HumanMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from typing import Optional

REFLECTION_PROMPT = """
You are a content strategist tasked with reflecting on the research and plan for a short-form video.

Topic: __state__{topic}__state__
Content Type: __state__{content_type}__state__
Style: __state__{style}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Plan:
__state__{plan}__state__

Research Content:
__state__{content}__state__

Analyze and reflect on:
1. Alignment between research and plan
2. Coverage of key points
3. Potential gaps or improvements
4. Suggestions for strengthening the content

If global custom instructions are provided, evaluate how well the content aligns with those requirements and suggest improvements accordingly.
"""

def reflection_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
) -> dict:
    """Generate reflection on the research and plan
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
    """
    ctx.start_conversation("🔄 Starting reflection phase...")
    
    try:
        plan = ctx.state.get('plan', '')
        content = ctx.state.get('content', [])
        topic = ctx.state.get('topic', 'default topic')
        content_type = ctx.state.get('content_type', 'Short (60 seconds)')
        style = ctx.state.get('style', 'Educational')
        script = ctx.state.get('script', '')
        ctx.log_progress("📝 Analyzing research and plan...")

        content_text = "\n\n".join(content) if content else "No content available"
        ctx.state['content'] = content_text  # Add content to state for template replacement
        
        prompt_template = ctx.prompts.get('reflection', REFLECTION_PROMPT)
        base_prompt = replace_state_placeholders(prompt_template, ctx.state)

        if custom_user_message:
            base_prompt += f"\n\nAdditional user instructions: {custom_user_message}"

        messages = [
            SystemMessage(content=base_prompt),
            HumanMessage(content=f"Script Generated and needs to be revised\n: {script}")
        ]
        if custom_user_message:
            messages.append(HumanMessage(content=custom_user_message))
        

        ctx.log_progress("✍️ Generating reflection...")
        response = ctx.model.invoke(messages)
        token_usage = response.response_metadata["token_usage"]
        
        result = {
            "critique": response.content,
            "lnode": "reflect",
            "revision_number": ctx.state.get("revision_number", 0) + 1,
            "token_usage": token_usage
        }

        ctx.finalize_conversation({
            "summary": "✅ Script review completed",
            "critique": response.content,
            "token_usage": token_usage,
            "node": "reflection"
        })

        return result
        
    except Exception as e:
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "reflection"
        })
        raise 