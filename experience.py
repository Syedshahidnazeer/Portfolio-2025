import streamlit as st
from experience_data import sample_experiences
from utils import animate_text_letter_by_letter

def load_styles():
    st.markdown("""
        <style>
        hr {
            border: none;
            border-top: 2px solid var(--royal-accent); /* Use royal accent color */
            margin: 20px 0;
        }
        .experience-card {
            background-color: var(--royal-secondary-bg); /* Use royal secondary background */
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px var(--royal-shadow); /* Use royal shadow */
            display: flex;
            align-items: flex-start;
            color: var(--royal-light-text); /* Default text color for card content */
        }
        .experience-card h3 {
            color: var(--royal-accent); /* Headings in gold */
        }
        .experience-card p,
        .experience-card li,
        .experience-card div {
            color: var(--royal-light-text); /* Ensure all text within card is light */
        }
        .experience-card h4 {
            color: var(--royal-accent); /* Subheadings in gold */
        }
        .experience-card li {
            color: var(--royal-light-text); /* List items in light text */
        }
        .experience-logo-container {
            flex-shrink: 0;
            margin-right: 20px;
        }
        .experience-details-content {
            flex-grow: 1;
        }
        .experience-company-info {
            font-size: 1.05rem;
            color: var(--royal-light-text);
            margin-bottom: 0.3rem;
        }
        .experience-company-info b {
            color: var(--royal-accent);
        }
        .experience-duration {
            font-size: 0.9rem;
            color: var(--royal-light-text);
            margin-bottom: 0.8rem;
        }
        </style>
    """, unsafe_allow_html=True)

import base64
import os

def get_image_base64(image_path):
    """Encodes an image to base64 for embedding in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

def render_experience_section(sample_experiences):
    load_styles()
    st.markdown(f"""
    <div id='experience' class='section fade-in'>
        <h2 style='text-align: center;'>{animate_text_letter_by_letter("Work Experience", tag='span', delay_per_letter=0.10, animation_duration=3.5)}</h2>
        <div class="royal-header-particles">
            <span>💼</span><span>📈</span><span>🤝</span><span>🚀</span><span>💡</span><span>✨</span><span>🌟</span><span>💪</span><span>🏢</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for experience in sample_experiences:
        logo_html = ""
        if "logo_path" in experience and os.path.exists(experience["logo_path"]):
            logo_base64 = get_image_base64(experience["logo_path"])
            logo_html = f"<img src='data:image/png;base64,{logo_base64}' width='100'>"

        description_html = ""
        if experience["description"]:
            description_html = f"<p>{experience['description']}</p>"

        responsibilities_html = ""
        if experience["responsibilities"]:
            responsibilities_items = "".join([f"<li>{item}</li>" for item in experience["responsibilities"]])
            responsibilities_html = f"<h4>Responsibilities:</h4><ul>{responsibilities_items}</ul>"

        card_html = f"""
        <div class='experience-card card'>
            <div class='experience-logo-container'>
                {logo_html}
            </div>
            <div class='experience-details-content'>
                <h3>{experience['title']}</h3>
                <div class='experience-company-info'>
                    <b>{experience['company']}</b> | {experience['location']}
                </div>
                <div class='experience-duration'>
                    <i>{experience['duration']}</i>
                </div>
                {description_html}
                {responsibilities_html}
            </div>
        </div>
        <hr>
        """
        st.markdown(card_html, unsafe_allow_html=True)
