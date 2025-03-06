import streamlit as st
import os
from typing import List, Dict, Optional
from datetime import datetime
import base64
    # Sample resume data structure
sample_resumes = [
    {
        "title": "Data Science",
        "description": "Resume tailored for Data Science roles.",
        "file": "resumes/data_science_resume.pdf",
        "date": "2023-01-15"
    },
    {
        "title": "Full Stack Developer",
        "description": "Resume tailored for Full Stack Development roles.",
        "file": "resumes/full_stack_resume.pdf",
        "date": "2022-11-05"
    },
    {
        "title": "Business Analyst",
        "description": "Resume tailored for Business Analyst roles.",
        "file": "resumes/business_analyst_resume.pdf",
        "date": "2021-09-20"
    },
    {
        "title": "Machine Learning Engineer",
        "description": "Resume tailored for Machine Learning Engineering roles.",
        "file": "resumes/machine_learning_resume.pdf",
        "date": "2023-03-10"
    },
    {
        "title": "Data Analyst",
        "description": "Resume tailored for Data Analyst roles.",
        "file": "resumes/data_analyst_resume.pdf",
        "date": "2022-07-22"
    },
    {
        "title": "Software Developer",
        "description": "Resume tailored for Software Development roles.",
        "file": "resumes/software_developer_resume.pdf",
        "date": "2021-05-14"
    },
    {
        "title": "AI Researcher",
        "description": "Resume tailored for AI Research roles.",
        "file": "resumes/ai_researcher_resume.pdf",
        "date": "2023-02-01"
    },
    {
        "title": "DevOps Engineer",
        "description": "Resume tailored for DevOps Engineering roles.",
        "file": "resumes/devops_engineer_resume.pdf",
        "date": "2022-04-18"
    }
]
    
# Function to load custom CSS styles
def load_styles() -> None:
    """Load custom CSS styles for the contact section."""
    st.markdown("""
        <style>
        /* Contact Section Styling */
        .contact-info {
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            background: var(--secondary-background-color);
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .contact-info:hover {
            transform: translateY(-5px);
        }
        .contact-info p {
            font-size: 16px;
            color: var(--text-color);
            margin: 10px 0;
        }
        .contact-info a {
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .contact-info a:hover {
            color: var(--secondary-color);
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
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf">'
        return pdf_display
    except Exception as e:
        st.error(f"Error generating PDF preview: {e}")
        return ""

# Function to render an individual resume card
def render_resume_card(resume: Dict[str, str], show_detailed: bool = False) -> None:
    """Render an individual resume card."""
    with st.container():
        # Icon or placeholder
        icon = get_icon_for_resume(resume['title'])
        st.markdown(f"**{icon} {resume['title']}**")
        
        # Description
        if 'description' in resume:
            st.markdown(resume['description'])
        
        # Preview and download buttons
        col1, col2 = st.columns(2)
        
        if os.path.exists(resume['file']):
            # Preview button
            if col1.button("Preview Resume", key=f"preview_{resume['title'].replace(' ', '_')}"):
                pdf_display = get_pdf_display_link(resume['file'])
                if pdf_display:
                    st.markdown(pdf_display, unsafe_allow_html=True)
                else:
                    st.error("Could not generate preview.")
            
            # Download button
            with open(resume['file'], "rb") as file:
                col2.download_button(
                    label="Download Resume",
                    data=file,
                    file_name=os.path.basename(resume['file']),
                    mime="application/pdf",
                    key=f"dl_{resume['title'].replace(' ', '_')}",
                    use_container_width=True
                )
        else:
            st.error(f"Resume file not found: {resume['file']}")

# Function to select an appropriate icon based on resume title
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

# Main function to render the contact section
def render_contact_section(resumes: List[Dict[str, str]]) -> None:
    """Render the enhanced contact section with all features."""
    st.markdown("<div id='contact' class='section fade-in'>", unsafe_allow_html=True)
    st.header("📞 Contact Me")
    st.write("Feel free to reach out to me through the following channels.")
    
    # Load custom styles
    load_styles()
    
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
    st.markdown("---")
    st.subheader("📋 My Resumes")
    st.write("Explore my professional resumes tailored for different roles.")
    
    # Filters and search section
    search_query = st.text_input("🔍 Search resumes", key="resume_search", help="Search by title or description")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_titles = st.multiselect("Filter by Title", options=sorted({resume['title'] for resume in resumes}))
    
    with col2:
        sort_option = st.selectbox("Sort by", options=["Most Recent", "Alphabetical"])
    
    # Display mode
    view_mode = st.radio("View Mode", ["Grid View", "Detailed View"], horizontal=True)
    
    # Apply filters and search
    filtered_resumes = resumes.copy()
    
    if search_query:
        filtered_resumes = [
            resume for resume in filtered_resumes if 
            search_query.lower() in resume['title'].lower() or
            ('description' in resume and search_query.lower() in resume['description'].lower())
        ]
    
    if selected_titles:
        filtered_resumes = [
            resume for resume in filtered_resumes if 
            resume['title'] in selected_titles
        ]
    
    # Sort resumes
    if sort_option == "Most Recent":
        filtered_resumes = sorted(filtered_resumes, key=lambda x: datetime.strptime(x.get('date', '2000-01-01'), "%Y-%m-%d"), reverse=True)
    elif sort_option == "Alphabetical":
        filtered_resumes = sorted(filtered_resumes, key=lambda x: x['title'])
    
    # Display filtered resumes
    if not filtered_resumes:
        st.info("No resumes match your search criteria. Try adjusting your filters.")
    else:
        st.write(f"Displaying {len(filtered_resumes)} resume(s)")
        
        if view_mode == "Grid View":
            # Display in grid view (3 columns)
            num_cols = 3
            rows = [filtered_resumes[i:i + num_cols] for i in range(0, len(filtered_resumes), num_cols)]
            
            for row in rows:
                cols = st.columns(num_cols)
                for i, resume in enumerate(row):
                    with cols[i]:
                        render_resume_card(resume, show_detailed=False)
        else:
            # Display in detailed view (1 column)
            for resume in filtered_resumes:
                render_resume_card(resume, show_detailed=True)
                st.markdown("---")
