# src/agents/hospital_agent.py

from typing import Dict
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent, AgentExecutor

class HospitalAgent:
    def __init__(self, tools):
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
        prompt = hub.pull("hwchase17/openai-functions-agent")
        self.agent = create_openai_functions_agent(self.llm, tools, prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=tools, verbose=True)

    def run(self, query: str) -> Dict[str, str]:
        result = self.agent_executor.invoke({"input": query})
        tool_used = result.get('intermediate_steps', [])
        if tool_used:
            tool_name = tool_used[0][0].tool
        else:
            tool_name = "No se utilizó ninguna herramienta específica"
        return {
            "output": result["output"],
            "tool_used": tool_name
        }