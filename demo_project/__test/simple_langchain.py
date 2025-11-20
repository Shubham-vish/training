

import os
from typing import Optional, Type, TypeVar
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage



DIRECT_ENV_PATH = "/home/shubham/training/demo_project/.env"
load_dotenv(dotenv_path=DIRECT_ENV_PATH, override=True)



llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            temperature=0.7,
            max_tokens=2000
        )

res = llm.invoke([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is General weather in India?"),
])

from pprint import  pprint
pprint(res)

res.content

messages = [
    SystemMessage(content="You are student, When I ask you who are you say you are student"),HumanMessage(content="Who Are you?")
]
aimessage = llm.invoke(messages)


# llm.invoke([HumanMessage(content="Who Are you?")])


messages.append(aimessage)

messages.append(HumanMessage(content="What was my last question? and you answered"))


llm.invoke(messages)
llm.invoke([ HumanMessage(content="Who Are you?")])


llm.invoke([HumanMessage(content="Who are you?")])