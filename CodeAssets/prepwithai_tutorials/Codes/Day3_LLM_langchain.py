from pprint import pprint
from langchain_core.prompts import PromptTemplate
import getpass
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# os.environ["AZURE_OPENAI_API_KEY"] = "your-azure-openai-api-key-here"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource-name.openai.azure.com"


if "AZURE_OPENAI_API_KEY" not in os.environ:
    os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass(
        "Enter your AzureOpenAI API key: "
    )

os.environ["AZURE_OPENAI_API_KEY"]
os.environ["AZURE_OPENAI_ENDPOINT"]


model = os.getenv("MODEL_NAME", "gpt-4o")
temperature = float(os.getenv("MODEL_TEMPERATURE", "0"))
model
temperature

llm = AzureChatOpenAI(
    azure_deployment=model,  # or your deployment
    api_version="2023-06-01-preview",  # or your api version
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

prompt = PromptTemplate(
    template="Write a single catchy tagline for a product called {product}.",
    input_variables=["product"]
)

chain = prompt | llm

ai_response = chain.invoke({"product": "Ai powered Toothbrush"})

pprint(ai_response.content)
