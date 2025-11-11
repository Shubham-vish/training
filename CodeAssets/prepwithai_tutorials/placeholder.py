import os

# =========================
# 🔐 API Keys & Endpoints
# =========================

# OpenAI / Azure OpenAI Configuration
# For OpenAI or Azure OpenAI auth
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
# Azure OpenAI key
os.environ["AZURE_OPENAI_API_KEY"] = "your-azure-openai-api-key-here"
# Azure endpoint (replace with your endpoint)
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource-name.openai.azure.com"
# Often same as endpoint
os.environ["AZURE_API_BASE"] = "https://your-resource-name.openai.azure.com"
# API version
os.environ["AZURE_API_VERSION"] = "2024-02-15-preview"
# Azure deployment name (e.g., gpt-4o)
os.environ["AZURE_DEPLOYMENT_NAME"] = "your-deployment-name-here"

# General OpenAI Config (if using `openai` package with Azure backend)
# Required for Azure OpenAI
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2024-02-15-preview"
# =========================
# 🔍 Search Service Keys
# =========================
# For SERP API-based tools
os.environ["SERPAPI_API_KEY"] = "your-serpapi-key-here"
# For Tavily search tool (optional)
os.environ["TAVILY_API_KEY"] = "your-tavily-api-key-here"
# =========================
# ⚙️ Model Configuration
# =========================
# Model name or deployment alias
os.environ["MODEL_NAME"] = "gpt-4o"
# Temperature for response creativity
os.environ["MODEL_TEMPERATURE"] = "0"
# =========================
# 🤖 Gemini (Optional)
# =========================
# For Google's Gemini API (if used)
os.environ["GEMINI_API_KEY"] = "your-gemini-api-key-here"
