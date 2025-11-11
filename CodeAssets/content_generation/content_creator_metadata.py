from SharedCode.agent_utils.graph_schema import (
    GraphMetadata,
    StatePropertyMetadata,
    NodeMetadata,
    DataType,
)

from agents.content_generation.agent_nodes.planner import PLANNER_PROMPT
from agents.content_generation.agent_nodes.research_planner import RESEARCH_PLANNER_PROMPT
from agents.content_generation.agent_nodes.script_generator import SCRIPT_GENERATOR_PROMPT
from agents.content_generation.agent_nodes.reflection import REFLECTION_PROMPT
from agents.content_generation.agent_nodes.research_critique import RESEARCH_CRITIQUE_PROMPT
from agents.content_generation.agent_nodes.hashtag_generator import HASHTAG_GENERATOR_PROMPT
from agents.content_generation.agent_nodes.cta_generator import CTA_GENERATOR_PROMPT
from agents.content_generation.agent_nodes.operator import OPERATOR_PROMPT
from agents.state_management.state_updater_agent import STATE_UPDATER_PROMPT

# Define state properties metadata
CONTENT_CREATOR_STATE_PROPERTIES = {
    "title": StatePropertyMetadata(
        name="title",
        description="The title of the content",
        data_type=DataType.TEXT,
        default_value="AI Workflow Creation",
        is_required=True,
        show_in_ui=True
    ),
    "topic": StatePropertyMetadata(
        name="topic",
        description="The main topic for content creation",
        data_type=DataType.TEXT,
        default_value="",
        is_required=True,
        show_in_ui=True
    ),
    "content_type": StatePropertyMetadata(
        name="content_type",
        description="Type of content to generate",
        data_type=DataType.STRING,
        default_value="Short (60 seconds)",
        possible_values=["Short (60 seconds)",
                         "Medium (2-3 minutes)", "Long (5+ minutes)"],
        is_required=True,
        show_in_ui=True
    ),
    "style": StatePropertyMetadata(
        name="style",
        description="Content style or tone",
        data_type=DataType.STRING,
        default_value="Educational",
        possible_values=["Educational", "Conversational",
                         "Professional", "Entertaining", "Other"],
        is_required=True,
        show_in_ui=True
    ),
    "max_revisions": StatePropertyMetadata(
        name="max_revisions",
        description="Maximum number of revision cycles",
        data_type=DataType.INTEGER,
        default_value=2,
        is_required=False,
        show_in_ui=True
    ),
    "plan": StatePropertyMetadata(
        name="plan",
        description="Content plan outline",
        data_type=DataType.TEXT,
        is_user_configurable=False,
        show_in_ui=True
    ),
    "queries": StatePropertyMetadata(
        name="queries",
        description="Research queries",
        data_type=DataType.LIST,
        is_user_configurable=False,
        show_in_ui=True
    ),
    "content": StatePropertyMetadata(
        name="content",
        description="Research content results",
        data_type=DataType.LIST,
        is_user_configurable=False,
        show_in_ui=True
    ),
    "script": StatePropertyMetadata(
        name="script",
        description="Generated script",
        data_type=DataType.TEXT,
        is_user_configurable=False,
        show_in_ui=True
    ),
    "hook": StatePropertyMetadata(
        name="hook",
        description="Attention-grabbing opening line",
        data_type=DataType.TEXT,
        is_user_configurable=False,
        show_in_ui=True
    ),
    "critique": StatePropertyMetadata(
        name="critique",
        description="Feedback on the script",
        data_type=DataType.TEXT,
        is_user_configurable=False,
        show_in_ui=True
    ),
    "hashtags": StatePropertyMetadata(
        name="hashtags",
        description="Generated hashtags",
        data_type=DataType.LIST,
        is_user_configurable=False,
        show_in_ui=True
    ),
    "cta": StatePropertyMetadata(
        name="cta",
        description="Call to action",
        data_type=DataType.TEXT,
        is_user_configurable=False,
        show_in_ui=True
    ),
    "revision_number": StatePropertyMetadata(
        name="revision_number",
        description="Current revision number",
        data_type=DataType.INTEGER,
        default_value=0,
        is_user_configurable=False,
        show_in_ui=False
    ),
    "thread_id": StatePropertyMetadata(
        name="thread_id",
        description="Unique identifier for the workflow thread",
        data_type=DataType.STRING,
        is_user_configurable=False,
        show_in_ui=False
    )
}


# Define node metadata
CONTENT_CREATOR_NODE_METADATA = {
    
    "planner": NodeMetadata(
        name="planner",
        description="Creates a content plan based on the topic",
        input_properties=["topic"],
        output_properties=["plan"],
        ui_component="PlannerView",
        system_prompt=PLANNER_PROMPT
    ),
    "research_plan": NodeMetadata(
        name="research_plan",
        description="Generates research queries based on the plan",
        input_properties=["topic"],
        output_properties=["queries"],
        ui_component="ResearchPlanView",
        system_prompt=RESEARCH_PLANNER_PROMPT
    ),
    "script_generator": NodeMetadata(
        name="script_generator",
        description="Generates a script based on the plan and research",
        input_properties=["plan", "topic", "content_type", "style", "content", "critique", "Other"],
        output_properties=["script", "draft", "hook"],
        ui_component="ScriptGeneratorView",
        system_prompt=SCRIPT_GENERATOR_PROMPT
    ),
    "reflect": NodeMetadata(
        name="reflect",
        description="Reviews the script and provides feedback",
        input_properties=["script"],
        output_properties=["critique", "revision_number"],
        ui_component="ReflectionView",
        system_prompt=REFLECTION_PROMPT
    ),
    "research_critique": NodeMetadata(
        name="research_critique",
        description="Researches improvements based on critiques",
        input_properties=["critique"],
        output_properties=["content"],
        ui_component="ResearchCritiqueView",
        system_prompt=RESEARCH_CRITIQUE_PROMPT
    ),
    "hashtag_generator": NodeMetadata(
        name="hashtag_generator",
        description="Generates hashtags for the script",
        input_properties=["script"],
        output_properties=["hashtags"],
        ui_component="HashtagView",
        system_prompt=HASHTAG_GENERATOR_PROMPT
    ),
    "cta_generator": NodeMetadata(
        name="cta_generator",
        description="Generates a call-to-action for the script",
        input_properties=["script"],
        output_properties=["cta"],
        ui_component="CTAView",
        system_prompt=CTA_GENERATOR_PROMPT
    ),
    "operator": NodeMetadata(
        name="operator",
        description="Orchestrates the content creation workflow and coordinates between agents",
        input_properties=["topic", "content_type", "style", "current_node", "revision_number"],
        output_properties=["next_actions", "understanding", "action_type"],
        ui_component="OperatorView",
        system_prompt=OPERATOR_PROMPT
    ),
    "state_updater": NodeMetadata(
        name="state_updater",
        description="Analyzes and updates workflow state properties",
        input_properties=["prompt", "operation", "image_size", "image_url"],
        output_properties=["state_updates"],
        ui_component="StateUpdaterView",
        system_prompt=STATE_UPDATER_PROMPT
    )
}


# Edge descriptions for the graph
CONTENT_CREATOR_EDGES = {
    "planner": "research_plan",
    "research_plan": "script_generator",
    "script_generator": "reflect",
    "reflect": {
        "condition": "should_revise",
        "options": {
            "research_critique": "If revision count < max_revisions",
            "hashtag_generator": "If revision count >= max_revisions"
        }
    },
    "research_critique": "script_generator",
    "hashtag_generator": "cta_generator",
    "cta_generator": None  # End of workflow
}


# Create the graph metadata
CONTENT_CREATOR_GRAPH_METADATA = GraphMetadata(
    name="content_creator",
    description="A workflow graph for creating social media content scripts",
    state_properties=CONTENT_CREATOR_STATE_PROPERTIES,
    nodes=CONTENT_CREATOR_NODE_METADATA,
    edges=CONTENT_CREATOR_EDGES,
    operator_supported=True,
    initial_state={
        "topic": "",
        "content_type": "Short (60 seconds)",
        "style": "Educational",
        "revision_number": 0,
        "max_revisions": 2
    }
)


# Export active graph metadata
ACTIVE_GRAPH_METADATA = {
    "content_creator": CONTENT_CREATOR_GRAPH_METADATA
}


