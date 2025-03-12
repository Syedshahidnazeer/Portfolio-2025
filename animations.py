import streamlit as st

def animate_button():
    return """
    <style>
    .animate-button {
        transition: all 0.5s ease;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        background-color: #4CAF50; /* Green */
        color: white;
        border: none;
    }
    
    .animate-button:hover {
        background-color: #3e8e41; /* Darker green */
        transform: scale(1.1); /* Scale up a bit */
    }
    </style>
    """

def animate_text():
    return """
    <style>
    .animate-text {
        transition: all 0.5s ease;
        padding: 20px;
        font-size: 24px;
        text-align: center;
        cursor: pointer;
        color: #333;
    }
    
    .animate-text:hover {
        color: #FF5733; /* Orange */
        transform: translateY(-10px); /* Slide up a bit */
        opacity: 0.8; /* Fade in a bit more */
    }
    </style>
    """

def animate_box():
    return """
    <style>
    .animate-box {
        transition: all 0.5s ease;
        padding: 20px;
        border: 2px solid #ccc;
        text-align: center;
        cursor: pointer;
        background-color: #f9f9f9;
    }
    
    .animate-box:hover {
        background-color: #e1e1e1; /* Light grey */
        transform: scale(1.05); /* Scale up a bit more */
        box-shadow: 0 4px 8px rgba(0,0,0,0.2); /* Add shadow */
    }
    </style>
    """

def main():
    st.set_page_config(page_title="Portfolio", page_icon="👋")
    
    # Navigation bar
    st.markdown(
        """
        <style>
        .navbar {
            background-color: #333;
            overflow: hidden;
        }

        .navbar a {
            float: left;
            display: block;
            color: white;
            text-align: center;
            padding: 14px 20px;
            text-decoration: none;
            transition: all 0.5s ease;
        }
        
        .navbar a:hover {
            background-color: #ddd;
            color: black;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    st.markdown(
        '<a href="#home">Home</a> <a href="#projects">Projects</a> <a href="#contact">Contact</a>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Home section
    st.title("Welcome to My Portfolio")
    st.write(animate_text(), unsafe_allow_html=True)
    st.image("https://via.placeholder.com/600x400?text=Welcome+to+My+Portfolio", caption="Placeholder Image", use_column_width=True)
    
    # Projects section
    st.markdown("---")
    st.header("Projects")
    
    project1 = """
    <div class="animate-box">
        <h3>Project 1</h3>
        <p>Description of Project 1...</p>
    </div>
    """
    
    project2 = """
    <div class="animate-box">
        <h3>Project 2</h3>
        <p>Description of Project 2...</p>
    </div>
    """
    
    st.write(project1, unsafe_allow_html=True)
    st.write(project2, unsafe_allow_html=True)
    
    # Contact section
    st.markdown("---")
    st.header("Contact Me")
    
    contact_form = """
    <form action="https://formsubmit.co/your_email@example.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="email" name="_replyto" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message..." required></textarea>
        <button class="animate-button" type="submit">Send</button>
    </form>
    """
    
    st.write(contact_form, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
