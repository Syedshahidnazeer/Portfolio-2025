import streamlit as st
from streamlit_lottie import st_lottie
import requests
import os
from PIL import Image
from typing import List, Dict
from streamlit_option_menu import option_menu
from certifications import render_certifications_section
from contacts import display_contact_section
from skills import skills_section
from education import education_section
from profile import profile_section
from projects import project_section

# Page config
st.set_page_config(page_title="Syed Shahid Nazeer - Financial Analyst", page_icon="📊", layout="wide")

resumes = [
    {
        "title": "Data Science Resume",
        "description": "Focused on ML and AI projects",
        "file": "resumes/resume_25v1.pdf"
    },
    {
        "title": "Full Stack Developer",
        "description": "Web development expertise",
        "file": "resumes/resume_25v2.pdf"
    },
    {
        "title": "Business Analyst",
        "description": "Analytics and insights",
        "file": "resumes/resume_25v3a.pdf"
    },
    {
        "title": "Python Developer",
        "description": "Python programming specialist",
        "file": "resumes/resume_25v3i.pdf"
    },
    {
        "title": "Machine Learning",
        "description": "ML/AI focused projects",
        "file": "resumes/resume_25v4b.pdf"
    },
    {
        "title": "Research Resume",
        "description": "Academic research focus",
        "file": "resumes/resume_25v5b.pdf"
    },
    {
        "title": "Another Full Stack Developer Resume",
        "description": "Additional web development expertise",
        "file": "resumes/resume_25v6a.pdf"
    },
    {
        "title": "Another Business Analyst Resume",
        "description": "Further analytics and insights",
        "file": "resumes/resume_25v6i.pdf"
    }
]

certifications = [
    {
        "title": "Data Science - By Excelr",
        "pdf": "certifications/Excelr(Data Science)_Certification.pdf"
    },
    {
        "title": "Business Analytics - Internshala",
        "pdf": "certifications/Internshala(Business Analytics)_Certification.pdf"
    }
]

# Load CSS
def load_css():
    st.markdown("""
    <style>
    .big-font {font-size:calc(30px + 2vw) !important; color: #4A4A4A;}
    .medium-font {font-size:calc(20px + 1vw) !important; color: #4A4A4A;}
    .small-font {font-size:calc(16px + 0.5vw) !important; color: #4A4A4A;}
    .skill-item {font-size: calc(16px + 0.5vw); color: #4A4A4A; padding: 10px; border-radius: 5px; background: rgba(250, 250, 250, 0.8);}
    .stSelectbox {max-width: 300px;}
    @media (max-width: 768px) {
        .responsive-container {
            flex-direction: column;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Main function
def main():
    load_css()
    
    # Check if the session state is initialized
    if 'selected' not in st.session_state:
        st.session_state.selected = "Profile"
    
    # Page selection navbar
    st.session_state.selected = option_menu(
        menu_title=None,
        options=["Profile", "Education", "Skills", "Projects", "Certifications", "Contact"],
        icons=["house", "graduation-cap", "gear", "code-slash", "certificate", "envelope"],
        menu_icon="cast",
        default_index=0 if st.session_state.selected == "Profile" else 1,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(250, 250, 250, 0.8)"},
            "icon": {"color": "orange", "font-size": "calc(16px + 0.5vw)"}, 
            "nav-link": {"font-size": "calc(14px + 0.5vw)", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

    # Display the selected page
    if st.session_state.selected == "Profile":
        profile_section()
    elif st.session_state.selected == "Education":
        education_section()
    elif st.session_state.selected == "Skills":
        skills_section()
    elif st.session_state.selected == "Projects":
        project_section()
    elif st.session_state.selected == "Certifications":
        render_certifications_section(certifications)
    elif st.session_state.selected == "Contact":
        display_contact_section(resumes)

if __name__ == "__main__":
    main()