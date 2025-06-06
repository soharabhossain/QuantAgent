# ---------------------------------
# app1.py : Agentic app
# ---------------------------------

# ----------------------------------------------
# Your API keys are stored in a local .env file
# OPENAI_API_KEY = <your_openai_api_key>
# ----------------------------------------------
from dotenv import load_dotenv
load_dotenv()

# ----------------------------------------------
# Other imports
# ----------------------------------------------
from crewai import Crew, Task
from agents.data_collector import DataCollectorAgent
from agents.preprocessor import PreprocessorAgent
from agents.feature_extractor import FeatureExtractorAgent
from agents.model_predictor import ModelPredictorAgent
from agents.risk_assessor import RiskAssessorAgent
from agents.decision_maker import DecisionMakerAgent

# ------------------------------------------------------------
# A function to implement the agentic app 
# ------------------------------------------------------------

def run_app (symbol: str):

    data_collector = DataCollectorAgent().get_agent()
    preprocessor = PreprocessorAgent().get_agent()
    extractor = FeatureExtractorAgent().get_agent()
    predictor = ModelPredictorAgent().get_agent()
    risk_assessor = RiskAssessorAgent().get_agent()
    decision_maker = DecisionMakerAgent().get_agent()

    task1 = Task(
        description=f"Fetch historical and real-time data for {symbol}, including news and sentiment",
        agent=data_collector,
        expected_output="Fetch authentic data for the stock requested and provide the data in a suitable form to be used by other agents for the downstream task"
    )

    task2 = Task(
        description="Clean and normalize the collected data, removing outliers and filling missing values",
        agent=preprocessor,
        depends_on=[task1],
       expected_output="Present the preprocessed data in a suitable form to be used by other agents for the downstream task"
 
    )

    task3 = Task(
        description="Extract predictive features like moving averages, RSI, MACD, and sentiment scores",
        agent=extractor,
        depends_on=[task2],
        expected_output="Provide the features in a suitable form to be used by other agents for the downstream task"
     )

    task4 = Task(
        description="Use ML models (e.g., LSTM) to predict future prices based on engineered features",
        agent=predictor,
        depends_on=[task3],
        expected_output=" Output the predicted price and summary of the analysis in a suitable form to be used by other agents for the downstream task"
 
    )

    task5 = Task(
        description="Assess confidence and risk in the prediction based on historical volatility and uncertainty",
        agent=risk_assessor,
        depends_on=[task4],
        expected_output=" Provide output as a comprehensive and bullet point summary to be used by other agents for the downstream task"
     
    )

    task6 = Task(
        description="Analyze prediction and risk assessment to provide investment recommendation (buy/sell/hold)",
        agent=decision_maker,
        depends_on=[task5],
        expected_output="Provide a detailed analysis as bullet points, provide profit projecttions, mention associated risks. Provde The summary in apresentable form for the end user."
 
    )

    crew = Crew(
        agents=[data_collector, preprocessor, extractor, predictor, risk_assessor, decision_maker],
        tasks=[task1, task2, task3, task4, task5, task6],
        verbose=True
    )

    result = crew.kickoff()
    print("\nFinal Recommendation:")
    print(result)


# ------------------------------------------------------------
# Run the app
if __name__ == "__main__":
    run_app(symbol = "RELIANCE") # stock ticker
    # run_app(symbol = "NIFTY50")    # or index

# ------------------------------------------------------------


