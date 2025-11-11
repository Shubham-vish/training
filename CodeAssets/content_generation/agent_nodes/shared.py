"""Shared imports and utilities for agent nodes."""

from langchain_openai.chat_models.base import BaseChatOpenAI
from Runners.custom_agent_graph_runner import CustomAgentGraphRunner, AgentContext
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel
from typing import List, Dict, Any, Callable
import os
from dotenv import load_dotenv
import json
from pprint import pprint
from IPython.display import Image, display
import logging
import traceback
from SharedCode.agent_utils.agent_utils import AgentContext

class Queries(BaseModel):
    queries: List[str] 