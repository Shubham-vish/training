"""
Sample backup data for demo reliability

This module provides pre-generated outputs in case of API failures
or network issues during the live demonstration.
"""

SAMPLE_OUTPUTS = {
    "future_of_remote_work": {
        "topic": "Future of Remote Work",
        "content_outline": """
📋 CONTENT STRATEGY FOR: Future of Remote Work

🎯 CONTENT GOALS:
• Educate audience about remote work evolution
• Provide actionable insights for adaptation
• Drive engagement through success stories
• Establish thought leadership in workplace innovation

📝 CONTENT OUTLINE:
1. Hook: The remote work revolution is here to stay
2. Problem: Traditional office-centric thinking is obsolete
3. Solution: Hybrid models and digital-first approaches
4. Benefits: Productivity gains and employee satisfaction
5. Call to Action: Prepare for the future workplace

🎨 TONE & STYLE: Educational
👥 TARGET AUDIENCE: General
⏱️ FORMAT: Short (60 seconds)
""",
        "research_data": """
📊 RESEARCH FINDINGS FOR: Future of Remote Work

🔢 KEY STATISTICS:
• Market growth: 42% of U.S. workforce now works remotely full-time
• Adoption rate: 88% of companies implemented remote work policies
• ROI improvement: Average 35% productivity increase reported
• User satisfaction: 92% of remote workers want to continue

💡 EXPERT INSIGHTS:
• "The future of work is not about location, but about results" - Workplace Innovation Expert
• Companies embracing remote-first policies see better talent retention
• Technology adoption accelerated by 5-7 years due to remote work needs
• Hybrid models emerging as the optimal solution for most organizations

📈 TRENDS & DEVELOPMENTS:
• Virtual collaboration tools becoming more sophisticated
• Focus on asynchronous communication and documentation
• Company culture adapting to digital-first approaches
• Mental health and work-life balance prioritized

⚠️ CHALLENGES IDENTIFIED:
• Communication gaps and isolation concerns
• Technology infrastructure requirements
• Management adaptation to remote oversight
• Maintaining company culture in distributed teams

✅ SUCCESS STORIES:
• Company A: 40% increase in employee satisfaction
• Company B: 25% reduction in overhead costs
• Company C: 60% improvement in talent acquisition range
""",
        "script": """
🎬 FUTURE OF REMOTE WORK: THE REVOLUTION IS HERE

🪝 HOOK:
What if I told you that the biggest workplace revolution in a century isn't coming - it's already here? 
In the next 60 seconds, you'll discover why 92% of remote workers never want to go back to the old way of working.

🔥 THE PROBLEM:
Traditional office-centric thinking is becoming obsolete fast:
• Companies losing top talent to remote-first competitors
• $15,000+ per employee wasted on unused office space annually
• 67% productivity loss from forced return-to-office policies
• Employee burnout from inflexible work arrangements

💡 THE SOLUTION:
The future of work is already being written by forward-thinking companies:
✅ 42% of U.S. workforce now works remotely full-time
✅ 88% of companies have implemented flexible work policies
✅ 35% average productivity increase in remote-first organizations
✅ 92% of remote workers report higher job satisfaction

🌟 REAL IMPACT:
• Company A saw 40% increase in employee satisfaction
• Company B reduced overhead costs by 25%
• Company C expanded talent acquisition range by 60%

🚀 YOUR NEXT STEP:
The future of work isn't waiting for anyone. Companies that adapt now will dominate tomorrow.
Ready to future-proof your career? Start building your remote work skills today.

#RemoteWork #FutureOfWork #ProductivityRevolution #WorkFromHome
""",
        "hashtags": [
            "#FutureOfRemoteWork",
            "#RemoteWork", 
            "#ProductivityRevolution",
            "#WorkFromHome",
            "#DigitalTransformation",
            "#FlexibleWork",
            "#WorkLifeBalance",
            "#RemoteFirst",
            "#HybridWork",
            "#WorkplaceInnovation"
        ],
        "cta": """
🚀 Ready to master the future of remote work?

👇 Take action NOW:
✅ Follow for daily remote work strategies and tips
✅ Share this post with colleagues still stuck in traditional thinking  
✅ Comment "REMOTE" if you're ready to embrace the future
✅ DM us for a free remote work readiness assessment

⏰ The future of work is here - don't get left behind!

#JoinTheRevolution #RemoteWorkMastery #FutureReadyCareer
""",
        "quality_score": 8.5,
        "critique": """
📊 CONTENT QUALITY ASSESSMENT

⭐ OVERALL SCORE: 8.5/10

🔍 DETAILED EVALUATION:
✅ STRENGTHS:
• Strong hook with compelling statistics
• Excellent use of current data and research
• Clear problem-solution structure  
• Credible social proof with specific company examples
• Actionable call-to-action with clear next steps

⚠️ AREAS FOR IMPROVEMENT:
• Could add more emotional connection to personal experiences
• Consider including brief mention of potential challenges
• CTA could be more specific about timeline

📈 RECOMMENDATIONS:
1. Add brief personal remote work story in hook
2. Include one challenge acknowledgment for balance
3. Specify timeline in CTA (e.g., "Start this week")

🎯 CONTENT READINESS: APPROVED - High quality, ready for publication
"""
    },
    
    "ai_in_healthcare": {
        "topic": "AI in Healthcare",
        "content_outline": """
📋 CONTENT STRATEGY FOR: AI in Healthcare

🎯 CONTENT GOALS:
• Educate about AI healthcare applications
• Address common concerns and misconceptions
• Showcase real-world success stories
• Position as healthcare innovation thought leader

📝 CONTENT OUTLINE:
1. Hook: AI is saving lives right now, not in the future
2. Problem: Healthcare bottlenecks and human limitations
3. Solution: AI-powered diagnostics and treatment optimization
4. Benefits: Faster diagnoses, better outcomes, reduced costs
5. Call to Action: Support AI healthcare adoption

🎨 TONE & STYLE: Educational
👥 TARGET AUDIENCE: General
⏱️ FORMAT: Short (60 seconds)
""",
        "script": """
🎬 AI IN HEALTHCARE: SAVING LIVES TODAY

🪝 HOOK:
While you watched this video, AI helped diagnose 147 medical conditions and potentially saved 12 lives.
This isn't science fiction - this is healthcare reality in 2024.

🔥 THE PROBLEM:
Our healthcare system is overwhelmed and human-limited:
• 12 million diagnostic errors annually in the US alone
• 4-6 hours average wait time in emergency departments
• $750 billion wasted on inefficient medical processes
• 1 in 10 patients experience preventable medical errors

💡 THE SOLUTION:
AI is revolutionizing healthcare right now:
✅ 94% accuracy in early cancer detection (vs 86% human accuracy)
✅ 50% reduction in diagnostic time for critical conditions
✅ $150 billion potential annual savings in healthcare costs
✅ 24/7 monitoring and early warning systems

🌟 REAL IMPACT:
• Hospital A reduced diagnostic errors by 73%
• Clinic B improved treatment outcomes by 45%
• System C cut administrative costs by 60%

🚀 YOUR NEXT STEP:
The future of healthcare is here. Support AI adoption in your healthcare choices.
Every day we delay costs lives.

#AIHealthcare #MedicalInnovation #HealthTech #FutureOfMedicine
""",
        "quality_score": 8.7
    }
}

def get_sample_output(topic_key: str, output_type: str) -> str:
    """Get sample output for demo backup purposes"""
    topic_data = SAMPLE_OUTPUTS.get(topic_key, SAMPLE_OUTPUTS["future_of_remote_work"])
    return topic_data.get(output_type, f"Sample {output_type} for {topic_key}")

def get_topic_key(topic: str) -> str:
    """Convert topic string to sample data key"""
    topic_lower = topic.lower()
    if "remote" in topic_lower or "work" in topic_lower:
        return "future_of_remote_work"
    elif "ai" in topic_lower and "health" in topic_lower:
        return "ai_in_healthcare" 
    else:
        # Default fallback
        return "future_of_remote_work"

# Demo timing data for realistic delays
DEMO_TIMING = {
    "planner": 1.2,
    "research_planner": 1.0,
    "search_executor": 1.8,
    "script_generator": 2.3,
    "reflection": 1.1,
    "hashtag_generator": 0.9,
    "cta_generator": 1.0
}

def get_demo_timing(agent_name: str) -> float:
    """Get realistic timing for demo agent execution"""
    return DEMO_TIMING.get(agent_name, 1.0)