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
        "file": "resumes/fullstack_resume.pdf"
    },
    {
        "title": "Business Analyst",
        "description": "Analytics and insights",
        "file": "resumes/resume_25v3i.pdf"
    },
    {
        "title": "Python Developer",
        "description": "Python programming specialist",
        "file": "resumes/python_developer_resume.pdf"
    },
    {
        "title": "Machine Learning",
        "description": "ML/AI focused projects",
        "file": "resumes/ml_resume.pdf"
    },
    {
        "title": "Research Resume",
        "description": "Academic research focus",
        "file": "resumes/research_resume.pdf"
    }
]
certifications = [
    {
        "title": "Data Science - By Excelr",
        "image": "certifications/Excelr(Data Science)_Certification.jpg",
        "pdf": "certifications/Excelr(Data Science)_Certification.pdf"
    },
    {
        "title": "Business Analytics - Internshala",
        "image": "certifications/Internshala(Business Analytics)_Certification.jpg",
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

# Load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Set background image based on role
def set_background(image_path):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/png;base64,{image_path}");
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Profile section
def profile_section():
    st.markdown("<div class='header'><h1>Syed Shahid Nazeer</h1><h2>Financial Analyst</h2></div>", unsafe_allow_html=True)
    st.markdown("<div id='profile' class='section'><h2>Profile</h2></div>", unsafe_allow_html=True)
    st.write("""
    Aspiring Financial Analyst with hands-on experience in data collection, analysis, and reporting. 
    Proficient in Excel, Power BI, and SQL, with a strong foundation in business application skills. 
    Skilled in providing financial analysis, handling business issues, and delivering actionable insights. 
    Excellent communication and teamwork abilities, with a keen eye for detail and accuracy. 
    Adept at translating complex financial data into strategic recommendations.
    """)

# Projects section
def projects_section():
    st.markdown("<div id='projects' class='section'><h2>Projects</h2></div>", unsafe_allow_html=True)
    projects = [
        {
            "title": "Oil-Price Prediction",
            "description": "Developed an oil price prediction app for strategic decision-making and increased profitability. Mined over 35 years of oil price data using Python and yfinance, resulting in more than 11,000 values. The app maintains a variance range of 1.2% to 2% in oil price predictions, aiding strategic planning in the oil industry.",
            "duration": "March, 2023 - June, 2023",
            "type": "Ai variant Internship Project"
        },
        {
            "title": "Real/Fake News Detection",
            "description": "Developed a user-friendly web app leveraging advanced Natural Language Processing (NLP) techniques. Analyzed and extracted sentiment from a dataset exceeding 80,000 articles. The app offers near-instantaneous verification of news authenticity, delivering reliable results within milliseconds.",
            "duration": "July, 2023 - October, 2023",
            "type": "Ai variant Internship Project"
        },
        {
            "title": "Rating prediction of google play store apps",
            "description": "Analyzed a dataset of over 100,000 app entries using Python and sklearn, experimenting with various regression algorithms and optimizing model parameters. The result was a predictive model that achieved an impressive 93% accuracy. This model has since been instrumental in helping app developers identify trending categories and improve their app development strategies.",
            "duration": "Feb, 2022 - Jun, 2022",
            "type": "Final Semester Project"
        }
    ]
    
    for project in projects:
        st.markdown(f"<h3>{project['title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>{project['type']}</strong> | {project['duration']}</p>", unsafe_allow_html=True)
        st.write(project["description"])
        st.markdown("<hr>", unsafe_allow_html=True)

# Certifications section
def certifications_section():
    render_certifications_section(certifications)

# Contact section
def contact_section():
    display_contact_section(resumes)
# Set background image based on role
def set_background(image_path):
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("data:image/png;base64,{image_path}");
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
# Main function
def main():
    load_css()

    # Role selection navbar
    role = option_menu(
        menu_title=None,
        options=["Data Analyst", "Data Scientist", "Python Developer"],
        icons=["bar-chart-fill", "gear-fill", "code-slash"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(250, 250, 250, 0.8)"},
            "icon": {"color": "orange", "font-size": "calc(16px + 0.5vw)"}, 
            "nav-link": {"font-size": "calc(14px + 0.5vw)", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

    # Set background based on role
    background_images = {
        "Data Analyst": "data_analyst_bg.jpg",
        "Data Scientist": "data_scientist_bg.jpg",
        "Python Developer": "python_developer_bg.jpg"
    }
    set_background(background_images[role])

    # Page selection navbar
    selected = option_menu(
        menu_title=None,
        options=["Profile", "Education", "Skills", "Projects", "Certifications", "Contact"],
        icons=["house", "graduation-cap", "gear", "code-slash", "certificate", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(250, 250, 250, 0.8)"},
            "icon": {"color": "orange", "font-size": "calc(16px + 0.5vw)"}, 
            "nav-link": {"font-size": "calc(14px + 0.5vw)", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#02ab21"},
        }
    )

    # Display the selected page
    if selected == "Profile":
        profile_section()
    elif selected == "Education":
        education_section()
    elif selected == "Skills":
        skills_section()
    elif selected == "Projects":
        projects_section()
    elif selected == "Certifications":
        certifications_section()
    elif selected == "Contact":
        contact_section()

if __name__ == "__main__":
    main()