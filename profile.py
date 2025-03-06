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
    /* Load Synthwave84 Font */
    @font-face {
        font-family: 'Synthwave84';
        src: url('https://fonts.cdnfonts.com/s/20976/Synthwave84-Regular.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }

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

    /* Synthwave Text Styling */
    .synthwave-text {
        font-family: 'Synthwave84', sans-serif;
        color: #FF00FF; /* Neon pink for synthwave vibe */
        text-shadow: 0 0 10px #FF00FF, 0 0 20px #FF00FF, 0 0 30px #FF00FF;
        font-size: 2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        animation: neon-glow 1.5s infinite alternate;
    }

    /* Neon Glow Animation */
    @keyframes neon-glow {
        from {
            text-shadow: 0 0 10px #FF00FF, 0 0 20px #FF00FF, 0 0 30px #FF00FF;
        }
        to {
            text-shadow: 0 0 20px #FF00FF, 0 0 30px #FF00FF, 0 0 40px #FF00FF, 0 0 50px #FF00FF;
        }
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
    st.markdown("<div class='header'><h1 class='synthwave-text'>Syed Shahid Nazeer</h1></div>", unsafe_allow_html=True)
    
    # Profile Subtitle
    st.markdown("<h2 style='text-align: center;'>Financial Analyst</h2>", unsafe_allow_html=True)

    # Profile Description
    st.markdown("""
    <div class='profile-text'>
        Aspiring Financial Analyst with hands-on experience in data collection, analysis, and reporting. 
        Proficient in Excel, Power BI, and SQL, with a strong foundation in business application skills. 
        Skilled in providing financial analysis, handling business issues, and delivering actionable insights. 
        Excellent communication and teamwork abilities, with a keen eye for detail and accuracy. 
        Adept at translating complex financial data into strategic recommendations.
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
                    st.markdown(f"""
                    <div class='image-card'>
                        <img src='{img_path}' alt='Image {i+1}'>
                        <p style='margin-top: 10px;'>Image {i+1}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No images found in the 'images' directory.")
    else:
        st.error("The 'images' directory does not exist.")