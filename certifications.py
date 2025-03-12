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
        card = st.container()

        with card:
            st.markdown(f"""<div class="cert-card">""")
            # Logo
            if 'logo' in cert and os.path.exists(cert['logo']):
                st.image(cert['logo'], width=80)
            else:
                st.markdown(f"""<div class="cert-icon">🎓</div>""", unsafe_allow_html=True)

            # Title and basic info
            st.markdown(f"""<div class="cert-title">{cert['title']}</div>""", unsafe_allow_html=True)

            if 'organization' in cert:
                st.markdown(f"""<div class="cert-org">Issued by: {cert['organization']}</div>""", unsafe_allow_html=True)

            # Category badges
            if 'categories' in cert and cert['categories']:
                badges_html = ""
                for category in cert['categories']:
                    badges_html += f'<span class="category-badge">{category}</span>'
                st.markdown(f"""<div>{badges_html}</div>""", unsafe_allow_html=True)

            # Date information
            date_html = ""
            if 'issue_date' in cert:
                date_html += f"Issued: {cert['issue_date']}"

            if 'expiry_date' in cert and cert['expiry_date']:
                expiry_class = "expiring-soon" if expiring else ""
                date_html += f" • <span class='{expiry_class}'>Expires: {cert['expiry_date']}</span>"

                if expiring:
                    days_left = (datetime.strptime(cert['expiry_date'], "%Y-%m-%d") - datetime.now()).days
                    date_html += f" <span class='expiring-soon'>({days_left} days left)</span>"

            if date_html:
                st.markdown(f"""<div class="cert-date">{date_html}</div>""", unsafe_allow_html=True)

            # Description (only in detailed view)
            if 'description' in cert:
                st.markdown(f"""<div class="cert-details">{cert['description']}</div>""", unsafe_allow_html=True)

                # Skills covered (if available)
                if 'skills' in cert and cert['skills']:
                    skills_list = ", ".join(cert['skills'])
                    st.markdown(f"**Skills:** {skills_list}")

            # Certificate ID if available
            if 'credential_id' in cert:
                st.markdown(f"**Credential ID:** {cert['credential_id']}")

            # Verification URL if available
            if 'verification_url' in cert:
                st.markdown(f"[Verify Certificate]({cert['verification_url']})")

            # Preview
            pdf_display = get_pdf_display_link(cert['pdf'])
            if pdf_display:
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.error("Could not generate preview.")

            # Download button
            with open(cert['pdf'], "rb") as file:
                st.download_button(
                    label="Download Certificate",
                    data=file,
                    file_name=os.path.basename(cert['pdf']),
                    mime="application/pdf",
                    key=f"dl_{cert['title'].replace(' ', '_')}",
                    use_container_width=True
                )
            st.markdown(f"""</div>""")

# Main function to render the certifications section
def render_certifications_section(certifications: List[Dict[str, str]]) -> None:
    """Render the enhanced certifications section with all features."""
    st.markdown("<div id='certifications' class='section fade-in'>", unsafe_allow_html=True)
    st.header("🎓 My Certifications")
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