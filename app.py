import streamlit as st
import os
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

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    # Title and description
    st.title("📅AI Project Planner, powered by :red[CrewAI]")
    st.markdown("Create an detailed project plan with resource allocation and a timeline for tasks and milestones using AI agents.")