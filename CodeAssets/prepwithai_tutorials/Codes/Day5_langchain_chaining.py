from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

# Azure OpenAI model setup
model = os.getenv("MODEL_NAME", "gpt-4o")
temperature = float(os.getenv("MODEL_TEMPERATURE", "0"))
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-06-01-preview")

llm = AzureChatOpenAI(
    azure_deployment=model,
    api_version=api_version,
    temperature=temperature
)

# Step 1: Title generation
title_prompt = PromptTemplate.from_template(
    "Write a catchy blog title about {topic}"
)
title_chain = title_prompt | llm | StrOutputParser()

# Step 2: Outline generation


def to_outline_input(title: str) -> dict:
    return {"title": title}


outline_prompt = PromptTemplate.from_template(
    "Write a short outline for a blog titled: {title}"
)
outline_chain = RunnableLambda(to_outline_input) | outline_prompt | llm | StrOutputParser()

# ✅ Chain them together using `|`
full_chain = title_chain | outline_chain

# Run the pipeline
result = full_chain.invoke({"topic": "AI in Education"})

print("\n📝 Blog Outline:\n")
print(result)
