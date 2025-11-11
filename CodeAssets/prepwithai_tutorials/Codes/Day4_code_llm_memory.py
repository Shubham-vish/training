from langchain_core.prompts import PromptTemplate
import getpass
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
import sys
from pprint import pprint
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# Load environment variables
load_dotenv(override=True)


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

response = llm.invoke("I am AiLead, Leading AI Agent Development")

pprint(response.content)

response = llm.invoke("Who Am I?")
pprint(response.content)

# Above example showed that by default, the LLM does not remember the previous conversation.
# 
# To enable memory, we can use the `ConversationChain` class from Langchain.
# 



messages = []

messages.append(HumanMessage(
    content="I am AiLead, Leading AI Agent Development"))

response = llm.invoke(messages)

messages.append(response)

pprint(messages)


messages.append(HumanMessage(content="Who Am I?"))


response = llm.invoke(messages)
pprint(response.content)