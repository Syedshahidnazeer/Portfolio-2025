import streamlit as st
from typing import List, Dict
from datetime import datetime

# Function to load custom CSS styles
def load_styles() -> None:
    """Load custom CSS styles for the projects section."""
    st.markdown("""
        <style>
        /* Project Card Styling */
        .project-card {
            border: 1px solid var(--accent-color);
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 8px;
            background-color: var(--secondary-background-color);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            display: flex;
            align-items: flex-start;
        }
        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
        }

        /* Project Icon */
        .project-icon {
            width: 50px;
            height: 50px;
            margin-right: 15px;
            flex-shrink: 0;
        }

        /* Project Title */
        .project-title {
            font-size: 20px;
            color: var(--primary-color);
            margin-bottom: 5px;
        }

        /* Project Type and Duration */
        .project-type-duration {
            font-size: 14px;
            color: var(--text-color);
            margin-bottom: 10px;
        }

        /* Project Description */
        .project-description {
            font-size: 16px;
            color: var(--text-color);
            line-height: 1.6;
        }

        /* Filter Buttons */
        .filter-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 2rem;
        }
        .filter-button {
            padding: 10px 15px;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .filter-button:hover {
            background-color: var(--secondary-color);
        }
        </style>
    """, unsafe_allow_html=True)

# Function to render an individual project card
def render_project_card(project: Dict[str, str], show_detailed: bool = False) -> None:
    """Render an individual project card."""
    with st.container():
        # Logo or placeholder
        if 'icon' in project and project['icon']:
            st.image(project['icon'], width=50)
        else:
            st.markdown("📁", unsafe_allow_html=True)
        
        # Title and basic info
        st.markdown(f"**{project['title']}**")
        st.markdown(f"{project['type']} | {project['duration']}")
        
        # Description
        if 'description' in project:
            st.markdown(project['description'])
        
        # Tags (skills)
        if 'tags' in project and project['tags']:
            tags_list = " | ".join([f"`{tag}`" for tag in project['tags']])
            st.markdown(f"**Tags:** {tags_list}")

# Main function to render the projects section
def render_projects_section(projects: List[Dict[str, str]]) -> None:
    """Render the enhanced projects section with all features."""
    st.markdown("<div id='projects' class='section fade-in'>", unsafe_allow_html=True)
    st.header("📂 My Projects")
    st.write("Explore my professional projects and contributions.")
    
    # Load custom styles
    load_styles()
    
    # Extract all unique tags and types for filtering
    all_tags = sorted(list(set(tag for project in projects for tag in project.get('tags', []))))
    all_types = sorted(list(set(project['type'] for project in projects)))
    
    # Filters and search section
    search_query = st.text_input("🔍 Search projects", key="project_search", help="Search by title, type, or tags")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tags = st.multiselect("Filter by Tag", options=all_tags, help="Select one or more tags")
    with col2:
        selected_types = st.multiselect("Filter by Type", options=all_types, help="Select one or more types")
    with col3:
        sort_option = st.selectbox("Sort by", options=["Most Recent", "Alphabetical"], help="Choose how to sort projects")
    
    # Display mode
    view_mode = st.radio("View Mode", ["Grid View", "Detailed View"], horizontal=True)
    
    # Apply filters and search
    filtered_projects = projects.copy()
    
    if search_query:
        filtered_projects = [
            project for project in filtered_projects if 
            search_query.lower() in project['title'].lower() or
            ('type' in project and search_query.lower() in project['type'].lower()) or
            ('tags' in project and any(search_query.lower() in tag.lower() for tag in project['tags']))
        ]
    
    if selected_tags:
        filtered_projects = [
            project for project in filtered_projects if 
            'tags' in project and any(tag in selected_tags for tag in project['tags'])
        ]
    
    if selected_types:
        filtered_projects = [
            project for project in filtered_projects if 
            'type' in project and project['type'] in selected_types
        ]
    
    # Sort projects
    if sort_option == "Most Recent":
        filtered_projects = sorted(
            filtered_projects,
            key=lambda x: datetime.strptime(x['duration'].split(" - ")[0], "%B, %Y"),
            reverse=True
        )
    elif sort_option == "Alphabetical":
        filtered_projects = sorted(filtered_projects, key=lambda x: x['title'])
    
    # Display filtered projects
    if not filtered_projects:
        st.info("No projects match your search criteria. Try adjusting your filters.")
    else:
        st.write(f"Displaying {len(filtered_projects)} project(s)")
        
        if view_mode == "Grid View":
            # Display in grid view (3 columns)
            num_cols = 3
            rows = [filtered_projects[i:i + num_cols] for i in range(0, len(filtered_projects), num_cols)]
            
            for row in rows:
                cols = st.columns(num_cols)
                for i, project in enumerate(row):
                    with cols[i]:
                        render_project_card(project, show_detailed=False)
        else:
            # Display in detailed view (1 column)
            for project in filtered_projects:
                render_project_card(project, show_detailed=True)
                st.markdown("---")

# Sample project data structure
sample_projects = [
    {
        "title": "Oil-Price Prediction",
        "description": "Developed an oil price prediction app for strategic decision-making and increased profitability. Mined over 35 years of oil price data using Python and yfinance, resulting in more than 11,000 values. The app maintains a variance range of 1.2% to 2% in oil price predictions, aiding strategic planning in the oil industry.",
        "duration": "March, 2023 - June, 2023",
        "type": "AI Variant Internship Project",
        "icon": "https://cdn-icons-png.flaticon.com/512/667/667984.png",
        "tags": ["Python", "AI", "Data Science"]
    },
    {
        "title": "Real/Fake News Detection",
        "description": "Developed a user-friendly web app leveraging advanced Natural Language Processing (NLP) techniques. Analyzed and extracted sentiment from a dataset exceeding 80,000 articles. The app offers near-instantaneous verification of news authenticity, delivering reliable results within milliseconds.",
        "duration": "July, 2023 - October, 2023",
        "type": "AI Variant Internship Project",
        "icon": "https://cdn-icons-png.flaticon.com/512/1697/1697488.png",
        "tags": ["NLP", "Machine Learning", "Web Development"]
    },
    {
        "title": "Rating Prediction of Google Play Store Apps",
        "description": "Analyzed a dataset of over 100,000 app entries using Python and sklearn, experimenting with various regression algorithms and optimizing model parameters. The result was a predictive model that achieved an impressive 93% accuracy. This model has since been instrumental in helping app developers identify trending categories and improve their app development strategies.",
        "duration": "Feb, 2022 - Jun, 2022",
        "type": "Final Semester Project",
        "icon": "https://cdn-icons-png.flaticon.com/512/816/816964.png",
        "tags": ["Data Analysis", "Regression", "Python"]
    }
]

# Export the sample_projects variable
__all__ = ['render_projects_section', 'sample_projects']