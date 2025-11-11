"""
Test Individual Nodes

This script allows you to test individual agent nodes without running
the entire workflow. Useful for debugging and development.
"""

from workflow.state_schema import ContentCreationState
from agents.script_generator import script_generator_node
from agents.planner import planner_node
from agents.research_planner import research_planner_node
from agents.search_executor import search_executor_node
from agents.reflection import reflection_node
from agents.hashtag_generator import hashtag_generator_node
from agents.cta_generator import cta_generator_node


def test_script_generator():
    """Test script generator node independently"""
    print("🧪 Testing Script Generator Node\n")
    
    # Create state from scratch
    state = ContentCreationState(
        topic="Machine Learning",
        content_type="LinkedIn Post",
        style="Professional and engaging",
        target_audience="Tech professionals and data scientists"
    )
    
    # Set required fields for script generator
    state.content_outline = """
    Content Strategy:
    - Goal 1: Educate about ML fundamentals
    - Goal 2: Showcase practical applications
    - Goal 3: Drive engagement with industry insights
    
    Structure:
    1. Hook: Start with a surprising ML statistic
    2. Problem: Current challenges in ML adoption
    3. Solution: Benefits of ML implementation
    4. Proof: Real-world success stories
    5. CTA: Encourage discussion
    """
    
    state.research_data = """
    Key Statistics:
    - ML market growing at 42% CAGR
    - 80% of enterprises plan ML adoption by 2025
    - Average 30% ROI improvement with ML
    
    Trends:
    - AutoML democratizing ML development
    - Edge ML gaining traction for real-time processing
    - Explainable AI becoming critical for trust
    
    Challenges:
    - Data quality and availability
    - Talent shortage in ML expertise
    - Integration with legacy systems
    """
    
    state.content_goals = ["Educate", "Engage", "Inspire action"]
    
    # Execute the node
    print("▶️  Executing script_generator_node...\n")
    result = script_generator_node(state)
    
    # Apply the updates to state (nodes return updates but don't modify state directly)
    for key, value in result.items():
        if hasattr(state, key):
            setattr(state, key, value)
    
    print("\n" + "="*60)
    print("📄 GENERATED SCRIPT:")
    print("="*60)
    if state.script:
        print(state.script)
        print("\n" + "="*60)
        print(f"✅ Script generated successfully!")
        print(f"   Word count: {len(state.script.split())} words")
    else:
        print("⚠️  No script generated (state.script is empty)")
    print("="*60)


def test_planner():
    """Test planner node independently"""
    print("🧪 Testing Planner Node\n")
    
    state = ContentCreationState(
        topic="Artificial Intelligence",
        content_type="Blog Post",
        style="Educational and inspiring",
        target_audience="Business leaders and entrepreneurs"
    )
    
    print("▶️  Executing planner_node...\n")
    result = planner_node(state)
    
    print("\n" + "="*60)
    print("📋 CONTENT OUTLINE:")
    print("="*60)
    print(state.content_outline)
    print("\n" + "="*60)
    print(f"✅ Strategy created successfully!")
    print("="*60)


def test_reflection():
    """Test reflection node independently"""
    print("🧪 Testing Reflection Node\n")
    
    state = ContentCreationState(
        topic="Cloud Computing",
        content_type="LinkedIn Post",
        style="Professional",
        target_audience="IT professionals"
    )
    
    # Set required fields
    state.script = """
    🚀 Cloud Computing is Transforming Business
    
    Did you know that 94% of enterprises now use cloud services? 
    
    The challenge? Many struggle with migration complexity and security concerns.
    
    But here's the opportunity: Companies that successfully migrate see 30% cost 
    reduction and 2x faster deployment times.
    
    Real example: Netflix saved $1B by moving to AWS, while gaining unprecedented 
    scalability.
    
    💡 What's your biggest cloud migration challenge? Share below!
    """
    
    state.content_goals = ["Educate", "Engage"]
    state.content_outline = "Brief outline about cloud computing benefits"
    
    print("▶️  Executing reflection_node...\n")
    result = reflection_node(state)
    
    print("\n" + "="*60)
    print("📊 QUALITY ASSESSMENT:")
    print("="*60)
    print(f"Overall Score: {state.quality_score:.1f}/10")
    print(f"\nCritique:\n{state.critique}")
    print("\n" + "="*60)
    print(f"✅ Assessment completed!")
    print("="*60)


def test_full_chain():
    """Test a chain of nodes: planner -> research_planner -> search_executor -> script_generator"""
    print("🧪 Testing Node Chain: Planner -> Research -> Search -> Script\n")
    
    state = ContentCreationState(
        topic="Blockchain Technology",
        content_type="Twitter Thread",
        style="Engaging and informative",
        target_audience="Tech enthusiasts and crypto investors"
    )
    
    # Step 1: Planner
    print("▶️  Step 1: Running planner...\n")
    planner_node(state)
    
    # Step 2: Research Planner
    print("\n▶️  Step 2: Running research planner...\n")
    research_planner_node(state)
    
    # Step 3: Search Executor
    print("\n▶️  Step 3: Running search executor...\n")
    search_executor_node(state)
    
    # Step 4: Script Generator
    print("\n▶️  Step 4: Running script generator...\n")
    script_generator_node(state)
    
    print("\n" + "="*60)
    print("🎉 FULL CHAIN COMPLETED!")
    print("="*60)
    print(f"Topic: {state.topic}")
    print(f"Script length: {len(state.script.split())} words")
    print(f"Research queries: {len(state.research_queries)}")
    print(f"Key insights: {len(state.key_insights)}")
    print("="*60)


if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("🧪 INDIVIDUAL NODE TESTING UTILITY")
    print("="*60 + "\n")
    
    if len(sys.argv) > 1:
        node_name = sys.argv[1].lower()
        
        if node_name == "script" or node_name == "script_generator":
            test_script_generator()
        elif node_name == "planner":
            test_planner()
        elif node_name == "reflection":
            test_reflection()
        elif node_name == "chain":
            test_full_chain()
        else:
            print(f"❌ Unknown node: {node_name}")
            print("\nAvailable options:")
            print("  - script (or script_generator)")
            print("  - planner")
            print("  - reflection")
            print("  - chain (test multiple nodes)")
    else:
        print("Usage: python test_individual_node.py <node_name>")
        print("\nAvailable options:")
        print("  - script (or script_generator)")
        print("  - planner")
        print("  - reflection")
        print("  - chain (test multiple nodes)")
        print("\nExample:")
        print("  python test_individual_node.py script")
