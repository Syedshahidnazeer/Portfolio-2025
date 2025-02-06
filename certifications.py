# certifications.py
import streamlit as st
import os
import base64
from typing import List, Dict

def load_styles() -> None:
    """Load custom CSS styles for the animated certificate cards."""
    st.markdown("""
    <style>
    .cert-section {
        padding: 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    .cert-container {
        display: flex;
        justify-content: center;
        align-items: start;
        gap: 40px;
        margin-top: 20px;
    }
    .cert-card {
        width: 320px;
        height: 360px;
        perspective: 1500px;
        flex-shrink: 0;
    }
    .cert-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.8s;
        transform-style: preserve-3d;
        cursor: pointer;
    }
    .cert-card:hover .cert-card-inner {
        transform: rotateY(180deg);
    }
    .cert-front, .cert-back {
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
        padding: 20px;
    }
    .cert-back {
        transform: rotateY(180deg);
        background: #f8f9fa;
    }
    .cert-image {
        width: 100%;
        height: 240px;
        object-fit: contain;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .cert-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 10px 0;
    }
    .stDownloadButton {
        margin-top: 15px !important;
    }
    /* Hide Streamlit's default containers */
    .block-container {
        padding-top: 0;
        padding-bottom: 0;
        max-width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def get_image_base64(image_path: str) -> str:
    """Convert image to base64 string."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def display_certification_card(cert: Dict[str, str]) -> None:
    """Display a single certification card with flip animation."""
    html = f"""
    <div class="cert-card">
        <div class="cert-card-inner">
            <div class="cert-front">
                <img src="data:image/png;base64,{get_image_base64(cert['image'])}" 
                     class="cert-image" alt="{cert['title']}"/>
                <div class="cert-title">{cert['title']}</div>
            </div>
            <div class="cert-back">
                <div class="cert-title">{cert['title']}</div>
                <div class="cert-details">Click the button below to download</div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    if os.path.exists(cert['pdf']):
        with open(cert['pdf'], "rb") as pdf_file:
            st.download_button(
                label="📄 Download Certificate",
                data=pdf_file.read(),
                file_name=os.path.basename(cert['pdf']),
                mime="application/octet-stream",
                key=f"download_{cert['title']}"
            )
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_certifications_section(certifications: List[Dict[str, str]]) -> None:
    """Render the entire certifications section with animated cards."""
    st.markdown("<div class='cert-section'>", unsafe_allow_html=True)
    st.header("Certifications")
    
    load_styles()
    
    st.markdown('<div class="cert-container">', unsafe_allow_html=True)
    for cert in certifications:
        display_certification_card(cert)
    st.markdown('</div></div>', unsafe_allow_html=True)