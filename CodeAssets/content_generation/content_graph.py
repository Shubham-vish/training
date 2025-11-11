from agents.content_generation.agent_nodes.planner import planner_node, PLANNER_PROMPT
from agents.content_generation.agent_nodes.research_planner import research_plan_node, RESEARCH_PLANNER_PROMPT
from agents.content_generation.agent_nodes.search_executor import search_executor_node, SEARCH_EXECUTOR_PROMPT
from agents.content_generation.agent_nodes.script_generator import script_generator_node, SCRIPT_GENERATOR_PROMPT
from agents.content_generation.agent_nodes.reflection import reflection_node, REFLECTION_PROMPT
from agents.content_generation.agent_nodes.research_critique import research_critique_node, RESEARCH_CRITIQUE_PROMPT
from agents.content_generation.agent_nodes.hook_creator import hook_creator_node, HOOK_CREATOR_PROMPT
from agents.content_generation.agent_nodes.hashtag_generator import hashtag_generator_node, HASHTAG_GENERATOR_PROMPT
from agents.content_generation.agent_nodes.cta_generator import cta_generator_node, CTA_GENERATOR_PROMPT
from agents.content_generation.agent_nodes.operator import content_graph_operator, OPERATOR_PROMPT
from agents.content_generation.conditions.content_creator_conditions import should_revise, after_hook_creator
from agents.state_management.state_updater_agent import state_updater_agent
from agents.state_management.global_properties_agent import global_properties_agent
from agents.state_management.custom_properties_agent import custom_properties_agent
from agents.content_generation.content_creator_metadata import CONTENT_CREATOR_GRAPH_METADATA
from SharedCode.agent_utils.graph_schema import (
    GraphMetadata,
    StatePropertyMetadata,
    NodeMetadata,
    DataType,
)
from agents.general.general_agent import general_agent_node

# Define state properties metadata
CONTENT_CREATOR_STATE_PROPERTIES = {
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
        is_required=False,
        show_in_ui=True
    ),
    "style": StatePropertyMetadata(
        name="style",
        description="Content style or tone",
        data_type=DataType.STRING,
        default_value="Educational",
        possible_values=["Educational", "Conversational",
                         "Professional", "Entertaining", "Other"],
        is_required=False,
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
    "global_custom_instruction": StatePropertyMetadata(
        name="global_custom_instruction",
        description="Global custom instructions that apply to all nodes in the workflow",
        data_type=DataType.TEXT,
        default_value="",
        is_required=False,
        show_in_ui=True,
        is_user_configurable=True
    ),
    "initial_reference_material": StatePropertyMetadata(
        name="initial_reference_material",
        description="Reference script, ideas, or any initial material to guide content creation",
        data_type=DataType.TEXT,
        default_value="",
        is_required=False,
        show_in_ui=True,
        is_user_configurable=True
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
    "hook_options": StatePropertyMetadata(
        name="hook_options",
        description="Multiple hook options generated",
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
    "search_executor": NodeMetadata(
        name="search_executor",
        description="Executes web searches and analyzes results",
        input_properties=["queries", "topic", "content_type", "style"],
        output_properties=["content", "search_results"],
        ui_component="SearchExecutorView",
        system_prompt=SEARCH_EXECUTOR_PROMPT
    ),
    "script_generator": NodeMetadata(
        name="script_generator",
        description="Generates a script based on the plan and research",
        input_properties=["plan", "topic", "content_type",
                          "style", "content", "critique", "Other"],
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
        output_properties=["queries"],
        ui_component="ResearchCritiqueView",
        system_prompt=RESEARCH_CRITIQUE_PROMPT
    ),
    "hook_creator": NodeMetadata(
        name="hook_creator",
        description="Creates compelling hooks based on script and feedback",
        input_properties=["script", "topic", "content_type", "style", "critique"],
        output_properties=["hook", "hook_options"],
        ui_component="HookCreatorView",
        system_prompt=HOOK_CREATOR_PROMPT
    ),
    "hashtag_generator": NodeMetadata(
        name="hashtag_generator",
        description="Generates hashtags for the script",
        input_properties=["script", "topic"],
        output_properties=["hashtags"],
        ui_component="HashtagView",
        system_prompt=HASHTAG_GENERATOR_PROMPT
    ),
    "cta_generator": NodeMetadata(
        name="cta_generator",
        description="Generates a call-to-action for the script",
        input_properties=["script", "topic"],
        output_properties=["cta"],
        ui_component="CTAView",
        system_prompt=CTA_GENERATOR_PROMPT
    ),
    "state_updater": NodeMetadata(
        name="state_updater",
        description="Updates the state based on the script",
        input_properties=[],
        output_properties=[],
        ui_component="StateUpdaterView",
        system_prompt=None
    ),
    "global_properties_agent": NodeMetadata(
        name="global_properties_agent",
        description="Updates the global properties based on the script",
        input_properties=[],
        output_properties=[],
        ui_component="GlobalPropertiesView",
        system_prompt=None
    ),
    "custom_properties_agent": NodeMetadata(
        name="custom_properties_agent",
        description="Updates the custom properties based on the script",
        input_properties=[],
        output_properties=[],
        ui_component="CustomPropertiesView",
        system_prompt=None
    ),
    "operator": NodeMetadata(
        name="operator",
        description="Operator for the content graph",
        input_properties=["topic", "content_type", "style", "revision_number", "max_revisions"],
        output_properties=["next_node"],
        ui_component="OperatorView",
        system_prompt=OPERATOR_PROMPT
    ),
    "general_agent": NodeMetadata(
        name="general_agent",
        description="General agent for the content graph",
        input_properties=[],
        output_properties=[],
    )
}


# Edge descriptions for the graph
CONTENT_CREATOR_EDGES = {
    "planner": "research_plan",
    "research_plan": "search_executor",
    "search_executor": "script_generator",
    "script_generator": "reflect",
    "reflect": {
        "condition": "should_revise",
        "options": {
            "research_critique": "If revision count < max_revisions",
            "hook_creator": "If revision count >= max_revisions"
        }
    },
    "research_critique": "search_executor",
    "hook_creator": "hashtag_generator",
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
        "max_revisions": 2,
        "global_custom_instruction": "",
        "initial_reference_material": ""
    },
    default_temps={
        "planner": 0.1,
        "research_plan": 0.0,
        "search_executor": 0.0,
        "script_generator": 0.8,
        "reflect": 0.2,
        "research_critique": 0.0,
        "hook_creator": 1.0,
        "hashtag_generator": 0.7,
        "cta_generator": 0.6,
        "operator": 0.0,
        "state_updater": 0.0,
        "global_properties_agent": 0.0,
        "custom_properties_agent": 0.0,
        "general_agent": 0.0
    }
)

CONTENT_CREATOR_GRAPH = {
    "metadata": CONTENT_CREATOR_GRAPH_METADATA.model_dump(),
    "nodes": {
        "planner": planner_node,
        "research_plan": research_plan_node,
        "search_executor": search_executor_node,
        "script_generator": script_generator_node,
        "reflect": reflection_node,
        "research_critique": research_critique_node,
        "hook_creator": hook_creator_node,
        "hashtag_generator": hashtag_generator_node,
        "cta_generator": cta_generator_node,
        "operator": content_graph_operator,
        "state_updater": state_updater_agent,
        "global_properties_agent": global_properties_agent,
        "custom_properties_agent": custom_properties_agent,
        "general_agent": general_agent_node
    },

    "edges": {
        "planner": "research_plan",
        "research_plan": "search_executor",
        "search_executor": "script_generator",
        "script_generator": "reflect",
        "reflect": should_revise,
        "research_critique": "search_executor",
        "hook_creator": "hashtag_generator",
        "hashtag_generator": "cta_generator",
        "cta_generator": None  # End of workflow
    },

    "initial_state": {
        "topic": "",
        "content_type": "Short (60 seconds)",
        "style": "Educational",
        "revision_number": 0,
        "max_revisions": 2,
        "global_custom_instruction": "",
        "initial_reference_material": "",
        "thread_id": "example-thread-124"
    }
}
