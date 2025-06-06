# --- agents/feature_extractor.py ---
from crewai import Agent

class FeatureExtractorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Feature Extractor",
            goal="Engineer predictive features like technical indicators and sentiment scores",
            backstory="Quantitative analyst with expertise in feature engineering",
            allow_delegation=False,
        )

    def get_agent(self):
        return self.agent
