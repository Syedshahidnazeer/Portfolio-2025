# contact_resume.py
import streamlit as st
import os
from typing import Dict, List

def load_resume_styles() -> None:
    """Load custom CSS styles for the resume cards with 3 per row layout."""
    st.markdown("""
    <style>
    .resume-section {
        padding: 20px;
        max-width: 1400px;
        margin: 0 auto;
    }
    .resume-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);  /* Changed to grid with 3 columns */
        gap: 25px;
        margin-top: 20px;
        justify-items: center;
    }
    .resume-card {
        width: 300px;  /* Slightly wider cards */
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
        font-size: 48px;
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
    /* Responsive design for smaller screens */
    @media (max-width: 1200px) {
        .resume-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    @media (max-width: 768px) {
        .resume-container {
            grid-template-columns: 1fr;
        }
        .resume-card {
            width: 280px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_resume_card(resume: Dict[str, str]) -> None:
    """Display a single resume card with flip animation."""
    html = f"""
    <div class="resume-card">
        <div class="resume-card-inner">
            <div class="resume-front">
                <div class="resume-icon">📄</div>
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
    
    # Contact Information and Languages
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='contact-info'>
            <p>📧 Email: shahidnazeerda@gmail.com</p>
            <p>📱 Phone: +91-9912357968</p>
            <p>📍 Location: Madhapur, Hyderabad</p>
            <p>🌐 Portfolio: <a href="https://syed-shahid-nazeer-portfolio.streamlit.app" target="_blank">https://syed-shahid-nazeer-portfolio.streamlit.app</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3>Languages</h3>", unsafe_allow_html=True)
        languages = ["English", "Telugu", "Hindi"]
        for lang in languages:
            st.markdown(f"<div class='language-item'>{lang}</div>", unsafe_allow_html=True)
    
    # Resume Showcase
    st.markdown("<div class='resume-section'>", unsafe_allow_html=True)
    st.header("My Resumes")
    
    st.markdown('<div class="resume-container">', unsafe_allow_html=True)
    for resume in resumes:
        display_resume_card(resume)
    st.markdown('</div></div>', unsafe_allow_html=True)