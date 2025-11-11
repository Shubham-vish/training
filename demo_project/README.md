# Multi-Agent Content Creation System

A LangGraph-based multi-agent system that creates high-quality content through specialized AI agents working together.

## Quick Start

1. **Create and activate a virtual environment:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. **Run the demo:**
```bash
python main_demo.py --topic "Future of AI"
```

## What It Does

The system uses 7 specialized agents to create content:

1. **Planner** - Creates content strategy
2. **Research Planner** - Designs research approach
3. **Search Executor** - Gathers information
4. **Script Generator** - Writes the content
5. **Reflection** - Reviews quality (conditional routing)
6. **Hashtag Generator** - Optimizes for SEO
7. **CTA Generator** - Creates call-to-action

## Key Features

- **State Management**: Shared state flows through all agents
- **Conditional Routing**: Quality check determines if revision is needed
- **Modular Design**: Each agent in separate file
- **LangGraph Orchestration**: Graph-based workflow with conditional edges

## Project Structure

```
demo_project/
├── agents/              # Individual agent implementations
│   ├── planner.py
│   ├── research_planner.py
│   ├── search_executor.py
│   ├── script_generator.py
│   ├── reflection.py
│   ├── hashtag_generator.py
│   └── cta_generator.py
├── workflow/            # LangGraph workflow
│   ├── graph_builder.py
│   └── state_schema.py
├── utils/               # Helper utilities
│   ├── display.py
│   └── llm_client.py
└── main_demo.py         # Main entry point
```

## Usage Examples

```bash
# Basic demo
python main_demo.py --topic "Future of AI"

# With custom style
python main_demo.py --topic "Climate Change" --style "Professional"
```

## Technologies

- **LangGraph**: Workflow orchestration and state management
- **LangChain**: LLM integration
- **OpenAI/Azure OpenAI**: Language model provider
- **Python 3.10+**: Core language

## Demo Output

The system generates:
- Complete content script
- Strategic hashtags
- Compelling call-to-action
- Quality score and metrics
