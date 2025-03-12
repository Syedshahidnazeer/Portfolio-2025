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