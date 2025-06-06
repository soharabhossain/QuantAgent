# --- agents/decision_maker.py ---
from crewai import Agent

class DecisionMakerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Investment Decision Maker",
            goal="Analyze predicted stock trends and risk to make buy/hold/sell recommendations",
            backstory="Financial strategist skilled in portfolio management and investment planning",
            allow_delegation=False,
        )

    def get_agent(self):
        return self.agent
