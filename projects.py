import streamlit as st
import os
from typing import List, Dict
from datetime import datetime
import base64
from io import BytesIO

# Function to load custom CSS styles
def load_styles():
    """Load custom CSS styles for the projects section."""
    st.markdown("""
    <style>
    /* Project Card Styling */
    .project-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .project-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
    }

    /* File Download Button Styling */
    .download-button {
        background-color: #02ab21;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .download-button:hover {
        background-color: #ff6ec7;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to create a download link for files
def get_file_download_link(file_path: str, label: str):
    """Create a download link for a file."""
    try:
        with open(file_path, "rb") as file:
            file_bytes = file.read()
        b64 = base64.b64encode(file_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}" class="download-button">{label}</a>'
        return href
    except Exception as e:
        st.error(f"Error generating download link: {e}")
        return ""

# Function to render an individual project card
def render_project_card(project: Dict[str, str]):
    """Render an individual project card."""
    with st.container():
        st.markdown(f"<div class='project-card'>", unsafe_allow_html=True)
        
        # Title and description
        st.markdown(f"### {project['title']}", unsafe_allow_html=True)
        st.markdown(f"**Description:** {project['description']}")
        
        # Categories (badges)
        if 'categories' in project and project['categories']:
            badges_html = " ".join([f"<span style='background-color: #02ab21; color: white; padding: 5px 10px; border-radius: 5px;'>{category}</span>" for category in project['categories']])
            st.markdown(f"{badges_html}", unsafe_allow_html=True)
        
        # Skills covered
        if 'skills' in project and project['skills']:
            skills_list = ", ".join(project['skills'])
            st.markdown(f"**Skills:** {skills_list}")
        
        # Links to code files, PPT, and video presentation
        st.markdown("#### Project Resources")
        col1, col2, col3 = st.columns(3)
        
        # Code file download
        if 'code_file' in project and os.path.exists(project['code_file']):
            with col1:
                st.markdown(get_file_download_link(project['code_file'], "Download Code"), unsafe_allow_html=True)
        else:
            with col1:
                st.info("No code file available.")
        
        # PowerPoint presentation download
        if 'ppt_file' in project and os.path.exists(project['ppt_file']):
            with col2:
                st.markdown(get_file_download_link(project['ppt_file'], "Download PPT"), unsafe_allow_html=True)
        else:
            with col2:
                st.info("No PowerPoint presentation available.")
        
        # Video presentation download or embed
        if 'video_url' in project and project['video_url']:
            with col3:
                st.video(project['video_url'])
        elif 'video_file' in project and os.path.exists(project['video_file']):
            with col3:
                st.video(project['video_file'])
        else:
            with col3:
                st.info("No video presentation available.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Main function to render the projects section
def render_projects_section(projects: List[Dict[str, str]]):
    """Render the projects section."""
    st.markdown("""
    <div id='projects' class='section fade-in'>
        <h2 style='text-align: center;'>🚀 My Projects</h2>
    </div>
    """, unsafe_allow_html=True)
    st.write("Explore my projects and their associated resources.")
    
    # Load custom styles
    load_styles()
    
    # Extract all unique categories for filtering
    all_categories = []
    for project in projects:
        if 'categories' in project:
            all_categories.extend(project['categories'])
    all_categories = sorted(list(set(all_categories)))
    
    # Filters and search section
    st.markdown(" ", unsafe_allow_html=True)
    
    # Search functionality
    search_query = st.text_input("🔍 Search projects", key="project_search", help="Search by title, category, or skills")
    
    # Filter options
    selected_categories = st.multiselect("Filter by Category", options=all_categories, help="Select one or more categories")
    
    # Apply filters and search
    filtered_projects = projects.copy()
    
    # Filter by search query
    if search_query:
        filtered_projects = [
            project for project in filtered_projects if 
            search_query.lower() in project['title'].lower() or
            ('categories' in project and any(search_query.lower() in category.lower() for category in project['categories'])) or
            ('skills' in project and any(search_query.lower() in skill.lower() for skill in project['skills']))
        ]
    
    # Filter by categories
    if selected_categories:
        filtered_projects = [
            project for project in filtered_projects if 
            'categories' in project and any(category in selected_categories for category in project['categories'])
        ]
    
    # Display filtered projects
    if not filtered_projects:
        st.info("No projects match your search criteria. Try adjusting your filters.")
    else:
        st.write(f"Displaying {len(filtered_projects)} project(s)")
        
        for project in filtered_projects:
            render_project_card(project)
            st.markdown("---")

# Sample project data structure
sample_projects = [
    {
        "title": "Oil-Price Prediction",
        "description": "Developed an oil price prediction app for strategic decision-making and increased profitability. Mined over 35 years of oil price data using Python and yfinance, resulting in more than 11,000 values. The app maintains a variance range of 1.2% to 2% in oil price predictions, aiding strategic planning in the oil industry.",
        "duration": "March, 2023 - June, 2023",
        "type": "AI Variant Internship Project",
        "icon": "https://cdn-icons-png.flaticon.com/512/667/667984.png",
        "tags": ["Python", "AI", "Data Science"]
    },
    {
        "title": "Real/Fake News Detection",
        "description": "Developed a user-friendly web app leveraging advanced Natural Language Processing (NLP) techniques. Analyzed and extracted sentiment from a dataset exceeding 80,000 articles. The app offers near-instantaneous verification of news authenticity, delivering reliable results within milliseconds.",
        "duration": "July, 2023 - October, 2023",
        "type": "AI Variant Internship Project",
        "icon": "https://cdn-icons-png.flaticon.com/512/1697/1697488.png",
        "tags": ["NLP", "Machine Learning", "Web Development"]
    },
    {
        "title": "Rating Prediction of Google Play Store Apps",
        "description": "Analyzed a dataset of over 100,000 app entries using Python and sklearn, experimenting with various regression algorithms and optimizing model parameters. The result was a predictive model that achieved an impressive 93% accuracy. This model has since been instrumental in helping app developers identify trending categories and improve their app development strategies.",
        "duration": "Feb, 2022 - Jun, 2022",
        "type": "Final Semester Project",
        "icon": "https://cdn-icons-png.flaticon.com/512/816/816964.png",
        "tags": ["Data Analysis", "Regression", "Python"]
    }
]

# Export the sample_projects variable
__all__ = ['render_projects_section', 'sample_projects']