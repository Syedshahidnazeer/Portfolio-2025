import streamlit as st
import os
from typing import List, Dict, Callable
from datetime import datetime
import base64
import nbformat
import nbconvert
import pandas as pd
from PIL import Image
sample_skills = [
    {
        "name": "MS Excel",
        "logo_path": "logos/excel_logo.png",
        "version": "Microsoft Excel 2021",
        "functionality": "Spreadsheet software used for data entry, manipulation, analysis, and visualization.",
        "use": "Widely used for financial analysis, data tracking, and simple statistical analysis.",
        "samples": [
            {
                "name": "Financial Dashboard",
                "file_path": "samples/excel/financial_dashboard.xlsx",
                "description": "A comprehensive financial dashboard with pivot tables and charts."
            },
            {
                "name": "Data Analysis with Pivot Tables",
                "file_path": "samples/excel/data_analysis.xlsx",
                "description": "Customer data analysis using advanced Excel functions and pivot tables."
            }
        ]
    },
    {
        "name": "Python",
        "logo_path": "logos/python_logo.png",
        "version": "Python 3.9",
        "functionality": "High-level programming language with extensive libraries for data analysis and machine learning.",
        "use": "Widely used for data manipulation, statistical analysis, machine learning, and automation.",
        "samples": [
            {
                "name": "Data Cleaning and EDA",
                "file_path": "samples/python/data_cleaning_eda.py",
                "description": "Python script for data cleaning and exploratory data analysis using pandas and matplotlib."
            },
            {
                "name": "Machine Learning Model",
                "file_path": "samples/python/machine_learning_model.ipynb",
                "description": "Jupyter notebook containing a machine learning model for customer churn prediction."
            }
        ]
    },
    {
        "name": "MySQL",
        "logo_path": "logos/mysql_logo.png",
        "version": "MySQL 8.0",
        "functionality": "Database management system used for storing, retrieving, and managing data in relational databases.",
        "use": "Essential for managing large datasets, performing complex queries, and ensuring data integrity in data science projects.",
        "samples": [
            {
                "name": "Customer Database Query",
                "query": """
SELECT c.customer_id, c.name, COUNT(o.order_id) as order_count, SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY c.customer_id, c.name
HAVING total_spent > 1000
ORDER BY total_spent DESC;
                """,
                "description": "Query that identifies high-value customers who spent over $1000 in 2022."
            },
            {
                "name": "Product Performance Analysis",
                "query": """
WITH product_metrics AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        SUM(oi.quantity) as total_quantity,
        SUM(oi.quantity * oi.unit_price) as total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_date >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    product_id,
    product_name,
    category,
    total_quantity,
    total_revenue,
    RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) as category_rank
FROM product_metrics
ORDER BY category, category_rank;
                """,
                "description": "Advanced SQL query using window functions to rank products by revenue within each category."
            }
        ]
    },
    {
        "name": "Power BI",
        "logo_path": "logos/powerbi_logo.png",
        "version": "Power BI 2021",
        "functionality": "Data visualization tool used for creating interactive and shareable dashboards.",
        "use": "Used to visualize complex datasets, identify trends, and aid in data-driven decision making.",
        "samples": [
            {
                "name": "Sales Performance Dashboard",
                "embed_url": "https://app.powerbi.com/view?r=your_embed_code_here",  # Replace with your actual embed code
                "description": "Interactive dashboard showing sales performance by region, product, and time period."
            },
            {
                "name": "Customer Analysis Dashboard",
                "image_path": "samples/powerbi/customer_dashboard.png",
                "description": "Dashboard analyzing customer demographics, purchasing behavior, and lifetime value."
            }
        ]
    },
    {
        "name": "Analytics and Statistics",
        "logo_path": "logos/analytics_logo.png",
        "version": "Various tools and packages",
        "functionality": "Techniques and tools for analyzing data and drawing statistical inferences.",
        "use": "Used for predictive modeling, hypothesis testing, and data-driven insights in various domains.",
        "samples": [
            {
                "name": "Statistical Analysis Report",
                "file_path": "samples/analytics/statistical_analysis.pdf",
                "description": "Comprehensive report on statistical methods applied to a real-world dataset."
            },
            {
                "name": "Predictive Modeling",
                "file_path": "samples/analytics/predictive_modeling.ipynb",
                "description": "Jupyter notebook demonstrating predictive modeling techniques using scikit-learn."
            }
        ]
    },
    {
        "name": "Tableau",
        "logo_path": "logos/tableau_logo.png",
        "version": "Tableau 2022",
        "functionality": "Data visualization tool used for creating interactive dashboards and reports.",
        "use": "Widely used for business intelligence, data exploration, and storytelling.",
        "samples": [
            {
                "name": "Sales Trends Dashboard",
                "image_path": "samples/tableau/sales_trends.png",
                "description": "Static image of a Tableau dashboard showcasing sales trends over time."
            },
            {
                "name": "Customer Segmentation",
                "embed_url": "https://public.tableau.com/views/your_view_id",  # Replace with your actual Tableau Public URL
                "description": "Interactive Tableau visualization segmenting customers based on purchasing behavior."
            }
        ]
    },
    {
        "name": "R Programming",
        "logo_path": "logos/r_logo.png",
        "version": "R 4.2",
        "functionality": "Statistical programming language used for data analysis, visualization, and machine learning.",
        "use": "Popular in academia and research for statistical modeling and data visualization.",
        "samples": [
            {
                "name": "Exploratory Data Analysis",
                "file_path": "samples/r/eda_script.R",
                "description": "R script for exploratory data analysis using ggplot2 and dplyr."
            },
            {
                "name": "Statistical Modeling",
                "file_path": "samples/r/statistical_modeling.Rmd",
                "description": "R Markdown document demonstrating statistical modeling techniques."
            }
        ]
    }
]
# Function to load custom CSS styles
def load_styles() -> None:
    """Load custom CSS styles for the skills section."""
    st.markdown("""
        <style>
        /* Skill Card Styling */
        .skill-card {
            background-color: var(--section-background-color);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            display: flex;
            align-items: flex-start;
        }
        .skill-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
        }

        .skill-logo-container {
            flex-shrink: 0;
            margin-right: 20px;
        }

        .skill-details-content {
            flex-grow: 1;
        }

        /* Skill Title */
        .skill-title {
            font-size: 20px;
            color: var(--primary-color);
            margin-bottom: 5px;
        }

        /* Skill Version */
        .skill-version {
            font-size: 14px;
            color: var(--text-color);
            margin-bottom: 10px;
        }

        /* Skill Description */
        .skill-description {
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

# Function to render an individual skill card
def render_skill_card(skill: Dict[str, str], get_image_base64: Callable, show_detailed: bool = False) -> None:
    """Render an individual skill card."""
    # Start building the HTML string for the main card content
    card_html = f"""
    <div class="skill-card">
        <div class="skill-logo-container">
    """
    if 'logo_path' in skill and os.path.exists(skill['logo_path']):
        logo_base64 = get_image_base64(skill['logo_path'])
        card_html += f"""<img src="data:image/png;base64,{logo_base64}" width="50" alt="{skill['name']} Logo">"""
    else:
        card_html += f"""<div class="skill-icon">🎓</div>""" # Using a div for icon as per CSS

    card_html += f"""
        </div>
        <div class="skill-details-content">
            <div class="skill-title">{skill['name']}</div>
            <div class="skill-version">Version: {skill['version']}</div>
            <div class="skill-description"><b>Functionality:</b> {skill['functionality']}</div>
            <div class="skill-description"><b>Uses in Data Science and Analytics:</b> {skill['use']}</div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # Handle work samples separately as they contain interactive Streamlit components
    if 'samples' in skill and skill['samples']:
        with st.expander(f"View my {skill['name']} work samples"):
            for sample in skill['samples']:
                st.subheader(sample['name'])
                st.write(sample['description'])

                # Display different types of content based on the sample type
                if 'file_path' in sample:
                    if sample['file_path'].endswith(".xlsx"):
                        try:
                            df = pd.read_excel(sample['file_path'])
                            st.dataframe(df)

                            with open(sample['file_path'], "rb") as file:
                                st.download_button(
                                    label="Download Excel File",
                                    data=file,
                                    file_name=os.path.basename(sample['file_path']),
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        except Exception as e:
                            st.error(f"Error displaying Excel file: {e}")

                    elif sample['file_path'].endswith(".py"):
                        try:
                            with open(sample['file_path'], "r") as file:
                                code = file.read()
                            st.code(code, language="python")

                            with open(sample['file_path'], "rb") as file:
                                st.download_button(
                                    label="Download Python File",
                                    data=file,
                                    file_name=os.path.basename(sample['file_path']),
                                    mime="text/plain"
                                )
                        except Exception as e:
                            st.error(f"Error displaying Python file: {e}")

                    elif sample['file_path'].endswith(".ipynb"):
                        try:
                            from nbformat import read as read_notebook
                            from nbconvert import HTMLExporter

                            notebook_content = read_notebook(sample['file_path'], as_version=4)
                            html_exporter = HTMLExporter()
                            (body, _) = html_exporter.from_notebook_node(notebook_content)

                            st.components.v1.html(body, height=600)

                            with open(sample['file_path'], "rb") as file:
                                st.download_button(
                                    label="Download Jupyter Notebook",
                                    data=file,
                                    file_name=os.path.basename(sample['file_path']),
                                    mime="application/x-ipynb+json"
                                )
                        except Exception as e:
                            st.error(f"Error displaying Jupyter notebook: {e}")

                elif 'embed_url' in sample:
                    try:
                        iframe_code = f"""
                        <iframe src="{sample['embed_url']}" width="100%" height="600" frameborder="0"></iframe>
                        """
                        st.markdown(iframe_code, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error displaying Power BI dashboard: {e}")

                elif 'query' in sample:
                    st.markdown("### Query Example")
                    st.code(sample['query'], language="sql")
                    st.markdown(f"**Description:** {sample['description']}")

# Main function to render the skills section
def render_skills_section(skills: List[Dict[str, str]], get_image_base64: Callable) -> None:
    """Render the enhanced skills section with all features."""
    st.markdown("""
    <div id='skills' class='section fade-in'>
        <h2 style='text-align: center;'>🛠️ My Skills</h2>
    </div>
    """, unsafe_allow_html=True)
    st.write("Explore my technical skills and tools expertise.")
    
    # Load custom styles
    load_styles()
    
    # Extract all unique categories and versions for filtering
    all_categories = sorted(list(set(skill['name'] for skill in skills)))
    
    # Filters and search section
    search_query = st.text_input("🔍 Search skills", key="skill_search", help="Search by name, functionality, or use cases")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_categories = st.multiselect("Filter by Skill", options=all_categories, help="Select one or more skills")
    
    with col2:
        sort_option = st.selectbox("Sort by", options=["Alphabetical", "Most Recent"], help="Choose how to sort skills")
    
    # Display mode
    view_mode = st.radio("View Mode", ["Grid View", "Detailed View"], horizontal=True)
    
    # Apply filters and search
    filtered_skills = skills.copy()
    
    if search_query:
        filtered_skills = [
            skill for skill in filtered_skills if 
            search_query.lower() in skill['name'].lower() or
            ('functionality' in skill and search_query.lower() in skill['functionality'].lower()) or
            ('use' in skill and search_query.lower() in skill['use'].lower())
        ]
    
    if selected_categories:
        filtered_skills = [
            skill for skill in filtered_skills if 
            skill['name'] in selected_categories
        ]
    
    # Sort skills
    if sort_option == "Alphabetical":
        filtered_skills = sorted(filtered_skills, key=lambda x: x['name'])
    elif sort_option == "Most Recent":
        filtered_skills = sorted(filtered_skills, key=lambda x: datetime.strptime(x.get('version', '2000'), "%Y"), reverse=True)
    
    # Display filtered skills
    if not filtered_skills:
        st.info("No skills match your search criteria. Try adjusting your filters.")
    else:
        st.write(f"Displaying {len(filtered_skills)} skill(s)")
        
        if view_mode == "Grid View":
            # Display in grid view (3 columns)
            num_cols = 3
            rows = [filtered_skills[i:i + num_cols] for i in range(0, len(filtered_skills), num_cols)]
            
            for row in rows:
                cols = st.columns(num_cols)
                for i, skill in enumerate(row):
                    with cols[i]:
                        render_skill_card(skill, get_image_base64=get_image_base64, show_detailed=False)
        else:
            # Display in detailed view (1 column)
            for skill in filtered_skills:
                render_skill_card(skill, get_image_base64=get_image_base64, show_detailed=True)
                st.markdown("---")
