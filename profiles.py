import base64
import streamlit as st
import requests
import os
from utils import animate_text_letter_by_letter


def get_image_base64(image_path):
    """Encodes an image to base64 for embedding in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""

# Function to render the profile section
def profile_section():
    # Custom CSS for styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Roboto:wght@300;400;700&display=swap');

    :root {
        --royal-dark: #000033; /* Pure Royal Navy Blue */
        --royal-accent: #FFD700; /* Gold */
        --royal-light-text: #F0F8FF; /* AliceBlue for soft contrast */
        --royal-secondary-bg: #00004d; /* Slightly lighter navy for secondary elements */
        --royal-shadow: rgba(0, 0, 0, 0.5);
    }

    body {
        font-family: 'Roboto', sans-serif;
        color: var(--royal-light-text);
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        color: var(--royal-accent);
    }

    /* Section Styling */
    .royal-section {
        background-color: var(--royal-dark);
        padding: 0.75rem 2rem; /* Minimized vertical padding to just contain text */
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 15px var(--royal-shadow); /* Softer shadow */
        animation: fadeIn 1s ease-out;
        max-width: 900px; /* Increased breadth */
        margin-left: auto;
        margin-right: auto;
    }

    /* Header Styling */
    .royal-header {
        text-align: center;
        margin-bottom: 2rem;
        position: relative; /* Added for particle positioning */
        overflow: hidden; /* Hide particles outside header bounds */
    }
    .royal-header h1 {
        font-size: 3.5rem;
        color: var(--royal-accent); /* Ensure text is visible */
        text-shadow: 0 0 5px rgba(255, 215, 0, 0.5), 0 0 10px rgba(255, 215, 0, 0.3); /* Subtle golden glow */
    }
    .royal-header h2 {
        font-size: 2rem;
        color: var(--royal-accent); /* Ensure text is visible */
        text-shadow: 0 0 5px rgba(255, 215, 0, 0.5), 0 0 10px rgba(255, 215, 0, 0.3); /* Subtle golden glow */
        margin-top: 0.5rem;
    }

    /* Profile Picture */
    .profile-pic-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    .profile-pic {
        width: 120px;
        height: 120px; /* Further reduced height */
        border-radius: 50%;
        object-fit: cover;
        border: 5px solid var(--royal-accent);
        box-shadow: 0 0 20px var(--royal-accent), 0 0 40px rgba(0,0,0,0.5); /* Adjusted shadow for consistency */
        transition: transform 0.3s ease-in-out;
    }
    .profile-pic:hover {
        transform: scale(1.05);
    }

    /* Profile Description Styling */
    .profile-text-royal { 
        font-size: 1.1rem; 
        color: var(--royal-light-text); /* Changed to light text for better contrast */
        line-height: 1.8; 
        text-align: justify; /* Changed to justify for a more formal look */
        max-width: 700px; /* Increased width for readability */
        margin: 0 auto; 
        padding: 0.5rem 1rem; /* Reduced vertical padding to minimum */
        background: var(--royal-secondary-bg);
        border-radius: 10px;
        box-shadow: 0 5px 15px var(--royal-shadow);
        border-left: 5px solid var(--royal-accent);
        animation: slideInFromLeft 1s ease-out;
    }
    .profile-text-royal strong {
        color: var(--royal-accent);
    }

    /* Image Gallery Styling */
    .image-card-royal {
        text-align: center;
        max-width: 350px;
        background: var(--royal-secondary-bg);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 15px var(--royal-shadow);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        margin: 1rem auto; /* Center cards in columns */
    }
    .image-card-royal:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 25px var(--royal-accent); /* Consistent golden glow */
    }
    .image-card-royal img {
        width: 100%;
        height: 280px; /* Slightly increased height */
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    .image-card-royal img:hover {
        transform: scale(1.02);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInFromLeft {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes textGlow {
        0% { text-shadow: 0 0 5px var(--royal-accent); }
        100% { text-shadow: 0 0 20px var(--royal-accent), 0 0 30px var(--royal-accent); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    @keyframes letterReveal {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    

    /* Social Icons */
    .social-icons {
        text-align: center;
        margin-top: 2rem;
    }
    .social-icons a {
        color: var(--royal-light-text);
        font-size: 2rem;
        margin: 0 15px;
        transition: color 0.3s ease, transform 0.3s ease;
    }
    .social-icons a:hover {
        color: var(--royal-accent);
        transform: translateY(-5px) scale(1.1);
    }

    /* Royal Name Bar */
    .royal-name-bar {
        background-color: var(--royal-dark); /* Use the main navy blue */
        padding: 1.5rem 1rem;
        text-align: center;
        border-radius: 10px;
        margin-top: 2rem; /* Space from elements above */
        box-shadow: 0 5px 15px var(--royal-shadow);
        animation: fadeIn 1.5s ease-out;
    }
    .royal-name-bar h1 {
        font-size: 2.5rem;
        color: var(--royal-accent); /* Ensure text is visible */
        margin-bottom: 0.5rem;
        text-shadow: 0 0 10px var(--royal-accent), 0 0 20px rgba(255, 215, 0, 0.5); /* More pronounced golden glow */
    }
    .royal-name-bar h2 {
        font-size: 1.5rem;
        color: var(--royal-light-text);
        margin-top: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    

    # Profile Section Title Bar (similar to other sections)
    # Main Profile Section Container
    st.markdown(f"""
    <div id='profile' class='royal-section'>
        <div class='royal-header'>
            <h1>{animate_text_letter_by_letter("Syed Shahid Nazeer", tag='span', delay_per_letter=0.10, animation_duration=3.5)}</h1>
            <h2>{animate_text_letter_by_letter("AI Generalist", tag='span', delay_per_letter=0.10, animation_duration=3.5)}</h2>
            <div class="royal-header-particles">
                <span>⚡</span><span>⚡</span><span>⚡</span><span>⚡</span><span>⚡</span><span>⚡</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Create columns for side-by-side layout
    col1, col2 = st.columns([1, 4]) # Adjusted ratios for better balance

    with col1:
        # Profile Picture (Placeholder - Update path if needed)
        profile_pic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', 'profile_pic.webp')
        if os.path.exists(profile_pic_path):
            profile_pic_base64 = get_image_base64(profile_pic_path)
            st.markdown(f"""
            <div class='profile-pic-container'>
                <img src='data:image/webp;base64,{profile_pic_base64}' class='profile-pic' alt='Profile Picture'>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"Profile picture not found at {profile_pic_path}. Please add 'profile_pic.webp' to your 'images' folder.")
            st.markdown("<div class='profile-pic-container'><div class='profile-pic' style='background-color: #555; display: flex; align-items: center; justify-content: center; font-size: 3rem;'>👤</div></div>", unsafe_allow_html=True)

    with col2:
        # Profile Description
        st.markdown("""
        <div class='profile-text-royal'>
            A versatile AI Generalist driving innovation at the forefront of intelligent system development. Mastering **Generative AI**, Large Language Models (LLMs), Natural Language Processing (NLP), and advanced Data Science, I possess proven expertise in **prompt engineering**, architecting robust Retrieval-Augmented Generation (RAG) systems, and optimizing **MLOps pipelines**. Passionate about 'Vibe Coding' to transform complex data into intuitive, high-impact AI solutions that deliver tangible real-world value.
        </div>
        """, unsafe_allow_html=True)

    

    # Image Gallery
    st.markdown("<h2 style='text-align: center; color: var(--royal-accent); margin-top: 3rem;'>AI Gallery</h2>", unsafe_allow_html=True)
    
    # Determine the correct path to images
    base_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(base_path, 'images')
    
    # Dynamically load all images from the directory
    if os.path.exists(images_path):
        image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and f != 'profile_pic.webp'] # Exclude profile pic
        
        if image_files:
            num_cols = min(len(image_files), 3)  # Limit columns to 3 for responsiveness
            cols = st.columns(num_cols)
            
            for i, img_file in enumerate(image_files):
                img_path = os.path.join(images_path, img_file)
                
                # Display images in columns
                with cols[i % num_cols]:
                    if os.path.exists(img_path):
                        img_base64 = get_image_base64(img_path)
                        st.markdown(f"""
                            <div class='image-card-royal'>
                                <img src='data:image/png;base64,{img_base64}' alt='{img_file}'>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"Image not found: {img_path}")
        else:
            st.info("No images found in the 'images' directory (excluding profile_pic.webp).")
    else:
        st.error("The 'images' directory does not exist.")

    st.markdown("</div>", unsafe_allow_html=True) # Close royal-section