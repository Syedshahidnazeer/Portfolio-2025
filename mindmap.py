import streamlit as st
import json
from PIL import Image

# Load your MySQL data (replace with your actual data structure)
mysql_data = {
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
}

# App configuration
st.set_page_config(
    page_title="MySQL Query Showcase",
    page_icon=":bar_chart:",
    layout="wide"
)

# Header section
st.title(f"📚 {mysql_data['name']} ({mysql_data['version']})")

# Logo and basic info
col1, col2 = st.columns([1, 3])
with col1:
    try:
        logo = Image.open(mysql_data['logo_path'])
        st.image(logo, use_column_width=True)
    except FileNotFoundError:
        st.error(f"Logo not found at: {mysql_data['logo_path']}")

with col2:
    st.header("Overview")
    st.markdown(f"**Functionality**: {mysql_data['functionality']}")
    st.markdown(f"**Use Case**: {mysql_data['use']}")

# Samples section
st.header("Sample Queries")
for sample in mysql_data['samples']:
    with st.expander(f"🔍 {sample['name']}"):
        st.markdown(f"**Description**: {sample['description']}")
        st.code(sample['query'], language='sql')
        st.button(f"Copy to clipboard", key=f"copy_{sample['name']}")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using Streamlit")