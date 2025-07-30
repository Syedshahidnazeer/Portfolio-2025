import streamlit as st

# Function to detect if user is on mobile or desktop
def get_device_type():
    """
    Detect if the user is on mobile or desktop based on viewport width.
    Uses session state to store the device type and avoid recalculating on every rerun.
    """
    if 'device_type' not in st.session_state:
        # Default to desktop
        st.session_state.device_type = "desktop"

        # Inject JavaScript to detect viewport width and update session state
        st.markdown(
            """
            <script>
            const deviceType = window.innerWidth < 768 ? 'mobile' : 'desktop';
            
            // Use Streamlit's setComponentValue to update session state
            if (window.parent.streamlitPyToken) {
                const pyToken = window.parent.streamlitPyToken;
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: deviceType,
                    componentId: "device_detector"
                }, "*");
            }
            </script>
            """,
            unsafe_allow_html=True
        )
    
    return st.session_state.device_type

# Function to create responsive columns
def responsive_columns(ratios=None, gap="small"):
    """
    Create responsive columns that adjust based on device type.
    Args:
        ratios (list): List of column ratios (e.g., [1, 2] for two columns with a 1:2 ratio).
        gap (str): Gap size between columns ("small", "medium", "large").
    Returns:
        list: List of Streamlit columns.
    """
    device = get_device_type()
    
    if device == "mobile":
        # On mobile, use a single column layout
        return [st.container()]
    else:
        # On desktop, use the specified column ratios
        if ratios is None:
            ratios = [1, 1]  # Default to two equal columns
        
        # Map gap sizes to pixel values
        gap_sizes = {
            "small": "10px",
            "medium": "20px",
            "large": "30px"
        }
        
        gap_size = gap_sizes.get(gap, "10px")
        
        # Create columns with appropriate spacing
        cols = st.columns(ratios, gap=gap)
        
        return cols

# Function to create a responsive container
def responsive_container(key=None, mobile_padding="10px", desktop_padding="20px"):
    """
    Create a responsive container with appropriate padding.
    Args:
        key (str): Key for the container (optional).
        mobile_padding (str): Padding for mobile devices.
        desktop_padding (str): Padding for desktop devices.
    Returns:
        st.container: A Streamlit container with responsive padding.
    """
    device = get_device_type()
    
    padding = mobile_padding if device == "mobile" else desktop_padding
    
    # Apply responsive container styling
    container_style = f"""
    <style>
        [data-testid="stVerticalBlock"] > div:has(div[key="{key}"]) {{
            padding: {padding};
            transition: padding 0.3s ease;
        }}
    </style>
    """
    st.markdown(container_style, unsafe_allow_html=True)
    
    return st.container(key=key)

# Function to apply global responsive styles
def apply_responsive_styles():
    """
    Apply global responsive styles based on device type.
    """
    device = get_device_type()
    
    if device == "mobile":
        st.markdown("""
        <style>
            /* Mobile-specific styles */
            .stApp {
                max-width: 100vw !important;
                padding: 0 !important;
                margin: 0 !important;
            }
            
            /* Reduce font sizes on mobile */
            h1 {
                font-size: 1.8rem !important;
            }
            h2 {
                font-size: 1.5rem !important;
            }
            p, li {
                font-size: 0.9rem !important;
            }
            
            /* Adjust navbar for mobile */
            .navbar-container {
                padding: 5px !important;
                background-color: var(--royal-secondary-bg) !important; /* Ensure royal theme */
            }
            
            /* Custom scrollbar for mobile */
            ::-webkit-scrollbar {
                width: 4px;
                height: 4px;
            }
            ::-webkit-scrollbar-track {
                background: var(--royal-dark); /* Royal theme scrollbar track */
            }
            ::-webkit-scrollbar-thumb {
                background: var(--royal-accent); /* Royal theme scrollbar thumb */
                border-radius: 2px;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            /* Desktop-specific styles */
            .stApp {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            /* Custom scrollbar for desktop */
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: var(--royal-dark); /* Royal theme scrollbar track */
            }
            ::-webkit-scrollbar-thumb {
                background: var(--royal-accent); /* Royal theme scrollbar thumb */
                border-radius: 4px;
            }
        </style>
        """, unsafe_allow_html=True)