import streamlit as st

def project_section():
    st.markdown("<div id='projects' class='section'><h2>Projects</h2></div>", unsafe_allow_html=True)
    
    # Add some CSS for styling
    st.markdown(
        """
        <style>
        .project-card {
            border: 1px solid #ccc;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 8px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .project-title {
            font-size: 20px;
            color: #333;
        }
        .project-type-duration {
            font-size: 14px;
            color: #555;
        }
        .project-description {
            font-size: 16px;
            color: #777;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    projects = [
        {
            "title": "Oil-Price Prediction",
            "description": "Developed an oil price prediction app for strategic decision-making and increased profitability. Mined over 35 years of oil price data using Python and yfinance, resulting in more than 11,000 values. The app maintains a variance range of 1.2% to 2% in oil price predictions, aiding strategic planning in the oil industry.",
            "duration": "March, 2023 - June, 2023",
            "type": "Ai variant Internship Project",
            "icon": "https://cdn-icons-png.flaticon.com/512/667/667984.png"
        },
        {
            "title": "Real/Fake News Detection",
            "description": "Developed a user-friendly web app leveraging advanced Natural Language Processing (NLP) techniques. Analyzed and extracted sentiment from a dataset exceeding 80,000 articles. The app offers near-instantaneous verification of news authenticity, delivering reliable results within milliseconds.",
            "duration": "July, 2023 - October, 2023",
            "type": "Ai variant Internship Project",
            "icon": "https://cdn-icons-png.flaticon.com/512/1697/1697488.png"
        },
        {
            "title": "Rating prediction of google play store apps",
            "description": "Analyzed a dataset of over 100,000 app entries using Python and sklearn, experimenting with various regression algorithms and optimizing model parameters. The result was a predictive model that achieved an impressive 93% accuracy. This model has since been instrumental in helping app developers identify trending categories and improve their app development strategies.",
            "duration": "Feb, 2022 - Jun, 2022",
            "type": "Final Semester Project",
            "icon": "https://cdn-icons-png.flaticon.com/512/816/816964.png"
        }
    ]
    
    for project in projects:
        st.markdown(f"<div class='project-card'>", unsafe_allow_html=True)
        st.markdown(f"<img src='{project['icon']}' alt='{project['title']}' style='width: 50px; margin-right: 10px;'>", unsafe_allow_html=True)
        st.markdown(f"<h3>{project['title']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p><strong>{project['type']}</strong> | {project['duration']}</p>", unsafe_allow_html=True)
        st.write(project["description"])
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

