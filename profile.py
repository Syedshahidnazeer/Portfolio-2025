import streamlit as st
import os

def profile_section():
    st.markdown("<div class='header'><h1>Syed Shahid Nazeer</h1><h2>Financial Analyst</h2></div>", unsafe_allow_html=True)
    st.markdown("<div id='profile' class='section'><h2>Profile</h2></div>", unsafe_allow_html=True)
    
    # Add some CSS for styling
    st.markdown(
        """
        <style>
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .profile-container {
            max-width: 80%;
            margin: 0 auto;
        }
        .profile-text {
            font-size: 16px;
            color: #555;
            line-height: 1.6;
            text-align: justify;
        }
        .gallery-container {
            display: flex;
            overflow-x: scroll;
            padding: 20px;
            border-radius: 8px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .gallery-item {
            flex: 0 0 auto;
            margin-right: 15px;
            transition: transform 0.3s ease-in-out;
        }
        .gallery-item:hover {
            transform: scale(1.05);
        }
        .gallery-item img {
            width: 150px;
            height: 150px;
            object-fit: cover;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Profile text with animation
    st.markdown("""
    <div class='profile-text'>
        <p>Aspiring Financial Analyst with hands-on experience in data collection, analysis, and reporting. 
           Proficient in Excel, Power BI, and SQL, with a strong foundation in business application skills. 
           Skilled in providing financial analysis, handling business issues, and delivering actionable insights. 
           Excellent communication and teamwork abilities, with a keen eye for detail and accuracy. 
           Adept at translating complex financial data into strategic recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

# Image list with paths
    images = [
        {"title": "Image 1", "path": "./images/image1.png"},
        {"title": "Image 2", "path": "./images/image2.png"},
        {"title": "Image 3", "path": "./images/image3.png"},
        {"title": "Image 4", "path": "./images/image4.webp"},
        {"title": "Image 5", "path": "./images/image5.webp"}
    ]

    # Check if images exist
    existing_images = [img for img in images if os.path.exists(img['path'])]

    # Initial index for the gallery
    index = 0

    # Container for the gallery to update dynamically
    gallery_container = st.container()

    # Navigation buttons container
    nav_container = st.container()

    with nav_container:
        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Previous"):
                index = (index - 1) % len(existing_images)
        with col2:
            if st.button("Next"):
                index = (index + 1) % len(existing_images)

    with gallery_container:
        # Display current image with a brief description
        if existing_images:
            current_image = existing_images[index]
            st.image(current_image['path'], caption=current_image['title'], width=600)  # Adjust width as needed
        else:
            st.write("No images found in the specified directory.")

    with gallery_container:
        # Add some basic styling for a carousel feel
        st.markdown(
            """
            <style>
            .gallery-container {
                max-width: 80%;
                margin: auto;
                overflow: hidden;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .gallery-image {
                display: block;
                margin: auto;
            }
            </style>
            """, unsafe_allow_html=True
        )

        # Display current image with a brief description, wrapped in a div for styling
        if existing_images:
            current_image = existing_images[index]
            st.markdown(f"""
                <div class='gallery-container'>
                    <img class='gallery-image' src='{current_image['path']}' width='600' alt='{current_image['title']}'>
                    <p style='text-align:center'>{current_image['title']}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.write("No images found in the specified directory.")

