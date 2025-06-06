

# --- agents/model_predictor.py ---
from crewai import Agent

class ModelPredictorAgent:
    def __init__(self):
        self.agent = Agent(
            role="Model Predictor",
            goal="Use ML models to predict stock prices using extracted features",
            backstory="AI expert with experience in time-series modeling",
            allow_delegation=False,
        )

    def get_agent(self):
        return self.agent
