import streamlit as st
import os
from typing import List
from streamlit_lottie import st_lottie
import requests

# Helper function to load Lottie animations
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

# Function to render the profile section
def profile_section():
    # Custom CSS for styling
    st.markdown("""
    <style>
    /* Header Styling */
    .header {
        text-align: center;
        margin-bottom: 40px;
        animation: fadeIn 1s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Profile Description Styling */
    .profile-text { 
        font-size: 16px; 
        color: var(--text-color); 
        line-height: 1.6; 
        text-align: justify; 
        max-width: 800px; 
        margin: 0 auto; 
        padding: 20px;
        background: var(--secondary-background-color);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .profile-text:hover {
        transform: translateY(-5px);
    }

    /* Image Gallery Styling */
    .image-gallery {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-top: 2rem;
    }
    .image-card {
        text-align: center;
        max-width: 300px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-radius: 10px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .image-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 12px rgba(0,0,0,0.2);
    }
    .image-card img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        transition: transform 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    # Profile Header with Synthwave84 Font
    st.markdown("<div class='header'><h1>Syed Shahid Nazeer</h1></div>", unsafe_allow_html=True)
    
    # Profile Subtitle
    st.markdown("<h2>AI Generalist</h2>", unsafe_allow_html=True)

    # Profile Description
    st.markdown("""
    <div class='profile-text'>
        A versatile AI Generalist driving innovation at the forefront of intelligent system development. Mastering **Generative AI**, Large Language Models (LLMs), Natural Language Processing (NLP), and advanced Data Science, I possess proven expertise in **prompt engineering**, architecting robust Retrieval-Augmented Generation (RAG) systems, and optimizing **MLOps pipelines**. Passionate about 'Vibe Coding' to transform complex data into intuitive, high-impact AI solutions that deliver tangible real-world value.
    </div>
    """, unsafe_allow_html=True)

    # Lottie Animation for Hero Section
    lottie_url = "https://assets9.lottiefiles.com/packages/lf20_gssu2dkm.json"
    lottie_animation = load_lottieurl(lottie_url)
    if lottie_animation:
        st_lottie(lottie_animation, height=300, key="hero-animation")
    else:
        st.warning("Failed to load Lottie animation.")

    # Image Gallery
    st.header("Image Gallery")
    
    # Determine the correct path to images
    base_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(base_path, 'images')
    
    # Dynamically load all images from the directory
    if os.path.exists(images_path):
        image_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        
        if image_files:
            num_cols = min(len(image_files), 3)  # Limit columns to 3 for responsiveness
            cols = st.columns(num_cols)
            
            for i, img_file in enumerate(image_files):
                img_path = os.path.join(images_path, img_file)
                
                # Display images in columns
                with cols[i % num_cols]:
                    if os.path.exists(img_path):
                        st.image(img_path, use_container_width=True)
                    else:
                        st.error(f"Image not found: {img_path}")
        else:
            st.info("No images found in the 'images' directory.")
    else:
        st.error("The 'images' directory does not exist.")