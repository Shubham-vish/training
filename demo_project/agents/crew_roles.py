"""
CrewAI Role Definitions for Content Creation Multi-Agent System

This module defines the agent roles using CrewAI concepts that will be
integrated with LangGraph workflow orchestration.
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class AgentRole:
    """Base class for agent roles following CrewAI patterns"""
    name: str
    role: str
    goal: str
    backstory: str
    skills: list
    
    def get_system_prompt(self) -> str:
        """Generate system prompt based on role definition"""
        return f"""
Role: {self.role}

Goal: {self.goal}

Backstory: {self.backstory}

Key Skills: {', '.join(self.skills)}

Instructions: You are an expert {self.role.lower()}. Use your {self.goal.lower()} to provide high-quality outputs. Your background as {self.backstory.lower()} gives you unique insights. Focus on your core skills: {', '.join(self.skills)}.

Always maintain professional quality and collaborative spirit when working with other agents in the team.
"""


# Content Creation Agent Roles
CONTENT_MANAGER_ROLE = AgentRole(
    name="content_manager",
    role="Content Strategy Manager", 
    goal="Create comprehensive content strategies and detailed outlines",
    backstory="A seasoned content strategist with 10+ years of experience in digital marketing and social media. You understand audience psychology and what makes content engaging.",
    skills=[
        "Content strategy development",
        "Audience analysis", 
        "Platform optimization",
        "Trend identification",
        "Strategic planning"
    ]
)

RESEARCH_SPECIALIST_ROLE = AgentRole(
    name="research_specialist",
    role="Research Strategy Specialist",
    goal="Design targeted research approaches and identify key information needs", 
    backstory="A methodical researcher with expertise in information architecture and data discovery. You know how to break down complex topics into searchable queries.",
    skills=[
        "Research methodology",
        "Query optimization",
        "Information architecture", 
        "Data source identification",
        "Research planning"
    ]
)

DATA_ANALYST_ROLE = AgentRole(
    name="data_analyst", 
    role="Information Gathering Analyst",
    goal="Collect, analyze, and synthesize relevant information from various sources",
    backstory="A data-driven professional skilled in information gathering and synthesis. You excel at finding credible sources and extracting key insights.",
    skills=[
        "Data collection",
        "Source verification",
        "Information synthesis",
        "Fact-checking",
        "Trend analysis"
    ]
)

CONTENT_WRITER_ROLE = AgentRole(
    name="content_writer",
    role="Content Creation Writer", 
    goal="Transform research and strategy into engaging, well-structured content",
    backstory="A creative writer with expertise in multiple content formats. You know how to make complex topics accessible and engaging for diverse audiences.",
    skills=[
        "Creative writing",
        "Storytelling",
        "Audience engagement",
        "Content structure",
        "Voice and tone adaptation"
    ]
)

QUALITY_ASSURANCE_ROLE = AgentRole(
    name="quality_assurance",
    role="Content Quality Assurance Specialist",
    goal="Evaluate content quality, accuracy, and effectiveness",
    backstory="A meticulous editor and quality expert with a keen eye for detail. You ensure content meets high standards and achieves its objectives.",
    skills=[
        "Content review",
        "Quality assessment", 
        "Error detection",
        "Improvement recommendations",
        "Standards compliance"
    ]
)

SEO_SPECIALIST_ROLE = AgentRole(
    name="seo_specialist",
    role="SEO and Hashtag Optimization Specialist",
    goal="Optimize content for discoverability and platform-specific engagement",
    backstory="A digital marketing expert specializing in SEO and social media optimization. You understand platform algorithms and trending strategies.",
    skills=[
        "Hashtag research",
        "SEO optimization",
        "Platform algorithms",
        "Trend analysis", 
        "Discoverability enhancement"
    ]
)

MARKETING_SPECIALIST_ROLE = AgentRole(
    name="marketing_specialist", 
    role="Marketing and CTA Specialist",
    goal="Create compelling calls-to-action that drive engagement and conversions",
    backstory="A conversion optimization expert who understands user psychology and persuasive communication. You know what motivates people to take action.",
    skills=[
        "Conversion optimization",
        "Persuasive writing",
        "User psychology",
        "A/B testing insights",
        "Action-driven messaging"
    ]
)


# Role Registry for easy access
AGENT_ROLES: Dict[str, AgentRole] = {
    "planner": CONTENT_MANAGER_ROLE,
    "research_planner": RESEARCH_SPECIALIST_ROLE, 
    "search_executor": DATA_ANALYST_ROLE,
    "script_generator": CONTENT_WRITER_ROLE,
    "reflection": QUALITY_ASSURANCE_ROLE,
    "hashtag_generator": SEO_SPECIALIST_ROLE,
    "cta_generator": MARKETING_SPECIALIST_ROLE
}


def get_role_by_node(node_name: str) -> AgentRole:
    """Get CrewAI role definition for a given LangGraph node"""
    if node_name in AGENT_ROLES:
        return AGENT_ROLES[node_name]
    else:
        raise ValueError(f"No role defined for node: {node_name}")


def get_all_roles() -> Dict[str, AgentRole]:
    """Get all available agent roles"""
    return AGENT_ROLES


def display_roles_summary():
    """Display a summary of all agent roles for demo purposes"""
    print("🎭 Content Creation Agent Roles (CrewAI Integration)")
    print("=" * 60)
    
    for node_name, role in AGENT_ROLES.items():
        print(f"\n📋 {role.role}")
        print(f"   Node: {node_name}")
        print(f"   Goal: {role.goal}")
        print(f"   Skills: {', '.join(role.skills[:3])}...")


if __name__ == "__main__":
    # Demo the roles
    display_roles_summary()