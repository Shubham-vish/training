"""Content graph operator agent node."""
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from SharedCode.agent_utils.agent_utils import AgentContext
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum
import traceback
from SharedCode.agent_utils.graph_schema import GraphMetadata
from SharedCode.agent_utils.agent_utils import replace_state_placeholders
import logging
from langchain_core.messages import BaseMessage
logger = logging.getLogger(__name__)

class ActionType(str, Enum):
    NEW_CONTENT = "new_content"
    REVISE = "revise"
    GENERATE_SCRIPT = "generate_script"
    FINALIZE = "finalize"
    UNKNOWN = "unknown"

class AgentAction(BaseModel):
    """Represents an action to be taken by an agent"""
    agent_name: str = Field(..., description="Name of the agent to call")
    reason: str = Field(..., description="Reason for calling this agent")
    priority: int = Field(default=1, description="Priority of this action (1-5)")
    required_context: List[str] = Field(default_factory=list, description="Required context fields from state")

class OperatorAnalysis(BaseModel):
    """Structured output for operator's analysis of user request"""
    understanding: str = Field(..., description="Summary of what the user wants")
    action_type: ActionType = Field(..., description="Type of action to take")
    extracted_info: Dict[str, Any] = Field(default_factory=dict, description="Information extracted from user message")
    next_actions: List[AgentAction] = Field(..., description="List of agent actions to take in sequence")
    requires_followup: bool = Field(default=False, description="Whether followup is needed from user")
    followup_question: Optional[str] = Field(None, description="Question to ask user if followup needed")
    answer: Optional[str] = Field(None, description="Answer to the user's question")

def _ensure_graph_metadata(metadata: Optional[Dict[str, Any]]) -> Optional[GraphMetadata]:
    """Convert dictionary to GraphMetadata if needed"""
    if metadata is None:
        return None
    if isinstance(metadata, GraphMetadata):
        return metadata
    try:
        return GraphMetadata(**metadata)
    except Exception as e:
        print(f"Error converting graph metadata: {str(e)}")
        return None


OPERATOR_PROMPT = """
You are an expert content creation operator that helps users create engaging short-form video content.
Based on the user's message and current context, determine what needs to be done.

Current Context:
- Topic: __state__{topic}__state__
- Style: __state__{style}__state__
- Current Stage: __state__{current_stage}__state__
- Progress: __state__{current_progress}__state__
- Revision #: __state__{revision_number}__state__

Available Nodes (Agents):
__internal__{available_nodes}__internal__

Your task is to:
1. Understand what the user wants
2. Extract any relevant information
3. Determine which agent(s) to call and in what order
4. Consider the current state and graph structure

Respond with a structured analysis including:
- Understanding of the request
- Type of action needed
- Information to extract
- Sequence of agent calls with reasons
- Whether we need more information from the user

If we need more information from the user, ask a followup question.
If user is asking a general question, answer it.
"""

def content_graph_operator(ctx: AgentContext, custom_user_message: Optional[str] = None) -> dict:
    """
    Operator function for content graph that orchestrates content creation workflow.
    Handles user interactions, coordinates agent calls, and manages the content creation process.
    """
    ctx.start_conversation("🔄 Starting content operator analysis...")
    
    try:
        # Convert graph_metadata to proper object if needed
        metadata = ctx.graph_metadata
        graph_metadata = _ensure_graph_metadata(metadata)
        
        # Build context from state and graph metadata
        context = {
            "topic": ctx.state.get("topic"),
            "content_type": ctx.state.get("content_type", "Short (60 seconds)"),
            "style": ctx.state.get("style", "Educational"),
            "current_stage": ctx.state.get("current_node"),
            "revision_number": ctx.state.get("revision_number", 0),
            "available_nodes": list(graph_metadata.nodes.keys()) if graph_metadata else [],
            "current_progress": {
                "has_plan": "plan" in ctx.state,
                "has_script": "script" in ctx.state,
                "has_critique": "critique" in ctx.state
            }
        }
        context.update(ctx.state)
        # Add step for context preparation
        ctx.add_step(
            title="📋 Preparing analysis context",
            status="completed",
            details={
                "context": context,
                "user_message": custom_user_message
            }
        )

        context["available_nodes"] = _format_available_nodes(graph_metadata)

        # Prepare the analysis prompt with graph metadata
        prompt_template = ctx.prompts.get('operator', OPERATOR_PROMPT)
        system_prompt = replace_state_placeholders(prompt_template, context)

        # Add step for analysis request
        analysis_step_key = ctx.add_step(
            title="🤔 Analyzing user request",
            status="in_progress",
            details={
                "prompt": system_prompt,
                "user_message": custom_user_message
            }
        )
        messages: List[BaseMessage] = [SystemMessage(content=system_prompt)]
        if custom_user_message:
            messages.append(HumanMessage(content=custom_user_message))

        # Use LangChain's structured output for analysis
        analysis_raw = ctx.model.with_structured_output(
            OperatorAnalysis,
            include_raw=True
        ).invoke(messages)
        
        # Cast to dict and extract values
        result_dict = dict(analysis_raw)
        analysis = result_dict['parsed']
        raw_response = result_dict['raw']
        token_usage = raw_response.response_metadata.get('token_usage', {})

        # Update analysis step with results
        ctx.update_step(
            step_key=analysis_step_key,
            updates={
                "status": "completed",
                "details": {
                    "analysis": analysis.dict(),
                    "token_usage": token_usage
                }
            }
        )

        # Handle followup needed
        if analysis.requires_followup:
            ctx.add_step(
                title="❓ Need more information",
                status="waiting_for_input",
                details={
                    "followup_question": analysis.followup_question,
                    "reason": "Insufficient information to proceed"
                }
            )
            ctx.finalize_conversation({
                "summary": "Need more information",
                "followup_question": analysis.followup_question,
                "requires_user_input": True,
                "token_usage": token_usage,
                "node": "operator"
            })
            return ctx.state

        # Update state with extracted information
        if analysis.extracted_info:
            ctx.add_step(
                title="📝 Updating state with extracted information",
                status="completed",
                details={
                    "extracted_info": analysis.extracted_info
                }
            )
            
            new_state = ctx.state.copy()
            new_state.update(analysis.extracted_info)
            ctx.set_state(new_state)

        # Execute agent actions in sequence
        for action in analysis.next_actions:
            # Validate agent exists in graph metadata
            if graph_metadata and action.agent_name not in graph_metadata.nodes:
                ctx.add_step(
                    title=f"⚠️ Invalid agent requested: {action.agent_name}",
                    status="failed",
                    details={
                        "error": f"Agent {action.agent_name} not found in graph metadata",
                        "available_agents": list(graph_metadata.nodes.keys()) if graph_metadata else []
                    }
                )
                continue

            ctx.add_step(
                title=f"🔄 Executing {action.agent_name}",
                status="in_progress",
                details={
                    "reason": action.reason,
                    "priority": action.priority,
                    "required_context": action.required_context
                }
            )
            
            # Call the agent and handle the result
            agent_result = ctx.call_agent(action.agent_name, custom_user_message)

            # Update state with agent result
            new_state = ctx.state.copy()
            new_state.update(agent_result)
            ctx.set_state(new_state)

            ctx.update_state(agent_result)

            # Add completion step
            ctx.add_step(
                title=f"✅ Completed {action.agent_name}",
                status="completed",
                details={
                    "result": agent_result,
                    "token_usage": agent_result.get("token_usage", {})
                },
                token_usage=agent_result.get("token_usage", {})
            )
            ctx.sync_execution_info()
        
        result = {
            "summary": f"✅ Completed: {analysis.action_type}",
            "understanding": analysis.understanding,
            "actions_taken": [action.agent_name for action in analysis.next_actions],
            "response": analysis.answer,
            "token_usage": token_usage
        }

        # Finalize the conversation
        ctx.finalize_conversation({
            "summary": f"✅ Completed: {analysis.action_type}",
            "understanding": analysis.understanding,
            "actions_taken": [action.agent_name for action in analysis.next_actions],
            "response": analysis.answer,
            "token_usage": token_usage,
            "node": "operator"
        })

        return ctx.state
        
    except Exception as e:
        ctx.add_step(
            title="❌ Error in operator execution",
            status="failed",
            details={
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
        )
        ctx.finalize_conversation({
            "error": str(e),
            "status": "failed",
            "node": "operator"
        })
        raise

def _format_available_nodes(graph_metadata: Optional[GraphMetadata]) -> str:
    """Format available nodes and their descriptions for the prompt"""
    if not graph_metadata or not graph_metadata.nodes:
        return "No nodes available"
        
    formatted = []
    for name, node in graph_metadata.nodes.items():
        desc = node.description if hasattr(node, 'description') else "No description available"
        formatted.append(f"- {name}: {desc}")
    
    return "\n".join(formatted) 