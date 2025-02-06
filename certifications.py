# certifications.py
import streamlit as st
import os
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
        flex-wrap: wrap; 
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
    .cert-symbol {
        font-size: 64px;
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
    /* Optional: Responsive adjustment to ensure cards don't get too small */
    @media only screen and (max-width: 768px) {
        .cert-card {
            width: calc(50% - 20px); 
        }
    }
    @media only screen and (max-width: 480px) {
        .cert-card {
            width: 100%; 
            margin: 20px auto; 
        }
    }
    </style>
    """, unsafe_allow_html=True)

def display_certification_card(cert: Dict[str, str], column) -> None:
    """Display a single certification card with flip animation."""
    html = f"""
    <div class="cert-card">
        <div class="cert-card-inner">
            <div class="cert-front">
                <span class="cert-symbol">&#127891;</span>
                <div class="cert-title">{cert['title']}</div>
            </div>
            <div class="cert-back">
                <div class="cert-title">{cert['title']}</div>
                <div class="cert-details">Click the button below to download</div>
    """
    column.markdown(html, unsafe_allow_html=True)
    
    if os.path.exists(cert['pdf']):
        with open(cert['pdf'], "rb") as pdf_file:
            column.download_button(
                label="&#128194; Download Certificate",
                data=pdf_file.read(),
                file_name=os.path.basename(cert['pdf']),
                mime="application/octet-stream",
                key=f"download_{cert['title']}"
            )
    
    column.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_certifications_section(certifications: List[Dict[str, str]]) -> None:
    """Render the entire certifications section with animated cards."""
    
    # **Temporary Adjustment for Debugging**
    st.write("---- **Before Custom Styles and Content** ----")
    st.write(f"Navbar Should be Visible Here: {st.session_state.selected}")
    
    st.markdown("<div class='cert-section'>", unsafe_allow_html=True)
    st.header("Certifications")
    
    # **Apply Custom Styles**
    load_styles()
    st.write("---- **After Applying Custom Styles** ----")
    st.write(f"Navbar Visibility After Styles: {st.session_state.selected}")
    
    # Create columns for horizontal layout
    num_cols = len(certifications)
    cols = st.columns(num_cols)
    
    # Display each certification card in a separate column
    for i, cert in enumerate(certifications):
        display_certification_card(cert, cols[i])
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("---- **After Rendering Content** ----")
    st.write(f"Final Navbar Visibility: {st.session_state.selected}")
