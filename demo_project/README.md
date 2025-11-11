# Multi-Agent Content Creation Demo
## CrewAI + LangGraph Integration

This demo showcases a content creation multi-agent system that integrates:
- **CrewAI**: Role-based agent collaboration patterns
- **LangGraph**: Workflow orchestration and state management

## Demo Structure

### 1. Framework Introduction (8 minutes)
- CrewAI role-based collaboration
- LangGraph workflow orchestration  
- Brief AutoGen comparison
- Integration benefits

### 2. Working Demo (15 minutes)
- Live content creation workflow
- Agent role demonstrations
- State management visualization
- Real-time results

### 3. Architecture Deep-dive (5 minutes)
- Technical implementation
- Integration patterns
- Best practices

## Agent Roles

1. **Content Manager** (Planner) - Strategy and planning
2. **Research Specialist** (Research Planner) - Research strategy
3. **Data Analyst** (Search Executor) - Information gathering  
4. **Content Writer** (Script Generator) - Content creation
5. **Quality Assurance** (Reflection) - Review and critique
6. **SEO Specialist** (Hashtag Generator) - Optimization
7. **Marketing Specialist** (CTA Generator) - Call-to-action

## Files Structure

```
demo_project/
├── README.md
├── requirements.txt
├── main_demo.py              # Main demo execution
├── agents/
│   ├── __init__.py
│   ├── crew_roles.py         # CrewAI role definitions
│   ├── langgraph_nodes.py    # LangGraph node implementations
│   └── integration.py        # CrewAI + LangGraph integration
├── workflow/
│   ├── __init__.py
│   ├── graph_builder.py      # LangGraph workflow definition
│   └── state_schema.py       # State management
├── utils/
│   ├── __init__.py
│   ├── display.py            # Demo visualization helpers
│   └── sample_data.py        # Backup demo data
└── presentation/
    ├── slides.md             # Slide content
    ├── script.md             # Demo script with timing
    └── diagrams/             # Workflow visualizations
```

## Quick Start

```bash
pip install -r requirements.txt
python main_demo.py --topic "Future of Remote Work"
```