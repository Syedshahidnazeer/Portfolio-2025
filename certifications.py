import streamlit as st
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image
#Import Method to render PDF
from utils import get_pdf_display_link

# Function to load custom CSS styles
def load_styles() -> None:
    """Load custom CSS styles for the certifications section."""
    st.markdown("""
    <style>
    /* Certifications Section Styling */
    .cert-section {
        padding: 20px;
        max-width: 1200px;
        margin: 0 auto;
        animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Certification Card Styling */
    .cert-card {
        background-color: var(--secondary-background-color);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        animation: slideIn 0.5s ease-out; /* Add slide-in animation */
    }
    @keyframes slideIn {
        from { transform: translateX(-50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .cert-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .cert-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        color: var(--primary-color);
    }
    .cert-title {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: var(--text-color);
        font-size: 1.1rem;
    }
    .cert-org {
        font-size: 0.9rem;
        color: var(--text-color);
        margin-bottom: 0.5rem;
        font-style: italic;
    }
    .cert-date {
        font-size: 0.8rem;
        color: var(--text-color-secondary);
        margin-bottom: 0.5rem;
    }
    .cert-details {
        font-size: 0.9rem;
        color: var(--text-color);
        margin-bottom: 1rem;
        flex-grow: 1;
    }
    .cert-logo {
        max-width: 80px;
        max-height: 40px;
        margin: 0 auto 0.5rem auto;
        object-fit: contain;
    }
    .download-cert-btn {
        background-color: var(--primary-color);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        display: inline-block;
    }
    .download-cert-btn:hover {
        background-color: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .preview-cert-btn {
        background-color: var(--secondary-color);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .preview-cert-btn:hover {
        background-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .cert-carousel {
        padding: 1rem;
        border-radius: 10px;
        background-color: rgba(0,0,0,0.03);
        margin-bottom: 2rem;
    }
    .expiring-soon {
        color: #ff4500;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.6; }
        100% { opacity: 1; }
    }
    .category-badge {
        display: inline-block;
        background-color: var(--primary-color);
        color: white;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        margin-right: 4px;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to generate a thumbnail from the first page of a PDF
def get_pdf_thumbnail(pdf_path: str) -> Optional[BytesIO]:
    """Generate a thumbnail image from the first page of a PDF."""
    try:
        import fitz  # PyMuPDF

        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # First page
        pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))  # Reduced size

        img_bytes = BytesIO(pix.tobytes("png"))
        doc.close()

        return img_bytes
    except Exception:
        # If PyMuPDF is not available or error occurs, return None
        return None

# Function to check if a certificate is expiring soon
def is_expiring_soon(expiry_date: Optional[str], days_threshold: int = 90) -> bool:
    """Check if a certificate is expiring within the given threshold of days."""
    if not expiry_date:
        return False

    try:
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
        today = datetime.now()
        days_remaining = (expiry - today).days

        return 0 <= days_remaining <= days_threshold
    except ValueError:
        return False

# Render individual certification card
def render_certificate_card(cert: Dict[str, str], col) -> None:  # Pass the column
    """Render an individual certification card."""
    expiring = is_expiring_soon(cert.get('expiry_date'))

    with col: # use the passed column
        # Build the HTML content for the card
        card_html = f"""<div class="cert-card">"""

        # Logo
        if 'logo' in cert and os.path.exists(cert['logo']):
            # Streamlit's st.image is better for local images, but for embedding in HTML, base64 is needed
            # For simplicity and to avoid re-implementing base64 encoding here, I'll use a placeholder
            # or assume st.image is called separately if needed, but for now, let's keep it simple.
            # If the logo needs to be *inside* the HTML string, it would need to be base64 encoded.
            # For this fix, I'll assume st.image is handled outside the main HTML string if desired.
            # For now, I'll just add a placeholder icon if no logo is directly embeddable in HTML.
            card_html += f"""<img src="{cert['logo']}" class="cert-logo" alt="Certification Logo">"""
        else:
            card_html += f"""<div class="cert-icon">🎓</div>"""

        # Title and basic info
        card_html += f"""<div class="cert-title">{cert['title']}</div>"""

        if 'organization' in cert:
            card_html += f"""<div class="cert-org">Issued by: {cert['organization']}</div>"""

        # Category badges
        if 'categories' in cert and cert['categories']:
            badges_html = ""
            for category in cert['categories']:
                badges_html += f'<span class="category-badge">{category}</span>'
            card_html += f"""<div>{badges_html}</div>"""

        # Date information
        date_html = ""
        if 'issue_date' in cert:
            date_html += f"Issued: {cert['issue_date']}"

        if 'expiry_date' in cert and cert['expiry_date']:
            expiry_class = "expiring-soon" if expiring else ""
            days_left_text = ""
            if expiring:
                days_left = (datetime.strptime(cert['expiry_date'], "%Y-%m-%d") - datetime.now()).days
                days_left_text = f" ({days_left} days left)"
            date_html += f" • <span class='{expiry_class}'>Expires: {cert['expiry_date']}{days_left_text}</span>"

        if date_html:
            card_html += f"""<div class="cert-date">{date_html}</div>"""

        # Description
        if 'description' in cert:
            card_html += f"""<div class="cert-details">{cert['description']}</div>"""

            # Skills covered (if available)
            if 'skills' in cert and cert['skills']:
                skills_list = ", ".join(cert['skills'])
                card_html += f"""<p><strong>Skills:</strong> {skills_list}</p>"""

        # Certificate ID if available
        if 'credential_id' in cert:
            card_html += f"""<p><strong>Credential ID:</strong> {cert['credential_id']}</p>"""

        # Verification URL if available
        if 'verification_url' in cert:
            card_html += f"""<p><a href="{cert['verification_url']}" target="_blank">Verify Certificate</a></p>"""

        # PDF Preview (embedded directly in HTML)
        pdf_display_html = get_pdf_display_link(cert['pdf'])
        if pdf_display_html:
            card_html += pdf_display_html
        else:
            card_html += f"""<p style="color: red;">Could not generate PDF preview.</p>"""

        card_html += f"""</div>""" # Close cert-card div

        # Render the entire HTML card
        st.markdown(card_html, unsafe_allow_html=True)

        # Download button (must be a separate Streamlit component)
        with open(cert['pdf'], "rb") as file:
            st.download_button(
                label="Download Certificate",
                data=file,
                file_name=os.path.basename(cert['pdf']),
                mime="application/pdf",
                key=f"dl_{cert['title'].replace(' ', '_')}",
                use_container_width=True
            )

# Main function to render the certifications section
def render_certifications_section(certifications: List[Dict[str, str]]) -> None:
    """Render the enhanced certifications section with all features."""
    st.markdown("""
    <div id='certifications' class='section fade-in'>
        <h2 style='text-align: center;'>🎓 My Certifications</h2>
    </div>
    """, unsafe_allow_html=True)
    st.write("Explore my professional certifications and qualifications.")

    # Load custom styles
    load_styles()

    # Display certificates in two columns
    cols = st.columns(2) # create two columns

    for i, cert in enumerate(certifications):
        render_certificate_card(cert, cols[i % 2])

    st.markdown("</div>", unsafe_allow_html=True)

sample_certifications = [
    {
        "title": "Data Science - By Excelr",
        "pdf": "Certifications/Excelr(Data Science)_Certification.pdf",
        "description": "A comprehensive certification in Data Science covering various tools and techniques.",
        "issue_date": "2023-01-15",
        "skills": ["Python", "Machine Learning", "Data Visualization"]
    },
    {
        "title": "Business Analytics - Internshala",
        "pdf": "Certifications/Internshala(Business Analytics)_Certification.pdf",
        "description": "An introductory certification in Business Analytics focusing on data-driven decision making.",
        "issue_date": "2022-11-20",
        "skills": ["Data Analysis", "Excel", "Statistical Analysis"]
    },
        {
        "title": "AWS Certified Cloud Practitioner",
        "pdf": "Certifications/Internshala(Business Analytics)_Certification.pdf",
        "description": "An introductory certification in Business Analytics focusing on data-driven decision making.",
        "issue_date": "2022-11-20",
        "skills": ["Data Analysis", "Excel", "Statistical Analysis"]
    },
        {
        "title": "Google Data Analytics Professional Certificate",
        "pdf": "Certifications/Internshala(Business Analytics)_Certification.pdf",
        "description": "An introductory certification in Business Analytics focusing on data-driven decision making.",
        "issue_date": "2022-11-20",
        "skills": ["Data Analysis", "Excel", "Statistical Analysis"]
    }
]