import streamlit as st
import os
import yaml
from crewai import LLM
from agents import *

# Streamlit Page Config
st.set_page_config(
    page_title = "Project Planner", 
    page_icon = "🛠️", 
    layout = "wide",
    initial_sidebar_state = "expanded")

# Logo
st.logo(
    "https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg",
    link = "https://www.crewai.com/",
    size = "large"
)

col1, col2, col3 = st.columns([1, 9, 1])
with col2:
    # Title and description
    st.title("AI Project Planner, powered by :red[CrewAI]")
    st.markdown("Create an detailed project plan with resource allocation and a timeline for tasks and milestones using AI agents.")
    
# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Model API Configuration")
    st.write("")
    
    model_options = [
        "gpt-4o-mini",
        "gpt-4o",
        "o1",
        "o1-mini", 
        "o1-preview"
        "o3-mini"
    ]
    
    selected_model = st.selectbox("🤖 Select which LLM to use", model_options, key = "selected_model")
    
    with st.expander("🔑 API Keys", expanded = True):
        
        st.info("API keys are stored temporarily in memory and cleared when you close the browser.")
        
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type = "password",
            placeholder = "Enter your OpenAI API key",
            help = "Enter your OpenAI API key"
        )
        
        if openai_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
            
        # serper_api_key = st.text_input(
        #     "Serper API Key",
        #     type = "password",
        #     placeholder = "Enter your Serper API key",
        #     help = "Enter your Serper API key for web search capabilities"
        #     )
        # if serper_api_key:
        #     os.environ["SERPER_API_KEY"] = serper_api_key
    
    st.write("")
    
    with st.expander("ℹ️ About", expanded=False):
        st.markdown(
            """This Project Planner uses advanced AI Agents to help you:
                - Strategically think and breakdown projects into actionable tasks and setting precise timelines.
                - Provide highly accurate time, resource, and effort estimations for each task.
                - Optimize the allocation of tasks for the project by balancing team members' skills, availability, and current workload.
                
                Choose your preferred model and enter the required API keys to get started.""")
        
if not os.environ.get("OPENAI_API_KEY"):
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to get started")
    st.stop()

# if not os.environ.get("SERPER_API_KEY"):
#     st.warning("⚠️ Please enter your Serper API key in the sidebar to get started")
#     st.stop()

# Define file paths for YAML configurations
files = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']

llm = llm = LLM(model = f"openai/{selected_model}")
planner_crew = ProjectPlanner(agents_config, tasks_config, llm)    

# Create two columns for the input section
input_col1, input_col2, input_col3 = st.columns([3, 3, 5])

with input_col1:
    project_topic = st.text_area(
        "Project Topic",
        height = 80,
        placeholder = "Enter the project topic (eg Website, Hiring, Building)"                
    )

with input_col2:
    industry = st.text_area(
        "Industry",
        height = 80,
        placeholder = "Enter the industry (eg Technology, Finance, Construction)"                
    )

with input_col3:
    objective = st.text_area(
        "Project Objective",
        height = 80,
        placeholder = "Enter the project objective (eg Build a website for a small business)"                
    )
    
input_col4, input_col5 = st.columns([3,2])

with input_col4:
    project_requirements = st.text_area(
        "Project Requirements (Brief bullet points)",
        height = 190,
        placeholder = """Enter bullet points of project requirements.
        eg: 
        - Create a responsive design that works well on desktop and mobile devices
        - Implement a modern, visually appealing user interface with a clean look
        - Develop a user-friendly navigation system with intuitive menu structure
        - Include an "About Us" page highlighting the company's history and values
        - Design a "Services" page showcasing the business's offerings with descriptions"""
    )
    
with input_col5:
    team_members = st.text_area(
        "Team Members",
        height = 190,
        placeholder = """Enter the Team Member names are their roles.
        eg:
        - John Doe (Project Manager)
        - Jane Doe (Software Engineer)
        - Bob Smith (Designer)
        - Alice Johnson (QA Engineer)
        - Tom Brown (QA Engineer)
        """
    )
    
generate_button = st.button("🚀 Plan My Project", use_container_width = False, type = "primary")

if generate_button:
    with st.spinner("Generating content... This may take a moment."):
        try:
            project_details = {
                'project_type': project_topic,
                'project_objectives': objective,
                'industry': industry,
                'team_members': team_members,
                'project_requirements': project_requirements
                }
            df_tasks, df_milestones = planner_crew.getPlanning(project_details)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    
    st.markdown("## Task Breakdown:")
    st.dataframe(df_tasks)
    
    st.divider()
    
    st.markdown("## Milestone Details")
    st.dataframe(df_milestones)    
    



# Add footer
st.divider()
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    st.caption("Made with ❤️ using [CrewAI](https://crewai.com) and [Streamlit](https://streamlit.io)")
    st.caption("By [Sharan Shyamsundar](http://sharan1712.github.io/)")
