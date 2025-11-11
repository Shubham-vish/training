# Demo Setup & Execution Guide
## Multi-Agent Content Creation System Demo

### 🚀 Quick Setup Instructions

#### 1. Environment Setup
```bash
cd /home/shubham/training/demo_project
uv sync  # Install all dependencies
```

#### 2. Configure Azure OpenAI (.env file)
```bash
# Copy the template and add your credentials
cp .env.example .env
# Edit .env with your Azure OpenAI details
```

Required environment variables:
- `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key  
- `AZURE_OPENAI_DEPLOYMENT_NAME` - Your GPT-4 deployment name

#### 3. Demo Execution Commands

**Full Presentation (30 minutes):**
```bash
uv run python main_demo.py --topic "Future of Remote Work" --full-presentation
```

**Demo Only (10 minutes):**
```bash
uv run python main_demo.py --topic "AI in Healthcare" --demo-only
```

**Test LLM Connection:**
```bash
uv run python utils/llm_client.py
```

### 🎯 Demo Topics (Tested)
- "Future of Remote Work"
- "AI in Healthcare"  
- "Digital Transformation"
- "Cybersecurity in 2024"
- "Sustainable Technology"

### 🛡️ Backup Options

#### Option 1: Sample Data Fallback (Automatic)
The demo automatically uses high-quality sample data if:
- Azure OpenAI is not configured
- API calls fail during demo
- Network connectivity issues

#### Option 2: Offline Demo Mode
```bash
# Force offline mode with sample data
export USE_SAMPLE_DATA_FALLBACK=true
uv run python main_demo.py --topic "Future of Remote Work" --demo-only
```

#### Option 3: Pre-recorded Demo
- Video recording available in `/presentation/backup_video.mp4`
- Screenshots in `/presentation/backup_screenshots/`

### ⚡ Performance Tips

#### For Live Demo:
- Test internet connection beforehand
- Have backup topics ready
- Practice with actual audience timing
- Keep VS Code terminal large and readable

#### For Azure OpenAI:
- Ensure sufficient quota/rate limits
- Test connection 10 minutes before demo
- Have backup API keys if possible

### 🎬 Demo Script Timing

| Section | Duration | Key Points |
|---------|----------|------------|
| Hook & Intro | 3-4 min | Strong opening, learning objectives |
| Framework Education | 8 min | CrewAI, LangGraph, integration benefits |
| Live Demo | 10-12 min | Real workflow execution with commentary |
| Architecture Deep-dive | 5 min | Technical implementation details |
| Q&A & Wrap-up | 3-5 min | Key takeaways, next steps |

### 🔧 Troubleshooting

#### Common Issues:
1. **Import Errors**: Ensure you're in the correct directory and virtual environment
2. **LLM Connection Fails**: Check .env configuration, will auto-fallback to samples
3. **Demo Runs Too Fast**: Increase delay times in `utils/sample_data.py`
4. **Display Issues**: Ensure terminal supports Unicode/colors

#### Emergency Fixes:
```bash
# Reset demo environment
rm -rf .venv
uv sync
uv run python utils/llm_client.py  # Test setup

# Force sample data mode
export USE_SAMPLE_DATA_FALLBACK=true
```

### 📊 Success Metrics

**Technical Success:**
- ✅ All 7 agents execute successfully
- ✅ Quality score above 7.0
- ✅ Complete content package generated
- ✅ No errors or crashes

**Audience Engagement:**
- ✅ Questions during/after demo
- ✅ Interest in implementation details
- ✅ Requests for code/resources
- ✅ Discussion about their use cases

### 🎯 Key Demo Messages

1. **Multi-agent systems are powerful** for complex workflows
2. **Framework integration** provides best-of-both-worlds benefits
3. **Role-based design** improves quality and maintainability  
4. **Working examples** are the best learning tools

### 🚀 Post-Demo Actions

**For Interested Audience:**
- Share GitHub repository link
- Provide learning resource list
- Offer follow-up consultation
- Connect on LinkedIn for continued discussion

**For Interview Panel:**
- Demonstrate deep technical knowledge
- Show teaching ability and engagement
- Provide practical, working solutions
- Display enthusiasm for the technology