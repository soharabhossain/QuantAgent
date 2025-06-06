
# --- agents/data_collector.py ---

from crewai import Agent

class DataCollectorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Data Collector",
            goal="Collect real-time stock, news, and sentiment data for a given company",
            backstory="Expert in financial data APIs and live data extraction",
            allow_delegation=False,
        )

    def get_agent(self):
        return self.agent


