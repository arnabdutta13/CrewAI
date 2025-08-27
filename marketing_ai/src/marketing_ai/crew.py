from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from pydantic import BaseModel, Field
from crewai_tools import SerperDevTool
from marketing_ai.tools.generate_pdf_tool import GeneratePDFTool


class TrendingTopic(BaseModel):
    name: str = Field(description="The name of the trending topic")
    description: str = Field(description="A brief description of the trending topic")
    relevance: str = Field(description="Why this topic is relevant to marketing")

class TrendingTopicList(BaseModel):
    topics: List[TrendingTopic] = Field(description="A list of trending topics relevant to marketing")

class StrategyTrendingTopic(BaseModel):
    score: str = Field(description="A score indicating the effectiveness of the strategy")
    topics: TrendingTopicList = Field(description="A list of trending topics that support the strategy")

class StrategyTrendingTopicList(BaseModel):
    strategies: List[StrategyTrendingTopic] = Field(description="A list of strategies with their associated trending topics")

class MarketingCampaign(BaseModel):
    name: str = Field(description="The name of the marketing campaign")
    objective: str = Field(description="The main objective of the marketing campaign")
    target_audience: str = Field(description="The target audience for the marketing campaign")
    campaign_details: str = Field(description="Detailed description of the marketing campaign")
    strategy: StrategyTrendingTopic = Field(description="The strategy and its associated trending topics for the campaign")

class MarketingCampaignList(BaseModel):
    campaigns: List[MarketingCampaign] = Field(description="A list of marketing campaigns")

@CrewBase
class MarketingAi():
    """MarketingAi crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml' 

    openaillm: LLM = LLM(model="openai/gpt-4o", temperature=0.7)
    ollamallm: LLM = LLM(model="ollama/deepseek-r1", temperature=0.7, base_url="http://localhost:11434")

    @agent
    def trend_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_researcher'], 
            verbose=True,
            tools=[SerperDevTool()],
            llm=self.openaillm
        )

    @agent
    def strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['strategist'], 
            verbose=True,
            llm=self.openaillm
        )
    
    @agent
    def campaign_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['campaign_designer'],
            verbose=True,
            llm=self.openaillm
        )

    
    @task
    def trend_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_task'], 
            output_pydantic=TrendingTopicList
        )

    @task
    def strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['strategy_task'], 
            output_pydantic=StrategyTrendingTopicList
        )
    
    @task
    def campaign_task(self) -> Task:
        return Task(
            config=self.tasks_config['campaign_task'], 
            output_pydantic=MarketingCampaignList
        )

    @task
    def pdf_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_generation_task'], 
            tools=[GeneratePDFTool()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MarketingAi crew"""
        

        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
