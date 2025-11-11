#!/usr/bin/env python3
"""
Multi-Agent Content Creation Demo
CrewAI + LangGraph Integration

This is the main demo script for the Interview Kickstart presentation.
It demonstrates building a multi-agent system using CrewAI role-based
collaboration patterns with LangGraph workflow orchestration.

Usage:
    python main_demo.py --topic "Future of Remote Work"
    python main_demo.py --topic "AI in Healthcare" --style "Professional"
"""

import argparse
import sys
import time
from typing import Optional

# Demo imports
from workflow.graph_builder import (
    execute_content_creation_demo,
    demonstrate_workflow_features,
    demonstrate_crewai_integration,
    get_workflow_summary
)
from utils.display import (
    demo_introduction,
    framework_comparison,
    display_agent_roles,
    display_workflow_diagram,
    display_final_output,
    display_state_summary,
    pause_for_audience,
    section_header,
    demo_print
)
from workflow.state_schema import create_initial_state
from agents.crew_roles import display_roles_summary


def presentation_introduction():
    """
    Demo Introduction Section (3-4 minutes)
    """
    section_header("🎬 Welcome to Multi-Agent Content Creation", "bright_blue")
    
    demo_introduction()
    
    demo_print("\n🎯 Today's Learning Objectives:", "cyan", bold=True)
    objectives = [
        "1. Understanding CrewAI, AutoGen, and LangGraph frameworks",
        "2. Designing agent roles for specialized tasks", 
        "3. Implementing graph-based workflows with state management",
        "4. Deploying autonomous multi-agent systems"
    ]
    
    for obj in objectives:
        demo_print(f"   {obj}", "white")
    
    pause_for_audience()


def framework_education_section():
    """
    Framework Education Section (8 minutes)
    """
    section_header("🔍 Multi-Agent Framework Landscape", "magenta")
    
    demo_print("Let's understand the three major frameworks for multi-agent systems:", "cyan")
    
    # Framework comparison
    framework_comparison()
    
    demo_print("\n💡 Key Insight: Each framework has unique strengths!", "yellow", bold=True)
    demo_print("   • CrewAI excels at role-based collaboration", "green")
    demo_print("   • LangGraph provides powerful workflow orchestration", "green") 
    demo_print("   • AutoGen enables conversation-driven consensus", "green")
    
    demo_print("\n🎯 Our Demo Strategy: CrewAI + LangGraph Integration", "blue", bold=True)
    demo_print("   We'll combine CrewAI's role patterns with LangGraph's orchestration", "white")
    
    pause_for_audience()
    
    # Agent roles introduction
    section_header("🎭 Meet Our Content Creation Team", "magenta")
    display_agent_roles()
    
    demo_print("\n🤝 Notice how each agent has a specific CrewAI role:", "yellow")
    demo_print("   • Clear responsibilities and expertise areas", "white")
    demo_print("   • Specialized skills and backstories", "white")
    demo_print("   • Goal-oriented design for better outcomes", "white")
    
    pause_for_audience()


def workflow_architecture_section():
    """
    Workflow Architecture Section (5 minutes) 
    """
    section_header("🏗️ LangGraph Workflow Architecture", "blue")
    
    display_workflow_diagram()
    
    demo_print("\n⚡ Key LangGraph Features in Our Workflow:", "cyan", bold=True)
    
    features = [
        "🔄 State Management: Shared state flows through all agents",
        "🎯 Conditional Routing: Quality check determines next step", 
        "🔄 Revision Loops: Automatic improvement cycles",
        "📊 Execution Tracking: Monitor agent performance",
        "🛡️ Error Handling: Graceful failure recovery"
    ]
    
    for feature in features:
        demo_print(f"   {feature}", "green")
    
    demo_print("\n🎭 CrewAI Integration Benefits:", "magenta", bold=True)
    
    benefits = [
        "👨‍💼 Role Clarity: Each node represents a specialist",
        "🎯 Goal Alignment: Agents work toward clear objectives",
        "🤝 Team Dynamics: Professional collaboration patterns",
        "📈 Quality Focus: Built-in review and improvement"
    ]
    
    for benefit in benefits:
        demo_print(f"   {benefit}", "green")
    
    pause_for_audience()


def live_demo_section(topic: str, style: str):
    """
    Live Demo Section (10-12 minutes)
    """
    section_header("🚀 Live Multi-Agent Workflow Execution", "bright_green")
    
    demo_print(f"🎬 Let's watch our agent team create content about: '{topic}'", "blue", bold=True)
    demo_print(f"   Style: {style}", "cyan")
    
    # Execute the actual workflow
    final_state = execute_content_creation_demo(topic, style)
    
    # Display results
    section_header("📊 Workflow Results Analysis", "green")
    display_state_summary(final_state)
    display_final_output(final_state)
    
    # Performance insights
    total_execution_time = sum(final_state.execution_time.values())
    demo_print(f"\n⚡ Performance Insights:", "yellow", bold=True)
    demo_print(f"   • Total execution time: {total_execution_time:.2f} seconds", "green")
    demo_print(f"   • Average per agent: {total_execution_time/7:.2f} seconds", "green")
    demo_print(f"   • Quality score achieved: {final_state.quality_score:.1f}/10", "green")
    demo_print(f"   • Revision cycles: {final_state.revision_number}", "green")
    
    pause_for_audience()
    
    return final_state


def architecture_deep_dive():
    """
    Technical Architecture Deep Dive (5 minutes)
    """
    section_header("🔧 Technical Implementation Deep Dive", "blue")
    
    # Show workflow features
    demonstrate_workflow_features()
    
    # Show CrewAI integration
    demonstrate_crewai_integration()
    
    # Integration insights
    demo_print("\n💡 Why This Integration Works:", "yellow", bold=True)
    integration_benefits = [
        "🎯 Clear Separation of Concerns: LangGraph for flow, CrewAI for roles",
        "📈 Enhanced Quality: Role expertise + workflow orchestration",
        "🔧 Maintainability: Modular design makes updates easy",
        "⚡ Performance: Optimized state management and routing",
        "🎨 Flexibility: Easy to adapt for different use cases"
    ]
    
    for benefit in integration_benefits:
        demo_print(f"   {benefit}", "green")
    
    pause_for_audience()


def conclusion_and_qna():
    """
    Conclusion and Q&A Section (3-5 minutes)
    """
    section_header("🎯 Key Takeaways & Next Steps", "bright_green")
    
    summary = get_workflow_summary()
    
    demo_print("🌟 What We Built Today:", "cyan", bold=True)
    achievements = [
        "✅ Multi-agent system with 7 specialized roles",
        "✅ CrewAI + LangGraph integration pattern", 
        "✅ Working content creation pipeline",
        "✅ Quality assurance and revision loops",
        "✅ Scalable, modular architecture"
    ]
    
    for achievement in achievements:
        demo_print(f"   {achievement}", "green")
    
    demo_print("\n🚀 Business Value Delivered:", "magenta", bold=True)
    for value in summary['business_value']:
        demo_print(f"   • {value}", "green")
    
    demo_print("\n📚 Your Learning Path Forward:", "blue", bold=True)
    next_steps = [
        "1. Start with single-agent implementations",
        "2. Learn LangGraph fundamentals and state management", 
        "3. Explore CrewAI role-based patterns",
        "4. Design your own multi-agent teams",
        "5. Implement conditional workflows and error handling"
    ]
    
    for step in next_steps:
        demo_print(f"   {step}", "white")
    
    demo_print("\n🤝 Questions & Discussion:", "yellow", bold=True)
    demo_print("   What questions do you have about multi-agent systems?", "white")
    demo_print("   How would you adapt this for your own use cases?", "white")


def main():
    """
    Main demo execution function
    """
    parser = argparse.ArgumentParser(description='Multi-Agent Content Creation Demo')
    parser.add_argument('--topic', required=True, help='Content topic for demo')
    parser.add_argument('--style', default='Educational', 
                       choices=['Educational', 'Professional', 'Conversational', 'Entertaining'],
                       help='Content style')
    parser.add_argument('--full-presentation', action='store_true',
                       help='Run full 30-minute presentation')
    parser.add_argument('--demo-only', action='store_true', 
                       help='Run only the live demo section')
    
    args = parser.parse_args()
    
    try:
        if args.demo_only:
            # Just run the live demo
            live_demo_section(args.topic, args.style)
            
        elif args.full_presentation:
            # Full 30-minute presentation
            demo_print("🎬 Starting Full Presentation (30 minutes)", "bright_blue", bold=True)
            
            # 1. Introduction (3-4 minutes)
            presentation_introduction()
            
            # 2. Framework Education (8 minutes)  
            framework_education_section()
            
            # 3. Architecture Overview (5 minutes)
            workflow_architecture_section()
            
            # 4. Live Demo (10-12 minutes)
            live_demo_section(args.topic, args.style)
            
            # 5. Technical Deep Dive (5 minutes)
            architecture_deep_dive()
            
            # 6. Conclusion & Q&A (3-5 minutes)
            conclusion_and_qna()
            
            demo_print("\n🎉 Presentation Complete! Thank you for your attention!", "bright_green", bold=True)
            
        else:
            # Default: Just run the workflow demo
            final_state = execute_content_creation_demo(args.topic, args.style)
            display_final_output(final_state)
            
    except KeyboardInterrupt:
        demo_print("\n⏹️  Demo interrupted by user", "yellow")
        sys.exit(0)
        
    except Exception as e:
        demo_print(f"\n❌ Demo error: {str(e)}", "red")
        sys.exit(1)


if __name__ == "__main__":
    main()