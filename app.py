import streamlit as st
from streamlit_lottie import st_lottie
import requests
import os
from typing import List, Dict
from streamlit_option_menu import option_menu

# Import module functions
from certifications import render_certifications_section, sample_certifications
from contacts import render_contact_section, sample_resumes
from skills import render_skills_section, sample_skills
from image_utils import get_image_base64
from education import education_section
from profile import profile_section
from projects import render_projects_section, sample_projects
from experience import render_experience_section
from experience_data import sample_experiences

# Page configuration
st.set_page_config(
    page_title="Syed Shahid Nazeer - Financial Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clear any previous app state issues
if "navbar_key" not in st.session_state:
    st.session_state.navbar_key = 0

if 'selected' not in st.session_state:
    st.session_state.selected = "Profile"

# Function to load Lottie animations
def load_lottie_animation(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

# Base CSS for the entire application
def load_base_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Define callback for navbar selection
def on_navbar_change():
    st.session_state.navbar_key += 1

# Main application function
def main():
    # Load base CSS first
    load_base_css()

    # Create a container for the navbar with fixed styling
    with st.container():
        st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
        
        # Simple and reliable navigation
        selected = option_menu(
            menu_title=None,
            options=["Profile", "Education", "Skills", "Projects", "Certifications", "Experience", "Contact"],
            icons=["house", "book", "gear", "code-slash", "award", "briefcase", "envelope"],
            default_index=["Profile", "Education", "Skills", "Projects", "Certifications", "Experience", "Contact"].index(st.session_state.selected),
            orientation="horizontal",
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "#02ab21", "font-size": "1rem"},
                "nav-link": {
                    "font-size": "0.9rem",
                    "text-align": "center",
                    "margin": "0",
                    "padding": "0.5rem 1rem",
                    "--hover-color": "#f0f0f0"
                },
                "nav-link-selected": {"background-color": "#02ab21", "color": "white", "font-weight": "bold"},
            },
            key=f"navbar_{st.session_state.navbar_key}"
        )
        
        # Update session state with current selection
        st.session_state.selected = selected
        st.markdown('</div>', unsafe_allow_html=True)

    # Social Media Links with Hover Effects
    st.markdown("""
    <style>
    .social-links a {
        margin-right: 10px;
        font-size: 20px;
        color: var(--primary-color);
        text-decoration: none;
        transition: transform 0.3s ease, color 0.3s ease;
    }
    .social-links a:hover {
        transform: scale(1.2);
        color: #ff6ec7;
    }
    </style>
    <div class='social-links'>
        <a href="https://www.linkedin.com/in/shahidnazeersyed/" target="_blank" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
        <a href="https://github.com/Syedshahidnazeer" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
    </div>
    """, unsafe_allow_html=True)

    # Create a container for the main content
    with st.container():
        st.markdown('<div class="main-content fade-in">', unsafe_allow_html=True)
        
        # Display the selected section content
        if st.session_state.selected == "Profile":
            profile_section()
        elif st.session_state.selected == "Education":
            education_section()
        elif st.session_state.selected == "Skills":
            render_skills_section(sample_skills, get_image_base64)
        elif st.session_state.selected == "Projects":
            render_projects_section(sample_projects)
        elif st.session_state.selected == "Certifications":
            render_certifications_section(sample_certifications)
        elif st.session_state.selected == "Experience":
            render_experience_section(sample_experiences)
        elif st.session_state.selected == "Contact":
            render_contact_section(sample_resumes)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()