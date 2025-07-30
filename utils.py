# utils.py
import streamlit as st
import base64
import os

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

def get_binary_file_downloader_html(file_path: str, file_label: str = "File") -> str:
    """Generate a download link for a binary file."""
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
        b64 = base64.b64encode(file_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}" class="btn">{file_label}</a>'
        return href
    except Exception as e:
        st.error(f"Error generating download link: {e}")
        return ""

def animate_text_letter_by_letter(text, tag='span', delay_per_letter=0.05, animation_duration=0.5):
    html_content = ""
    for i, char in enumerate(text):
        if char == " ": # Handle spaces
            html_content += " "
        else:
            html_content += f'<{tag} style="display: inline-block; animation: letterReveal {animation_duration}s ease-out {i * delay_per_letter}s infinite;">{char}</{tag}>'
    return html_content