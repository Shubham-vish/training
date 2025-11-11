"""
LangGraph Node Implementations with CrewAI Role Integration

Each node in this module represents a specialized agent following CrewAI role patterns
while operating within a LangGraph workflow for orchestration and state management.
"""

import time
from typing import Dict, Any
from workflow.state_schema import ContentCreationState
from agents.crew_roles import get_role_by_node
from utils.display import demo_print, agent_thinking, agent_output
from utils.llm_client import get_llm_client


def planner_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Content Manager Agent (CrewAI Role: Content Strategy Manager)
    
    Creates comprehensive content strategy and detailed outline based on the topic.
    This agent embodies the CrewAI pattern of role-based specialization.
    """
    start_time = time.time()
    role = get_role_by_node("planner")
    llm_client = get_llm_client()
    
    demo_print(f"🎭 {role.role} is working...", "blue")
    agent_thinking("Analyzing topic and developing content strategy...")
    
    # Create system prompt from role
    system_prompt = role.get_system_prompt()
    
    user_prompt = f"""
Create a comprehensive content strategy for the topic: "{state.topic}"

Requirements:
- Content Type: {state.content_type}
- Style: {state.style}
- Target Audience: {state.target_audience}

Please provide:
1. Clear content goals (3-4 specific objectives)
2. Detailed content outline with structure
3. Tone and style guidelines
4. Success metrics to track

Format your response as a structured strategy document.
"""
    
    # Generate response using LLM client
    content_outline = llm_client.generate_response(
        system_prompt, 
        user_prompt,
        "planner",
        state.topic,
        temperature=0.1
    )
    
    # Extract goals from the response (simplified for demo)
    content_goals = [
        f"Educate audience about {state.topic}",
        "Provide actionable insights",
        "Drive engagement through storytelling",
        "Establish thought leadership"
    ]
    
    execution_time = time.time() - start_time
    
    # Update state with agent outputs
    updates = {
        "content_outline": content_outline,
        "content_goals": content_goals,
        "current_step": "content_planning_complete"
    }
    
    # Record agent execution
    state.add_agent_execution("planner", role.role, updates, execution_time)
    
    agent_output(f"✅ Content strategy created for '{state.topic}'")
    demo_print(f"   Goals: {len(content_goals)} objectives defined", "green")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")
    
    return updates


def research_planner_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Research Specialist Agent (CrewAI Role: Research Strategy Specialist)
    
    Designs targeted research approaches and identifies key information needs.
    """
    start_time = time.time()
    role = get_role_by_node("research_planner")
    
    demo_print(f"🎭 {role.role} is working...", "blue")
    agent_thinking("Developing research strategy and identifying information needs...")
    
    time.sleep(1)  # Demo delay
    
    # Research planning based on content outline
    research_plan = f"""
🔍 RESEARCH STRATEGY FOR: {state.topic}

📋 RESEARCH OBJECTIVES:
• Gather current statistics and trends
• Identify expert opinions and case studies  
• Find real-world examples and applications
• Collect supporting data and evidence

🎯 KEY RESEARCH AREAS:
1. Current state of {state.topic}
2. Recent developments and trends
3. Challenges and pain points
4. Success stories and case studies
5. Future predictions and opportunities

📊 INFORMATION SOURCES:
• Industry reports and studies
• Expert interviews and opinions
• News articles and press releases
• Academic research and papers
• Social media trends and discussions
"""
    
    research_queries = [
        f"latest trends in {state.topic} 2024",
        f"{state.topic} statistics and market data",
        f"{state.topic} expert opinions and insights", 
        f"{state.topic} case studies and success stories",
        f"challenges and solutions in {state.topic}"
    ]
    
    execution_time = time.time() - start_time
    
    updates = {
        "research_plan": research_plan,
        "research_queries": research_queries,
        "current_step": "research_planning_complete"
    }
    
    state.add_agent_execution("research_planner", role.role, updates, execution_time)
    
    agent_output(f"✅ Research strategy developed")
    demo_print(f"   Queries: {len(research_queries)} targeted searches planned", "green")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")
    
    return updates


def search_executor_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Data Analyst Agent (CrewAI Role: Information Gathering Analyst)
    
    Collects, analyzes, and synthesizes relevant information from various sources.
    """
    start_time = time.time()
    role = get_role_by_node("search_executor")
    
    demo_print(f"🎭 {role.role} is working...", "blue")
    agent_thinking("Collecting and analyzing information from multiple sources...")
    
    time.sleep(1.5)  # Demo delay for "research"
    
    # Simulated research data (in real demo, this would use actual APIs)
    research_data = f"""
📊 RESEARCH FINDINGS FOR: {state.topic}

🔢 KEY STATISTICS:
• Market growth: 25% year-over-year increase
• Adoption rate: 60% of companies are implementing {state.topic}
• ROI improvement: Average 30% efficiency gains reported
• User satisfaction: 85% positive feedback from early adopters

💡 EXPERT INSIGHTS:
• "The future of {state.topic} lies in seamless integration with existing workflows" - Industry Expert
• Leading companies are seeing significant competitive advantages
• Early adoption is crucial for staying ahead of the curve
• Training and change management are key success factors

📈 TRENDS & DEVELOPMENTS:
• AI integration is becoming standard practice
• Remote and hybrid work models are driving adoption
• Focus shifting from technology to user experience
• Regulatory frameworks are evolving to support innovation

⚠️ CHALLENGES IDENTIFIED:
• Implementation complexity and costs
• Skills gap in workforce
• Data privacy and security concerns
• Resistance to change in traditional industries

✅ SUCCESS STORIES:
• Company A: 40% productivity improvement
• Company B: 50% reduction in processing time
• Company C: 90% customer satisfaction increase
"""
    
    key_insights = [
        "25% year-over-year market growth demonstrates strong momentum",
        "60% company adoption rate shows mainstream acceptance", 
        "30% average ROI improvement proves business value",
        "Skills gap and change management are primary implementation challenges",
        "AI integration and user experience are key differentiators"
    ]
    
    execution_time = time.time() - start_time
    
    updates = {
        "research_data": research_data,
        "key_insights": key_insights,
        "current_step": "research_complete"
    }
    
    state.add_agent_execution("search_executor", role.role, updates, execution_time)
    
    agent_output(f"✅ Research data collected and analyzed")
    demo_print(f"   Insights: {len(key_insights)} key findings identified", "green")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")
    
    return updates


def script_generator_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Content Writer Agent (CrewAI Role: Content Creation Writer)
    
    Transforms research and strategy into engaging, well-structured content.
    """
    start_time = time.time()
    role = get_role_by_node("script_generator")
    llm_client = get_llm_client()
    
    demo_print(f"🎭 {role.role} is working...", "blue")
    agent_thinking("Crafting engaging content based on strategy and research...")
    
    # Create system prompt from role
    system_prompt = role.get_system_prompt()
    
    user_prompt = f"""
Create engaging {state.content_type} content for: "{state.topic}"

Content Strategy:
{state.content_outline}

Research Data:
{state.research_data}

Requirements:
- Style: {state.style}
- Target Audience: {state.target_audience}
- Include hook, problem, solution, proof, and call-to-action
- Integrate research statistics and insights
- Make it compelling and actionable
- Keep it appropriate for {state.content_type}

Create a complete script that's ready for social media publication.
"""
    
    # Generate response using LLM client
    script = llm_client.generate_response(
        system_prompt,
        user_prompt,
        "script_generator", 
        state.topic,
        temperature=0.8
    )
    
    content_structure = {
        "hook": "Attention-grabbing question and promise",
        "problem": "Current challenges and pain points",
        "solution": "Benefits and statistics from research",
        "proof": "Real success stories and case studies", 
        "cta": "Clear next step for audience"
    }
    
    execution_time = time.time() - start_time
    
    updates = {
        "script": script,
        "content_structure": content_structure,
        "current_step": "script_complete"
    }
    
    state.add_agent_execution("script_generator", role.role, updates, execution_time)
    
    agent_output(f"✅ Content script created")
    demo_print(f"   Word count: ~{len(script.split())} words", "green")
    demo_print(f"   Structure: {len(content_structure)} sections", "green") 
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")
    
    return updates


def reflection_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Quality Assurance Agent (CrewAI Role: Content Quality Assurance Specialist)
    
    Evaluates content quality, accuracy, and effectiveness.
    """
    start_time = time.time()
    role = get_role_by_node("reflection")
    
    demo_print(f"🎭 {role.role} is working...", "blue")
    agent_thinking("Evaluating content quality and providing improvement recommendations...")
    
    time.sleep(1)  # Demo delay
    
    # Quality assessment based on content analysis
    # Simple scoring system for demo
    content_quality_factors = {
        "engagement": 8.5,  # Hook and storytelling
        "accuracy": 9.0,    # Research integration
        "structure": 8.0,   # Clear organization
        "actionability": 7.5,  # Clear next steps
        "audience_fit": 8.5   # Target audience alignment
    }
    
    quality_score = sum(content_quality_factors.values()) / len(content_quality_factors)
    
    critique = f"""
📊 CONTENT QUALITY ASSESSMENT

⭐ OVERALL SCORE: {quality_score:.1f}/10

🔍 DETAILED EVALUATION:
✅ STRENGTHS:
• Strong hook with compelling question format
• Excellent use of statistics and data points
• Clear problem-solution structure
• Credible social proof with specific examples
• Actionable call-to-action

⚠️ AREAS FOR IMPROVEMENT:
• Could benefit from more emotional connection
• Consider adding personal anecdote or story
• CTA could be more specific and urgent
• Add more sensory details for engagement

📈 RECOMMENDATIONS:
1. Enhance emotional appeal in the hook
2. Add specific timeline in CTA 
3. Include more relatable examples
4. Strengthen urgency in closing

🎯 CONTENT READINESS: {"APPROVED" if quality_score >= 7.0 else "NEEDS REVISION"}
"""
    
    improvement_suggestions = [
        "Add emotional storytelling element to hook",
        "Include specific timeline in call-to-action",
        "Add more relatable, everyday examples",
        "Strengthen urgency and scarcity in closing"
    ]
    
    execution_time = time.time() - start_time
    
    updates = {
        "quality_score": quality_score,
        "critique": critique,
        "improvement_suggestions": improvement_suggestions,
        "current_step": "quality_review_complete"
    }
    
    state.add_agent_execution("reflection", role.role, updates, execution_time)
    
    agent_output(f"✅ Quality assessment completed")
    demo_print(f"   Score: {quality_score:.1f}/10", "green" if quality_score >= 7.0 else "yellow")
    demo_print(f"   Status: {'APPROVED' if quality_score >= 7.0 else 'NEEDS REVISION'}", 
               "green" if quality_score >= 7.0 else "red")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")
    
    return updates


def hashtag_generator_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    SEO Specialist Agent (CrewAI Role: SEO and Hashtag Optimization Specialist)
    
    Optimizes content for discoverability and platform-specific engagement.
    """
    start_time = time.time()
    role = get_role_by_node("hashtag_generator")
    
    demo_print(f"🎭 {role.role} is working...", "blue")
    agent_thinking("Optimizing content for maximum discoverability and engagement...")
    
    time.sleep(1)  # Demo delay
    
    # Generate hashtags based on content and topic
    hashtags = [
        f"#{state.topic.replace(' ', '').replace('-', '')}",
        "#Innovation",
        "#Productivity", 
        "#FutureOfWork",
        "#Technology",
        "#BusinessTransformation",
        "#DigitalTransformation",
        "#WorkSmarter",
        "#Efficiency",
        "#Leadership"
    ]
    
    seo_keywords = [
        state.topic.lower(),
        "productivity improvement",
        "business transformation",
        "workplace innovation", 
        "digital efficiency"
    ]
    
    execution_time = time.time() - start_time
    
    updates = {
        "hashtags": hashtags,
        "seo_keywords": seo_keywords,
        "current_step": "seo_optimization_complete"
    }
    
    state.add_agent_execution("hashtag_generator", role.role, updates, execution_time)
    
    agent_output(f"✅ SEO optimization completed")
    demo_print(f"   Hashtags: {len(hashtags)} strategic tags generated", "green")
    demo_print(f"   Keywords: {len(seo_keywords)} SEO terms identified", "green")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")
    
    return updates


def cta_generator_node(state: ContentCreationState) -> Dict[str, Any]:
    """
    Marketing Specialist Agent (CrewAI Role: Marketing and CTA Specialist)
    
    Creates compelling calls-to-action that drive engagement and conversions.
    """
    start_time = time.time()
    role = get_role_by_node("cta_generator")
    
    demo_print(f"🎭 {role.role} is working...", "blue") 
    agent_thinking("Crafting compelling calls-to-action for maximum conversion...")
    
    time.sleep(1)  # Demo delay
    
    # Generate CTA based on content and goals
    cta = f"""
🚀 Ready to transform your approach to {state.topic}?

👇 Take action NOW:
✅ Follow for daily insights on workplace innovation
✅ Share this post with your team to start the conversation
✅ Comment "READY" if you want to learn more about implementation
✅ DM us for a free strategy consultation

⏰ Don't wait - your competitors aren't!

#GetStarted #TransformNow #YourFutureStartsHere
"""
    
    engagement_hooks = [
        "Follow for daily insights",
        "Share with your team", 
        "Comment 'READY' for more info",
        "DM for free consultation",
        "Tag someone who needs to see this"
    ]
    
    execution_time = time.time() - start_time
    
    updates = {
        "cta": cta,
        "engagement_hooks": engagement_hooks,
        "current_step": "content_creation_complete"
    }
    
    state.add_agent_execution("cta_generator", role.role, updates, execution_time)
    
    agent_output(f"✅ Call-to-action created")
    demo_print(f"   Engagement hooks: {len(engagement_hooks)} conversion strategies", "green")
    demo_print(f"   Execution time: {execution_time:.2f}s", "cyan")
    
    return updates