# --- agents/risk_assessor.py ---
from crewai import Agent

class RiskAssessorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Risk Assessor",
            goal="Evaluate the confidence level and potential risk in stock price predictions",
            backstory="Risk management specialist skilled in financial uncertainty analysis",
            allow_delegation=False,
        )

    def get_agent(self):
        return self.agent
