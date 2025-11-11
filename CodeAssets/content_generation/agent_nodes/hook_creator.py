"""Hook creator agent node."""

from langchain_core.messages import SystemMessage, HumanMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from typing import Optional

HOOK_CREATOR_PROMPT = """
You are an expert hook creator specialized in crafting attention-grabbing opening lines for short-form video content.

Topic: __state__{topic}__state__
Content Type: __state__{content_type}__state__
Style: __state__{style}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Initial Reference Material (if provided):
__state__{initial_reference_material}__state__

Script:
__state__{script}__state__

Past Reflections/Feedback (if available):
__state__{critique}__state__

Your task is to create a compelling hook that:
1. Immediately captures attention in the first 3-5 seconds
2. Creates curiosity or poses an intriguing question
3. Promises value to the viewer
4. Aligns with the content style and tone
5. Is optimized for the specific platform and content type
6. Uses psychological triggers (curiosity gap, controversy, surprise, etc.)

Consider these hook frameworks:
- The Problem Hook: Start with a relatable problem
- The Question Hook: Pose an intriguing question
- The Stat Hook: Share a surprising statistic
- The Story Hook: Begin with a captivating story
- The Contradiction Hook: Challenge common beliefs
- The Tutorial Hook: Promise to teach something valuable

Generate 3-5 different hook options, then select and refine the best one. 
Provide the final hook as a single, polished line that's ready to use.

Focus only on creating the hook - not rewriting the entire script.

If global custom instructions are provided, ensure your hook aligns with those specific requirements, brand voice, or approach.
If initial reference material is provided, analyze any effective hook patterns or styles from it for inspiration.
"""

def hook_creator_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
) -> dict:
    """
    Generate a compelling hook based on the script and feedback
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
    """
    ctx.start_conversation("🔄 Starting hook creation...")
    
    try:
        script = ctx.state.get('script', '')
        topic = ctx.state.get('topic', 'default topic')
        content_type = ctx.state.get('content_type', 'Short (60 seconds)')
        style = ctx.state.get('style', 'Educational')
        critique = ctx.state.get('critique', '')
        
        ctx.log_progress("🎯 Analyzing script and feedback for hook creation...")

        if not script:
            ctx.log_progress("⚠️ No script available for hook creation")
            return {
                "hook": "Create engaging content that captures attention!",
                "lnode": "hook_creator",
                "token_usage": {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}
            }

        # Use prompt template from context or default
        prompt_template = ctx.prompts.get('hook_creator', HOOK_CREATOR_PROMPT)
        base_prompt = replace_state_placeholders(prompt_template, ctx.state)

        messages = [
            SystemMessage(content=base_prompt),
        ]

        if custom_user_message:
            ctx.log_progress("🔄 Applying additional user instructions...")
            messages.append(HumanMessage(content=f"Additional user instructions: {custom_user_message}"))

        ctx.log_progress("✨ Crafting compelling hook...")
        response = ctx.invoke_model_with_temperature(messages)
        token_usage = response.response_metadata.get("token_usage", {})
        
        # Extract the final hook from the response
        hook_content = response.content.strip()
        
        # Try to extract the final hook if the response contains multiple options
        lines = hook_content.split('\n')
        final_hook = hook_content
        
        # Look for patterns that indicate the final hook
        for i, line in enumerate(lines):
            if any(phrase in line.lower() for phrase in ['final hook:', 'selected hook:', 'best hook:', 'refined hook:']):
                if i + 1 < len(lines):
                    final_hook = lines[i + 1].strip()
                    break
        
        # If we still have a multi-line response, try to get the last meaningful line
        if '\n' in final_hook:
            meaningful_lines = [line.strip() for line in final_hook.split('\n') 
                               if line.strip() and not line.strip().startswith('**') 
                               and not any(word in line.lower() for word in ['hook', 'option', 'version'])]
            if meaningful_lines:
                final_hook = meaningful_lines[-1]

        # Clean up any formatting
        final_hook = final_hook.strip('"').strip("'").strip()
        
        result = {
            "hook": final_hook,
            "hook_options": response.content,  # Store full response with all options
            "lnode": "hook_creator",
            "token_usage": token_usage
        }

        ctx.finalize_conversation({
            "summary": "✅ Hook created successfully",
            "hook": final_hook,
            "full_response": response.content,
            "token_usage": token_usage,
            "node": "hook_creator"
        })

        return result
        
    except Exception as e:
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "hook_creator"
        })
        raise