#!/usr/bin/env python3
"""
Multi-Agent Content Creation Demo - LangGraph

Simple demo showing a multi-agent workflow creating content.

Usage:
    python main_demo.py --topic "Future of AI"
"""

import argparse
import sys

from workflow.graph_builder import execute_content_creation_demo
from utils.display import display_final_output, demo_print


def main():
    """
    Main demo execution - runs the multi-agent workflow
    """
    parser = argparse.ArgumentParser(description='Multi-Agent Content Creation Demo')
    parser.add_argument('--topic', required=True, help='Content topic')
    parser.add_argument('--style', default='Educational', help='Content style')
    
    args = parser.parse_args()
    
    try:
        demo_print(f"\n� Starting Multi-Agent Workflow for: '{args.topic}'\n", "bright_blue", bold=True)
        
        # Execute the workflow
        final_state = execute_content_creation_demo(args.topic, args.style)
        
        # Display results
        display_final_output(final_state)
        
        demo_print("\n✅ Demo Complete!\n", "bright_green", bold=True)
            
    except KeyboardInterrupt:
        demo_print("\n⏹️  Demo interrupted", "yellow")
        sys.exit(0)
        
    except Exception as e:
        demo_print(f"\n❌ Error: {str(e)}", "red")
        sys.exit(1)


if __name__ == "__main__":
    main()