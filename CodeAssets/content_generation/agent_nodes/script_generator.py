"""Script generator agent node."""

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from typing import Optional, List

SCRIPT_GENERATOR_PROMPT = """
You are a script generator tasked with creating a 60-second script for Reels/YouTube Shorts.

Topic: __state__{topic}__state__
Content Type: __state__{content_type}__state__
Style: __state__{style}__state__
Plan: __state__{plan}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Initial Reference Material (if provided):
__state__{initial_reference_material}__state__

Use the research content below to enhance your script:
__state__{content}__state__

Generate the best possible script that follows the plan and incorporates relevant research.

If global custom instructions are provided, ensure your script aligns with those specific requirements, tone, or approach.
If initial reference material is provided, use it as inspiration while creating your unique script.
"""

def script_generator_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
) -> dict:
    """Generate a script based on the plan and research
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
    """
    ctx.start_conversation("🔄 Starting script generation...")
    
    try:
        content = ctx.state.get('content', [])
        critique_text = ctx.state.get('critique', '')
        prev_script = ctx.state.get('script', '')

        ctx.log_progress("📝 Analyzing inputs and preparing script structure...")

        content_text = "\n\n".join(content) if content else "No content available"
        ctx.state['content'] = content_text  # Add content to state for template replacement
        
        prompt_template = ctx.prompts.get('script_generator', SCRIPT_GENERATOR_PROMPT)
        base_prompt = replace_state_placeholders(prompt_template, ctx.state)
        system_msg = SystemMessage(content=base_prompt)

        messages: List[BaseMessage] = [system_msg]

        if prev_script:
            ctx.log_progress("📄 Incorporating previous script version...")
            messages.append(AIMessage(content=prev_script))

        if critique_text:
            ctx.log_progress("🔄 Applying revision feedback...")
            messages.append(HumanMessage(
                content=f"Please revise based on this feedback:\n{critique_text}"))
            
        if custom_user_message:
            ctx.log_progress("🔄 Applying additional user instructions...")
            messages.append(HumanMessage(content=custom_user_message))

        ctx.log_progress("✍️ Generating script...")
        response = ctx.invoke_model_with_temperature(messages)
        hook = response.content.split("\n")[0]

        prev = ctx.state.get("prev_scripts", [])
        prev.append(response.content)
        token_usage = response.response_metadata["token_usage"]
        
        result = {
            "script": response.content,
            "draft": response.content,
            "hook": hook,
            "prev_scripts": prev,
            "lnode": "script_generator",
            "token_usage": token_usage
        }

        ctx.finalize_conversation({
            "summary": "✅ Script generated successfully",
            "script": response.content,
            "hook": hook,
            "token_usage": token_usage,
            "node": "script_generator"
        })

        return result
        
    except Exception as e:
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "script_generator"
        })
        raise 