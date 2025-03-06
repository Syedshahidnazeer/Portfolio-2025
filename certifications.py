import streamlit as st
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import base64
from io import BytesIO
import pandas as pd
from PIL import Image

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
    .filter-section {
        background-color: var(--secondary-background-color);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .search-box {
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to create a PDF preview link
def get_pdf_display_link(pdf_path: str) -> str:
    """Create a base64 encoded link to preview a PDF file."""
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Create a data URL for the PDF
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
        return pdf_display
    except Exception as e:
        st.error(f"Error generating PDF preview: {e}")
        return ""

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
def render_certificate_card(cert: Dict[str, str], show_detailed: bool = False) -> None:
    """Render an individual certification card."""
    expiring = is_expiring_soon(cert.get('expiry_date'))
    
    with st.container():
        card = st.container()
        
        with card:
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
            if show_detailed and 'description' in cert:
                st.markdown(f"""<div class="cert-details">{cert['description']}</div>""", unsafe_allow_html=True)
                
                # Skills covered (if available)
                if 'skills' in cert and cert['skills']:
                    skills_list = ", ".join(cert['skills'])
                    st.markdown(f"**Skills:** {skills_list}")
            
            # Certificate ID if available
            if show_detailed and 'credential_id' in cert:
                st.markdown(f"**Credential ID:** {cert['credential_id']}")
            
            # Verification URL if available
            if show_detailed and 'verification_url' in cert:
                st.markdown(f"[Verify Certificate]({cert['verification_url']})")
                
            # Preview and download buttons
            col1, col2 = st.columns(2)
            
            if os.path.exists(cert['pdf']):
                # Preview button
                if st.button("Preview Certificate", key=f"preview_{cert['title'].replace(' ', '_')}"):
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
            else:
                st.error(f"Certificate file not found: {cert['pdf']}")

# Function to display certificates in a carousel
def render_certificates_carousel(featured_certs: List[Dict[str, str]]) -> None:
    """Render a carousel of featured certificates."""
    st.markdown("<div class='cert-carousel'>", unsafe_allow_html=True)
    st.subheader("🌟 Featured Certifications")
    
    # Create columns for the carousel
    columns = st.columns(len(featured_certs))
    
    for i, cert in enumerate(featured_certs):
        with columns[i]:
            # Try to generate thumbnail
            thumbnail = get_pdf_thumbnail(cert['pdf']) if os.path.exists(cert['pdf']) else None
            
            if thumbnail:
                st.image(thumbnail, use_column_width=True)
            elif 'logo' in cert and os.path.exists(cert['logo']):
                st.image(cert['logo'], use_column_width=True)
            else:
                st.markdown("🎓", unsafe_allow_html=True)
                
            st.markdown(f"<div style='text-align: center;'><strong>{cert['title']}</strong></div>", unsafe_allow_html=True)
            if 'organization' in cert:
                st.markdown(f"<div style='text-align: center; font-style: italic;'>{cert['organization']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Main function to render the certifications section
def render_certifications_section(certifications: List[Dict[str, str]]) -> None:
    """Render the enhanced certifications section with all features."""
    st.markdown("<div id='certifications' class='section fade-in'>", unsafe_allow_html=True)
    st.header("🎓 My Certifications")
    st.write("Explore my professional certifications and qualifications.")
    
    # Load custom styles
    load_styles()
    
    # Extract all unique categories and organizations for filtering
    all_categories = []
    all_organizations = []
    
    for cert in certifications:
        if 'categories' in cert:
            all_categories.extend(cert['categories'])
        if 'organization' in cert:
            all_organizations.append(cert['organization'])
    
    all_categories = sorted(list(set(all_categories)))
    all_organizations = sorted(list(set(all_organizations)))
    
    # Featured certificates carousel (select 3-4 of your best ones)
    featured_certs = [cert for cert in certifications if cert.get('featured', False)]
    if featured_certs:
        render_certificates_carousel(featured_certs[:4])  # Limit to 4 featured certificates
    
    # Filters and search section
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    
    # Search functionality
    search_query = st.text_input("🔍 Search certifications", key="cert_search", 
                                 help="Search by title, organization, or skills")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_categories = st.multiselect("Filter by Category", 
                                            options=all_categories,
                                            help="Select one or more categories")
    
    with col2:
        selected_organizations = st.multiselect("Filter by Organization", 
                                                options=all_organizations,
                                                help="Select one or more organizations")
    
    with col3:
        sort_option = st.selectbox("Sort by", 
                                    options=["Most Recent", "Alphabetical", "Expiring Soon"],
                                    help="Choose how to sort certificates")
    
    # Display mode
    view_mode = st.radio("View Mode", ["Grid View", "Detailed View"], horizontal=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Apply filters and search
    filtered_certs = certifications.copy()
    
    # Filter by search query
    if search_query:
        filtered_certs = [
            cert for cert in filtered_certs if 
            search_query.lower() in cert['title'].lower() or
            ('organization' in cert and search_query.lower() in cert['organization'].lower()) or
            ('description' in cert and search_query.lower() in cert['description'].lower()) or
            ('skills' in cert and any(search_query.lower() in skill.lower() for skill in cert['skills']))
        ]
    
    # Filter by categories
    if selected_categories:
        filtered_certs = [
            cert for cert in filtered_certs if 
            'categories' in cert and any(category in selected_categories for category in cert['categories'])
        ]
    
    # Filter by organizations
    if selected_organizations:
        filtered_certs = [
            cert for cert in filtered_certs if 
            'organization' in cert and cert['organization'] in selected_organizations
        ]
    
    # Sort certificates
    if sort_option == "Most Recent":
        filtered_certs = sorted(filtered_certs, 
                               key=lambda x: datetime.strptime(x.get('issue_date', '2000-01-01'), "%Y-%m-%d"), 
                               reverse=True)
    elif sort_option == "Alphabetical":
        filtered_certs = sorted(filtered_certs, key=lambda x: x['title'])
    elif sort_option == "Expiring Soon":
        # Put expiring certificates first, then sort by expiry date
        filtered_certs = sorted(filtered_certs, 
                               key=lambda x: (
                                   0 if is_expiring_soon(x.get('expiry_date')) else 1,
                                   datetime.strptime(x.get('expiry_date', '9999-12-31'), "%Y-%m-%d")
                               ))
    
    # Display filtered certificates
    if not filtered_certs:
        st.info("No certificates match your search criteria. Try adjusting your filters.")
    else:
        st.write(f"Displaying {len(filtered_certs)} certification(s)")
        
        if view_mode == "Grid View":
            # Display in grid view (3 columns)
            num_cols = 3
            rows = [filtered_certs[i:i + num_cols] for i in range(0, len(filtered_certs), num_cols)]
            
            for row in rows:
                cols = st.columns(num_cols)
                for i, cert in enumerate(row):
                    with cols[i]:
                        render_certificate_card(cert, show_detailed=False)
        else:
            # Display in detailed view (1 column)
            for cert in filtered_certs:
                render_certificate_card(cert, show_detailed=True)
                st.markdown("---")
    
    # Display certificates that are expiring soon in a special section
    expiring_certs = [cert for cert in certifications if is_expiring_soon(cert.get('expiry_date'))]
    if expiring_certs:
        st.markdown("---")
        st.subheader("⚠️ Certifications Expiring Soon")
        st.write("The following certifications need attention:")
        
        for cert in expiring_certs:
            days_left = (datetime.strptime(cert['expiry_date'], "%Y-%m-%d") - datetime.now()).days
            st.warning(f"**{cert['title']}** expires in {days_left} days ({cert['expiry_date']})")
    
    st.markdown("</div>", unsafe_allow_html=True)

sample_certifications = [
    {
        "title": "Data Science - By Excelr",
        "pdf": "Certifications/Excelr(Data Science)_Certification.pdf"
    },
    {
        "title": "Business Analytics - Internshala",
        "pdf": "Certifications/Internshala(Business Analytics)_Certification.pdf"
    }
]