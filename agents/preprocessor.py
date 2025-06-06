
# --- agents/data_collector.py ---

from crewai import Agent

# --- agents/preprocessor.py ---
from crewai import Agent

class PreprocessorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Data Preprocessor",
            goal="Clean and normalize collected stock data, handling missing or noisy values",
            backstory="Experienced in financial data pipelines and preprocessing",
            allow_delegation=False,
        )

    def get_agent(self):
        return self.agent
