import streamlit as st
import os
from typing import List, Dict
from datetime import datetime
import base64
from io import BytesIO
from utils import animate_text_letter_by_letter

# Function to load custom CSS styles
def load_styles():
    """Load custom CSS styles for the projects section."""
    st.markdown("""
    <style>
    /* Project Card Styling */
    .project-card {
        background-color: var(--royal-secondary-bg); /* Use royal secondary background */
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px var(--royal-shadow); /* Use royal shadow */
        color: var(--royal-light-text); /* Default text color for card content */
    }
    .project-card h3 {
        color: var(--royal-accent); /* Headings in gold */
    }
    .project-card p b {
        color: var(--royal-accent); /* Bold text in gold */
    }

    /* Project Resources Section */
    .project-resources {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 1rem;
    }

    /* File Download Button Styling (using global .btn) */
    
    /* Search and Filter Controls */
    .stTextInput > div > div > input, .stMultiSelect > div > div {
        background-color: var(--royal-dark) !important;
        color: var(--royal-light-text) !important;
        border: 1px solid var(--royal-accent) !important;
        border-radius: 5px !important;
        box-shadow: inset 0 0 5px rgba(255, 215, 0, 0.2) !important;
    }
    .stTextInput > div > div > input:focus, .stMultiSelect > div > div:focus-within {
        border-color: var(--royal-accent) !important;
        box-shadow: 0 0 10px var(--royal-accent), inset 0 0 8px rgba(255, 215, 0, 0.5) !important;
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
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}" class="btn">{label}</a>'
        return href
    except Exception as e:
        st.error(f"Error generating download link: {e}")
        return ""

# Function to render an individual project card
def render_project_card(project: Dict[str, str]):
    """Render an individual project card."""
    # Start building the HTML for the project card
    card_html = f"""
    <div class='project-card card'>
        <h3>{project['title']}</h3>
        <p><b>Description:</b> {project['description']}</p>
    """

    # Categories (badges)
    if 'categories' in project and project['categories']:
        badges_html = " ".join([f"<span style='background-color: var(--royal-accent); color: var(--royal-dark); padding: 5px 10px; border-radius: 5px;'>{category}</span>" for category in project['categories']])
        card_html += f"<p>{badges_html}</p>"

    # Skills covered
    if 'skills' in project and project['skills']:
        skills_list = ", ".join(project['skills'])
        card_html += f"<p><b>Skills:</b> {skills_list}</p>"

    # Project Resources section
    card_html += "<h4>Project Resources</h4>"
    card_html += "<div class='project-resources'>" # Use flexbox for layout

    # Code file download
    if 'code_file' in project and os.path.exists(project['code_file']):
        card_html += get_file_download_link(project['code_file'], "Download Code")
    else:
        card_html += "<span style='color: var(--royal-light-text); font-size: 0.9em;'>No code file available.</span>"

    # PowerPoint presentation download
    if 'ppt_file' in project and os.path.exists(project['ppt_file']):
        card_html += get_file_download_link(project['ppt_file'], "Download PPT")
    else:
        card_html += "<span style='color: var(--royal-light-text); font-size: 0.9em;'>No PowerPoint presentation available.</span>"

    # Video presentation
    if 'video_url' in project and project['video_url']:
        # Embed external video using iframe
        card_html += f"""
        <div style='flex-basis: 100%; margin-top: 10px;'>
            <iframe src="{project['video_url']}" width="100%" height="315" frameborder="0" allowfullscreen></iframe>
        </div>
        """
    elif 'video_file' in project and os.path.exists(project['video_file']):
        # Provide download link for local video files
        card_html += get_file_download_link(project['video_file'], "Download Video")
    else:
        card_html += "<span style='color: var(--royal-light-text); font-size: 0.9em;'>No video presentation available.</span>"

    card_html += "</div>" # Close project resources div
    card_html += "</div>" # Close project-card div

    st.markdown(card_html, unsafe_allow_html=True)

# Main function to render the projects section
def render_projects_section(projects: List[Dict[str, str]]):
    """Render the projects section."""
    st.markdown(f"""
    <div id='projects' class='section fade-in'>
        <h2 style='text-align: center;'>{animate_text_letter_by_letter("My Projects", tag='span', delay_per_letter=0.10, animation_duration=3.5)}</h2>
        <div class="royal-header-particles">
            <span>🚀</span><span>💡</span><span>🎯</span><span>✅</span><span>🌟</span><span>🏗️</span><span>💻</span><span>📈</span><span>✨</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--royal-light-text);'>Explore my projects and their associated resources.</p>", unsafe_allow_html=True)
    
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