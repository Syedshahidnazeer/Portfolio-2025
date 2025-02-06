import streamlit as st
import os
from typing import Dict, List

def profile_section():
    st.markdown("<div class='header'><h1>Syed Shahid Nazeer</h1><h2>Financial Analyst</h2></div>", unsafe_allow_html=True)
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .header { text-align: center; margin-bottom: 40px; }
    .profile-text { 
        font-size: 16px; 
        color: #555; 
        line-height: 1.6; 
        text-align: justify; 
        max-width: 800px; 
        margin: 0 auto; 
        padding: 20px;
    }
    .image-gallery {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .image-card {
        text-align: center;
        max-width: 300px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-radius: 10px;
        overflow: hidden;
        transition: transform 0.3s ease;
    }
    .image-card:hover {
        transform: scale(1.05);
    }
    .image-card img {
        width: 100%;
        height: 250px;
        object-fit: cover;
    }
    </style>
    """, unsafe_allow_html=True)

    # Profile description
    st.markdown("""
    <div class='profile-text'>
        Aspiring Financial Analyst with hands-on experience in data collection, analysis, and reporting. 
        Proficient in Excel, Power BI, and SQL, with a strong foundation in business application skills. 
        Skilled in providing financial analysis, handling business issues, and delivering actionable insights. 
        Excellent communication and teamwork abilities, with a keen eye for detail and accuracy. 
        Adept at translating complex financial data into strategic recommendations.
    </div>
    """, unsafe_allow_html=True)

    # Image gallery
    st.header("Image Gallery")
    
    # Determine the correct path to images
    base_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(base_path, 'images')
    
    # List of images
    image_files = [
        'image1.png', 'image2.png', 'image3.png', 
        'image4.webp', 'image5.webp'
    ]
    
    # Create columns for image display
    cols = st.columns(3)
    
    # Display images
    for i, img_file in enumerate(image_files):
        img_path = os.path.join(images_path, img_file)
        
        # Check if image exists
        if os.path.exists(img_path):
            with cols[i % 3]:
                st.image(img_path, caption=f'Image {i+1}', use_container_width=True)
        else:
            st.warning(f"Image not found: {img_path}")