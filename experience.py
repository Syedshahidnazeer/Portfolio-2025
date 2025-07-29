import streamlit as st
from experience_data import sample_experiences

def render_experience_section(sample_experiences):
    st.markdown("""
    <div id='experience' class='section fade-in'>
        <h2 style='text-align: center;'>Work Experience</h2>
    </div>
    """, unsafe_allow_html=True)

    for experience in sample_experiences:
        col1, col2 = st.columns([1, 4])
        with col1:
            if "logo_path" in experience:
                st.image(experience["logo_path"], width=100)
        with col2:
            st.subheader(experience["title"])
            st.write(f"**{experience['company']}** | {experience['location']}")
            st.write(f"*{experience['duration']}*")
            if experience["description"]:
                st.write(experience["description"])
            if experience["responsibilities"]:
                st.write("**Responsibilities:**")
                for item in experience["responsibilities"]:
                    st.write(f"- {item}")
        st.markdown("<hr>", unsafe_allow_html=True)
