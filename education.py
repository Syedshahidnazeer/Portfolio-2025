import streamlit as st
from streamlit_lottie import st_lottie
import requests
import plotly.express as px
import pandas as pd

# Function to load Lottie animations
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Function to create education chart
def create_education_chart():
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
        template="plotly_dark" if st.session_state.get("theme_mode", "light") == "dark" else "plotly"
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )
    return fig

# Load custom CSS styles
def load_styles():
    """Load custom CSS styles for the education section."""
    st.markdown("""
        <style>
        /* Synthwave84 Font */
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        
        /* General Styling */
        body {
            background-color: #2e2e2e;
            color: #f3f3f3;
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Press Start 2P', cursive;
            color: #ff6ec7;
            text-shadow: 0 0 8px #ff00ff, 0 0 16px #ff00ff;
        }
        p {
            font-size: 16px;
            color: #dcdcdc;
            line-height: 1.6;
        }
        hr {
            border: none;
            border-top: 2px solid #ff00ff;
            margin: 20px 0;
        }
        .header-description {
            text-align: center;
            font-size: 18px;
            color: #dcdcdc;
            margin-bottom: 20px;
        }
        .glow {
            animation: glow 1.5s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from {
                text-shadow: 0 0 8px #ff00ff, 0 0 16px #ff00ff;
            }
            to {
                text-shadow: 0 0 16px #ff00ff, 0 0 32px #ff00ff;
            }
        }
        </style>
    """, unsafe_allow_html=True)

# Education section with logos, detailed information, and animations
def education_section():
    # Load custom styles
    load_styles()

    # Section Header with Animation
    st.markdown("""
    <div id='education' class='section fade-in'>
        <h2 class='glow' style='text-align: center; margin-bottom: 2rem;'>Education</h2>
    </div>
    """, unsafe_allow_html=True)

    # Load Lottie animation for the section header
    header_animation = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
    education_chart = create_education_chart()

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

    # B.Tech details with institution and university logos
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("logos/aits_logo.png", width=50)
        st.image("logos/jntua_logo.png", width=50)
    with col2:
        st.write("### 🎓 B.Tech - CSE")
        st.write("**Institution**: Annamacharya Institute Of Technology & Sciences, Kadapa")
        st.write("**University (Affiliated)**: Jawaharlal Nehru Technological University, Anantapur")
        st.write("**Duration**: August 2018 - August 2022")
        st.write("**Percentage of Marks**: 67.98%")
        st.write("**CGPA**: 6.98 | **Final Semester SGPA**: 9.18")
        st.write("**Description**: During my undergraduate studies, I developed strong foundations in computer science and engineering principles, with a focus on software development, data structures, and algorithms.")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Higher Secondary details
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("logos/bie_ap_logo.png", width=50)
    with col2:
        st.write("### 📚 Higher Secondary - 12th Class (PCM)")
        st.write("**Institution**: Sri Chaitanya Junior College, Kadapa")
        st.write("**Board**: Board of Intermediate Education, Andhra Pradesh")
        st.write("**Duration**: April 2018")
        st.write("**Percentage of Marks**: 74.8%")
        st.write("**Description**: In high school, I studied Physics, Chemistry, and Mathematics, which provided me with a strong analytical and problem-solving skill set.")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Secondary details
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("logos/bse_ap_logo.png", width=50)
    with col2:
        st.write("### 🏫 Secondary - 10th Class")
        st.write("**Institution**: Nagarjuna Model School, Maruthinagar, Kadapa")
        st.write("**Board**: Board of Secondary Education, Andhra Pradesh")
        st.write("**Duration**: March 2016")
        st.write("**GPA**: 8.8")
        st.write("**Description**: In secondary school, I excelled in my studies, particularly in subjects like Mathematics and Science, which laid the groundwork for my future academic pursuits.")
    st.markdown("<hr>", unsafe_allow_html=True)