import pandas as pd
from typing import List
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew

class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the task")
    estimated_time_hours: float = Field(..., description = "Estimated time to complete the task in hours")
    required_resources: List[str] = Field(..., description = "List of resources required to complete the task")

class Milestone(BaseModel):
    milestone_name: str = Field(..., description = "Name of the milestone")
    tasks: List[str] = Field(..., description = "List of task IDs associated with this milestone")

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(..., description = "List of tasks with their estimates")
    milestones: List[Milestone] = Field(..., description = "List of project milestones")

class ProjectPlanner:
    
    def __init__(self, agents_config, tasks_config, llm):
        
        # Creating Agents
        project_planning_agent = Agent(config = agents_config['project_planning_agent'], llm = llm)
        estimation_agent = Agent(config = agents_config['estimation_agent'], llm = llm)
        resource_allocation_agent = Agent(config = agents_config['resource_allocation_agent'], llm = llm)

        # Creating Tasks
        task_breakdown = Task(config = tasks_config['task_breakdown'], agent = project_planning_agent)
        time_resource_estimation = Task(config = tasks_config['time_resource_estimation'], agent = estimation_agent)
        resource_allocation = Task(config = tasks_config['resource_allocation'], agent = resource_allocation_agent,
                                   output_pydantic = ProjectPlan # This is the structured output we want
                                   )

        # Creating Crew
        self.crew = Crew(
            agents = [project_planning_agent, estimation_agent, resource_allocation_agent],
            tasks = [task_breakdown, time_resource_estimation, resource_allocation],
            verbose = True
            )
    
    def getPlanning(self, project_details):
        
        results = self.crew.kickoff(inputs = project_details)
        task_breakdown = results.pydantic.model_dump()['tasks']
        df_tasks = pd.DataFrame(task_breakdown)
        milestones = results.pydantic.model_dump()['milestones']
        df_milestones = pd.DataFrame(milestones)
        
        return df_tasks, df_milestones