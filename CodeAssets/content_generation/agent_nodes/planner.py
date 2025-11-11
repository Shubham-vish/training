"""Content planner agent node."""

from langchain_core.messages import SystemMessage, HumanMessage
from SharedCode.agent_utils.agent_utils import AgentContext, replace_state_placeholders
from typing import Optional, List
from langchain_core.messages import BaseMessage

PLANNER_PROMPT = """
You are a content planner tasked with creating a structured plan for a short-form video.

Topic: __state__{topic}__state__
Content Type: __state__{content_type}__state__
Style: __state__{style}__state__

Global Custom Instructions (if provided):
__state__{global_custom_instruction}__state__

Initial Reference Material (if provided):
__state__{initial_reference_material}__state__

Create a detailed content plan that:
1. Has a clear hook/intro (5-7 seconds)
2. Presents main points efficiently (45-50 seconds)
3. Ends with a strong conclusion (5-7 seconds)
4. Maintains viewer engagement throughout
5. Fits the chosen style and format

The plan should be specific enough to guide script writing but flexible enough for creative expression.

If global custom instructions are provided, incorporate them into your planning approach.
If initial reference material is provided, use it as inspiration or a starting point for your plan.
"""

def planner_node(
    ctx: AgentContext, 
    custom_user_message: Optional[str] = None,
) -> dict:
    """Generate a content plan based on the topic and style
    
    Args:
        ctx: Agent context containing state and model
        custom_user_message: Additional instructions from user
    """
    ctx.start_conversation("🔄 Starting content planning...")
    
    try:
        topic = ctx.state.get('topic', 'default topic')
        ctx.add_step(
            title="📋 Initializing content planning",
            status="completed",
            details={
                "topic": topic,
                "custom_instructions": custom_user_message
            }
        )

        # Step 2: Prepare prompt
        ctx.add_step(
            title="🎯 Preparing content outline prompt",
            status="in_progress"
        )
        content_type = ctx.state.get('content_type', 'Short (60 seconds)')
        style = ctx.state.get('style', 'Educational')
        prev_plan = ctx.state.get('plan', '')

        ctx.log_progress("📝 Analyzing topic and preparing content structure...")

        prompt_template = ctx.prompts.get('planner', PLANNER_PROMPT)
        base_prompt = replace_state_placeholders(prompt_template, ctx.state)
        messages: List[BaseMessage] = [SystemMessage(content=base_prompt)]

        if custom_user_message:
            messages.append(HumanMessage(content=f"Additional user instructions: {custom_user_message}"))

        if prev_plan:
            ctx.log_progress("📄 Incorporating previous plan version...")
            messages.append(HumanMessage(content=f"Previous plan:\n{prev_plan}\n\nPlease improve upon this plan."))
        else:
            messages.append(HumanMessage(content="Generate the content plan now."))

        ctx.log_progress("✍️ Generating content plan...")
        response = ctx.model.invoke(messages)
        token_usage = response.response_metadata["token_usage"]
        
        result = {
            "plan": response.content,
            "lnode": "planner",
            "token_usage": token_usage
        }

        ctx.finalize_conversation({
            "summary": "✅ Content plan generated successfully",
            "plan": response.content,
            "token_usage": token_usage,
            "node": "planner"
        })

        return result
        
    except Exception as e:
        ctx.add_step(
            title="❌ Error in content planning",
            status="failed",
            details={
                "error": str(e),
                "error_type": type(e).__name__
            }
        )
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "planner"
        })
        raise 