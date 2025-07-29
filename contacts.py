import streamlit as st
import os
from typing import List, Dict
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

# Function to load external CSS file
#def load_css(file_name: str):
#    """Load an external CSS file into the Streamlit app."""
#    with open(file_name, "r", encoding="utf-8") as f:
#        css = f.read()
#    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Function to create a binary file downloader link
def get_binary_file_downloader_html(file_path: str, file_label: str = "File") -> str:
    """Generate a download link for a binary file."""
    with open(file_path, "rb") as f:
        file_data = f.read()
    b64 = base64.b64encode(file_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">{file_label}</a>'
    return href

# Function to create a PDF preview link
def get_pdf_display_link(pdf_path: str) -> str:
    """Create a base64 encoded link to preview a PDF file."""
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Create a data URL for the PDF
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="400" height="300" type="application/pdf">'
        return pdf_display
    except Exception as e:
        st.error(f"Error generating PDF preview: {e}")
        return ""

# Main function to render the contact section
def render_contact_section(resumes: List[Dict[str, str]]) -> None:
    """Render the simplified contact section."""
    st.markdown("""
    <div id='contact' class='section fade-in'>
        <h2 style='text-align: center;'>📞 Contact Me</h2>
    </div>
    """, unsafe_allow_html=True)

    # Contact Information
    st.markdown("<b>Phone:</b> <a href='tel:+919912357968'>+91-9912357968</a>", unsafe_allow_html=True)
    st.write("**Email:** shahidnazeerds@gmail.com")
    st.write("**Location:** Bengaluru, India")
    
    # Contact Form
    with st.form("contact_form"):
        st.subheader("Send me a message")
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit_button = st.form_submit_button("Send Message")
        
        if submit_button:
            if name and email and message:
                st.success("Thanks for your message! I'll get back to you soon.")
                
                # Provide a resume download link
                resume_path = "resumes/data_science_resume.pdf"  # Default resume
                if os.path.exists(resume_path):
                    st.markdown(get_binary_file_downloader_html(resume_path, "Download Resume"), unsafe_allow_html=True)
                else:
                    st.error("Resume file not found.")
            else:
                st.warning("Please fill in all fields before submitting.")

    # Add an interactive map
    st.subheader("📍 My Location")
    st.markdown("""
    <iframe 
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3889.0746881058276!2d77.62996367466373!3d12.902918887406164!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae149516d09edd%3A0x898f1caa2b217281!2sStayvel%20PG%20for%20Gents%20%2F%20PG%20in%20Bommanhalli!5e0!3m2!1sen!2sin!4v1741743188624!5m2!1sen!2sin" 
        width="100%" 
        height="450" 
        style="border:0;" 
        allowfullscreen="" 
        loading="lazy" 
        referrerpolicy="no-referrer-when-downgrade">
    </iframe>
    """, unsafe_allow_html=True)

    # Resume Showcase
    st.markdown("---")
    st.subheader("📋 My Resumes")
    st.write("Explore my professional resumes tailored for different roles.")
    
    # Display resumes side by side
    num_cols = 2  # Two resumes per row
    rows = [resumes[i:i + num_cols] for i in range(0, len(resumes), num_cols)]
    
    for row in rows:
        cols = st.columns(num_cols)
        for i, resume in enumerate(row):
            with cols[i]:
                render_resume_card(resume)

# Function to render an individual resume card
def render_resume_card(resume: Dict[str, str]) -> None:
    """Render an individual resume card with preview and download options."""
    with st.container():
        st.markdown(f"<div class='resume-card'>", unsafe_allow_html=True)
        
        # Icon or placeholder
        icon = get_icon_for_resume(resume['title'])
        st.markdown(f"**{icon} {resume['title']}**")
        
        # Description
        if 'description' in resume:
            st.markdown(resume['description'])
        
        # Preview and download buttons
        if os.path.exists(resume['file']):
            # Preview
            pdf_display = get_pdf_display_link(resume['file'])
            if pdf_display:
                st.markdown(pdf_display, unsafe_allow_html=True)
            else:
                st.error("Could not generate preview.")
            
            # Download button
            with open(resume['file'], "rb") as file:
                st.download_button(
                    label="Download Resume",
                    data=file,
                    file_name=os.path.basename(resume['file']),
                    mime="application/pdf",
                    key=f"dl_{resume['title'].replace(' ', '_')}",
                    use_container_width=True
                )
        else:
            st.error(f"Resume file not found: {resume['file']}")
        
        st.markdown("</div>", unsafe_allow_html=True)

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