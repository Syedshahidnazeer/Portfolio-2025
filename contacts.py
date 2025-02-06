import streamlit as st
import os
from typing import Dict, List

def load_resume_styles() -> None:
    """Load custom CSS styles for the resume cards with 3 columns layout."""
    st.markdown("""
    <style>
    .resume-section {
        padding: 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    .resume-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr); /* Changed to 3 columns */
        gap: 25px;
        margin-top: 20px;
        justify-items: center;
    }
    .resume-card {
        width: 100%;
        max-width: 320px; /* Adjusted max-width for 3 columns */
        height: 300px;
        perspective: 1500px;
        margin-bottom: 20px;
    }
    .resume-card {
        width: 100%;
        max-width: 500px;
        height: 300px;
        perspective: 1500px;
        margin-bottom: 20px;
    }
    .resume-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.8s;
        transform-style: preserve-3d;
        cursor: pointer;
    }
    .resume-card:hover .resume-card-inner {
        transform: rotateY(180deg);
    }
    .resume-front, .resume-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background: white;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px;
    }
    .resume-back {
        transform: rotateY(180deg);
        background: #f8f9fa;
    }
    .resume-icon {
        font-size: 64px;
        margin-bottom: 15px;
        color: #2c3e50;
    }
    .resume-title {
        font-size: 1rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 10px 0;
        text-align: center;
    }
    .resume-description {
        font-size: 0.9rem;
        color: #666;
        text-align: center;
        margin-top: 10px;
    }
    .stDownloadButton {
        margin-top: 15px !important;
    }
    @media (max-width: 1200px) { /* Adjusted breakpoint for 3 columns */
        .resume-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    @media (max-width: 768px) {
        .resume-container {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def get_icon_for_resume(title: str) -> str:
    """Select an appropriate icon based on resume title."""
    icons = {
        "Data Science": "🧠",
        "Full Stack Developer": "💻",
        "Business Analyst": "📊",
        "Python Developer": "🐍",
        "Machine Learning": "🤖"
    }
    return icons.get(title, "📄")

def display_resume_card(resume: Dict[str, str]) -> None:
    """Display a single resume card with flip animation."""
    icon = get_icon_for_resume(resume['title'])
    
    html = f"""
    <div class="resume-card">
        <div class="resume-card-inner">
            <div class="resume-front">
                <div class="resume-icon">{icon}</div>
                <div class="resume-title">{resume['title']}</div>
                <div class="resume-description">{resume.get('description', '')}</div>
            </div>
            <div class="resume-back">
                <div class="resume-title">{resume['title']}</div>
                <div class="resume-description">Click to download</div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    if os.path.exists(resume['file']):
        with open(resume['file'], "rb") as pdf_file:
            st.download_button(
                label="📄 Download Resume",
                data=pdf_file.read(),
                file_name=os.path.basename(resume['file']),
                mime="application/octet-stream",
                key=f"download_resume_{resume['title']}"
            )
    else:
        st.warning(f"Resume file not found: {resume['file']}")
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_contact_section(resumes: List[Dict[str, str]]) -> None:
    """Display contact information and resume showcase together."""
    load_resume_styles()
    
    st.markdown("<div id='contact' class='section'><h2>Contact</h2></div>", unsafe_allow_html=True)
    
    # Contact Information
    st.markdown("""
    <div class='contact-info'>
        <p>📧 Email: shahidnazeerda@gmail.com</p>
        <p>📱 Phone: +91-9912357968</p>
        <p>📍 Location: Madhapur, Hyderabad</p>
        <p>🌐 Portfolio: <a href="https://syed-shahid-nazeer-portfolio.streamlit.app" target="_blank">https://syed-shahid-nazeer-portfolio.streamlit.app</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Resume Showcase
    st.markdown("<div class='resume-section'>", unsafe_allow_html=True)
    st.header("My Resumes")
    
    # Create a 3-column layout
    num_cols = 3
    cols = st.columns(num_cols)
    
    # Calculate the number of rows needed
    num_rows = -(-len(resumes) // num_cols)  # Ceiling division
    
    # Display resumes in a 3-column layout
    for i in range(num_rows):
        for j in range(num_cols):
            index = i * num_cols + j
            if index < len(resumes):
                with cols[j]:
                    display_resume_card(resumes[index])
            else:
                # Empty column if no more resumes
                with cols[j]:
                    st.empty()
    
    st.markdown("</div>", unsafe_allow_html=True)