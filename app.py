import streamlit as st
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
from profiles import profile_section
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

    # Force background color to eliminate white corners and ensure theme consistency
    st.markdown(r'''
    <style>
        body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #000033 !important;
        }
    </style>
    ''', unsafe_allow_html=True)

    # Global Particle Animation Container
    st.markdown("""
    <div class="global-particles-container">
        <span class="golden-particle meteor" style="top: 10%; left: 15%; animation-delay: 0s; --duration: 5s; --end-x: 100px; --end-y: 800px;"></span>
        <span class="golden-particle star" style="top: 50%; left: 80%; animation-delay: 1s; --duration: 4s;"></span>
        <span class="golden-particle dust" style="top: 30%; left: 5%; animation-delay: 2s; --duration: 6s; --drift-x: 50px; --drift-y: 100px;"></span>
        <span class="golden-particle meteor" style="top: 70%; left: 30%; animation-delay: 3s; --duration: 5.5s; --end-x: -50px; --end-y: 700px;"></span>
        <span class="golden-particle star" style="top: 20%; left: 60%; animation-delay: 4s; --duration: 4.5s;"></span>
        <span class="golden-particle dust" style="top: 90%; left: 45%; animation-delay: 5s; --duration: 7s; --drift-x: -80px; --drift-y: -120px;"></span>
        <span class="golden-particle meteor" style="top: 40%; left: 95%; animation-delay: 6s; --duration: 6s; --end-x: -150px; --end-y: 600px;"></span>
        <span class="golden-particle star" style="top: 5%; left: 40%; animation-delay: 7s; --duration: 3.8s;"></span>
        <span class="golden-particle dust" style="top: 65%; left: 10%; animation-delay: 8s; --duration: 6.5s; --drift-x: 120px; --drift-y: -80px;"></span>
    </div>
    """, unsafe_allow_html=True)

    # Simple and reliable navigation
    selected = option_menu(
        menu_title=None,
        options=["Profile", "Education", "Skills", "Projects", "Certifications", "Experience", "Contact"],
        icons=["house", "book", "gear", "code-slash", "award", "briefcase", "envelope"],
        default_index=["Profile", "Education", "Skills", "Projects", "Certifications", "Experience", "Contact"].index(st.session_state.selected),
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0.5rem 1rem",
                "background-color": "#00004d",
                "border-radius": "0px",
                "width": "100%",
                "margin": "0 auto",
                "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.5)",
                "border": "1px solid #FFD700"
            },
            "icon": {
                "color": "#F0F8FF",
                "font-size": "20px"
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px 5px",
                "padding": "8px 15px",
                "--hover-color": "#000033",
                "color": "#F0F8FF",
                "border-radius": "0px"
            },
            "nav-link-selected": {
                "background-color": "#FFD700",
                "color": "#000033",
                "font-weight": "bold",
                "border-radius": "0px"
            },
        },
        key=f"navbar_{st.session_state.navbar_key}"
    )
    
    # Update session state with current selection
    st.session_state.selected = selected

    # Social Media Links with Hover Effects
    st.markdown('''
    <style>
    .social-links a {
        margin-right: 10px;
        font-size: 20px;
        color: var(--royal-accent); /* Use royal accent color */
        text-decoration: none;
        transition: transform 0.3s ease, color 0.3s ease;
    }
    .social-links a:hover {
        transform: scale(1.2);
        color: var(--royal-light-text); /* Lighter color on hover */
    }
    </style>
    <div class=\'social-links\'>
        <a href="https://www.linkedin.com/in/shahidnazeersyed/" target="_blank" title="LinkedIn"><i class="fab fa-linkedin"></i></a>
        <a href="https://github.com/Syedshahidnazeer" target="_blank" title="GitHub"><i class="fab fa-github"></i></a>
    </div>
    ''', unsafe_allow_html=True)

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
