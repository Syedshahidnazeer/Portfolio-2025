import streamlit as st
from streamlit_lottie import st_lottie
import requests
import plotly.express as px
import pandas as pd
import base64
import os

# === Utility Functions ===
@st.cache_data
def load_lottieurl(url):
    """Load Lottie animations from URL."""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

@st.cache_data
def get_image_base64(image_path):
    """Encodes an image to base64 for embedding in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image not found: {image_path}")
        return ""

def load_image(path):
    """Load images with error handling."""
    try:
        return st.image(path, width=50)
    except FileNotFoundError:
        st.write("Image Unavailable")

# === Custom CSS Styling ===
def load_styles():
    """Load custom CSS styles for the education section."""
    st.markdown("""
        <style>
        /* General Styling */
        hr {
            border: none;
            border-top: 2px solid #ff00ff;
            margin: 20px 0;
        }
        .header-description {
            text-align: center;
            font-size: 18px;
            margin-bottom: 20px;
        }
        /* Education Card Styling */
        .education-card {
            background-color: var(--section-background-color); /* Use the same white as sections */
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 20px; /* Space between cards */
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* Subtle shadow */
            transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transition for hover */
            display: flex; /* To align logo and text */
            align-items: flex-start; /* Align items to the top */
        }
        .education-card:hover {
            transform: translateY(-5px); /* Lift effect */
            box-shadow: 0 8px 12px rgba(0,0,0,0.2); /* Enhanced shadow on hover */
        }
        .education-logo-container {
            flex-shrink: 0; /* Prevent logo from shrinking */
            margin-right: 20px; /* Space between logo and text */
        }
        .education-details-content {
            flex-grow: 1; /* Allow content to take available space */
        }
        </style>
    """, unsafe_allow_html=True)

# === Data Visualization ===
@st.cache_data
def create_education_chart(theme_mode="light"):
    """Create an interactive academic performance chart."""
    education_data = pd.DataFrame({
        'Year': [2018, 2019, 2020, 2021, 2022],
        'SGPA': [7.0, 7.2, 7.5, 8.0, 9.18]
    })
    
    fig = px.line(
        education_data, 
        x='Year', 
        y='SGPA', 
        title='Academic Performance',
        labels={'SGPA': 'SGPA'},
        markers=True,
        template="plotly_dark" if theme_mode == "dark" else "plotly"
    )
    fig.update_traces(hovertemplate='Year: %{x}<br>SGPA: %{y}')
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    return fig

# === Education Section ===
def display_education_details():
    """Display detailed education information."""
    # B.Tech details
    aits_logo_base64 = get_image_base64("logos/aits_logo.png")
    jntua_logo_base64 = get_image_base64("logos/jntua_logo.png")

    st.markdown(f"""
    <div class="education-card">
        <div class="education-logo-container">
            <img src="data:image/png;base64,{aits_logo_base64}" width="50" style="margin-bottom: 10px;">
            <img src="data:image/png;base64,{jntua_logo_base64}" width="50">
        </div>
        <div class="education-details-content">
            <h3>🎓 B.Tech - CSE</h3>
            <p><b>Institution</b>: Annamacharya Institute Of Technology & Sciences, Kadapa</p>
            <p><b>University (Affiliated)</b>: Jawaharlal Nehru Technological University, Anantapur</p>
            <p><b>Duration</b>: August 2018 - August 2022</p>
            <p><b>Percentage of Marks</b>: 67.98%</p>
            <p><b>CGPA</b>: 6.98 | <b>Final Semester SGPA</b>: 9.18</p>
            <p><b>Description</b>: During my undergraduate studies, I developed strong foundations in computer science and engineering principles, with a focus on software development, data structures, and algorithms.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Higher Secondary details
    bie_ap_logo_base64 = get_image_base64("logos/bie_ap_logo.png")
    st.markdown(f"""
    <div class="education-card">
        <div class="education-logo-container">
            <img src="data:image/png;base64,{bie_ap_logo_base64}" width="50">
        </div>
        <div class="education-details-content">
            <h3>📚 Higher Secondary - 12th Class (PCM)</h3>
            <p><b>Institution</b>: Sri Chaitanya Junior College, Kadapa</p>
            <p><b>Board</b>: Board of Intermediate Education, Andhra Pradesh</p>
            <p><b>Duration</b>: April 2018</p>
            <p><b>Percentage of Marks</b>: 74.8%</p>
            <p><b>Description</b>: In high school, I studied Physics, Chemistry, and Mathematics, which provided me with a strong analytical and problem-solving skill set.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Secondary details
    bse_ap_logo_base64 = get_image_base64("logos/bse_ap_logo.png")
    st.markdown(f"""
    <div class="education-card">
        <div class="education-logo-container">
            <img src="data:image/png;base64,{bse_ap_logo_base64}" width="50">
        </div>
        <div class="education-details-content">
            <h3>🏫 Secondary - 10th Class</h3>
            <p><b>Institution</b>: Nagarjuna Model School, Maruthinagar, Kadapa</p>
            <p><b>Board</b>: Board of Secondary Education, Andhra Pradesh</p>
            <p><b>Duration</b>: March 2016</p>
            <p><b>GPA</b>: 8.8</p>
            <p><b>Description</b>: In secondary school, I excelled in my studies, particularly in subjects like Mathematics and Science, which laid the groundwork for my future academic pursuits.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def education_section():
    """Main function to render the education section."""
    # Load custom styles
    load_styles()

    # Section Header with Animation
    st.markdown("""
    <div id='education' class='section fade-in'>
        <h2 style='text-align: center;'>Education</h2>
    </div>
    """, unsafe_allow_html=True)

    # Load Lottie animation and chart
    header_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    education_chart = create_education_chart(st.session_state.get("theme_mode", "light"))

    if header_animation:
        col1, col2 = st.columns([1, 2])
        with col1:
            st_lottie(header_animation, height=200, key="education_header_animation")
        with col2:
            st.plotly_chart(education_chart, use_container_width=True)

    st.markdown("""
    <div class='header-description'>
        <p>This section highlights my educational background, showcasing the institutions I've attended, the qualifications I've earned, and my academic performance over the years.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Display detailed education information
    display_education_details()