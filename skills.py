import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Skills section with logos and detailed information
def skills_section():
    st.markdown("<div id='skills' class='section'><h2>Skills</h2></div>", unsafe_allow_html=True)

    # Load Lottie animation for the section header
    header_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    if header_animation:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("<div class='header-description'><p>This section showcases the skills and tools that are vital in the field of Data Science and Analytics. Below, you'll find detailed information on each tool, its current version, functionality, and uses in various domains.</p></div>", unsafe_allow_html=True)
        with col2:
            st_lottie(header_animation, height=200, key="skills_header_animation")

    skills = [
        {
            "name": "MS Excel",
            "logo_path": "logos/excel_logo.png",
            "version": "Microsoft Excel 2021",
            "functionality": "Spreadsheet software used for data entry, manipulation, analysis, and visualization.",
            "use": "Widely used for financial analysis, data tracking, and simple statistical analysis."
        },
        {
            "name": "MySQL",
            "logo_path": "logos/mysql_logo.png",
            "version": "MySQL 8.0",
            "functionality": "Database management system used for storing, retrieving, and managing data in relational databases.",
            "use": "Essential for managing large datasets, performing complex queries, and ensuring data integrity in data science projects."
        },
        {
            "name": "Power BI",
            "logo_path": "logos/powerbi_logo.png",
            "version": "Power BI 2021",
            "functionality": "Data visualization tool used for creating interactive and shareable dashboards.",
            "use": "Used to visualize complex datasets, identify trends, and aid in data-driven decision making."
        },
        {
            "name": "Analytics and Statistics",
            "logo_path": "logos/analytics_logo.png",
            "version": "Various tools and packages",
            "functionality": "Techniques and tools for analyzing data and drawing statistical inferences.",
            "use": "Used for predictive modeling, hypothesis testing, and data-driven insights in various domains."
        },
        {
            "name": "Python",
            "logo_path": "logos/python_logo.png",
            "version": "Python 3.9",
            "functionality": "High-level programming language with extensive libraries for data analysis and machine learning.",
            "use": "Widely used for data manipulation, statistical analysis, machine learning, and automation."
        }
    ]

    for skill in skills:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(skill["logo_path"], width=100)
        with col2:
            st.markdown(f"<div class='skill-item'><strong>{skill['name']}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"**Version:** {skill['version']}", unsafe_allow_html=True)
            st.markdown(f"**Functionality:** {skill['functionality']}", unsafe_allow_html=True)
            st.markdown(f"**Uses in Data Science and Analytics:** {skill['use']}", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
