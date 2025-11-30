# agents/report_agent.py

from core.models import LLMClient
from agents.memory_agent import MemoryAgent


class ReportAgent:
    def __init__(self, llm: LLMClient, memory_agent: MemoryAgent):
        self.llm = llm
        self.memory_agent = memory_agent

    def run(self, farmer_id: str, language: str = "English") -> str:
        history = self.memory_agent.get_history(farmer_id)

        prompt = f"""
You are generating a weekly crop health report for a farmer.

Here is the farmer's recent history (JSON-like, may be empty):
{history}

Write:
1. A short summary of what issues were seen recently.
2. Whether things are improving, stable, or getting worse.
3. Action points for the next week.
4. One motivational line for the farmer.

Respond in {language}. Use short, simple sentences for a smallholder farmer.
Limit to about 200 words.
"""
        return self.llm.generate(prompt)
