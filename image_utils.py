# image_utils.py
import streamlit as st
from PIL import Image
import io
import os
import hashlib
import logging
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@st.cache_data
def load_and_optimize_image(image_path, max_width=800, quality=85, format="WEBP"):
    """
    Load and optimize an image for web display
    
    Args:
        image_path: Path to the image file
        max_width: Maximum width to resize to (preserves aspect ratio)
        quality: Compression quality (0-100)
        format: Output format (WEBP recommended for best compression)
        
    Returns:
        Optimized image bytes
    """
    try:
        # Generate a cache key based on the file and parameters
        cache_key = hashlib.md5(f"{image_path}_{max_width}_{quality}_{format}".encode()).hexdigest()
        cache_dir = ".streamlit/image_cache"
        os.makedirs(cache_dir, exist_ok=True)
        cache_path = f"{cache_dir}/{cache_key}.{format.lower()}"
        
        # Check if cached version exists
        if os.path.exists(cache_path):
            with open(cache_path, "rb") as f:
                return f.read()
        
        # Load and process the image
        img = Image.open(image_path)
        
        # Convert to RGB if needed (for formats like PNG with transparency)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Calculate new dimensions while preserving aspect ratio
        width, height = img.size
        if width > max_width:
            ratio = max_width / width
            new_width = max_width
            new_height = int(height * ratio)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Save optimized image to memory
        buffer = io.BytesIO()
        if format.upper() == "WEBP":
            img.save(buffer, "WEBP", quality=quality, method=6)
        elif format.upper() == "JPEG":
            img.save(buffer, "JPEG", quality=quality, optimize=True)
        else:
            img.save(buffer, format, quality=quality)
        
        # Get the bytes and cache them
        img_bytes = buffer.getvalue()
        with open(cache_path, "wb") as f:
            f.write(img_bytes)
        
        logger.info(f"Optimized image saved to cache: {cache_path}")
        return img_bytes
    
    except Exception as e:
        logger.error(f"Error optimizing image {image_path}: {e}")
        st.error(f"Error optimizing image: {e}")
        # Return the original image as fallback
        try:
            with open(image_path, "rb") as f:
                return f.read()
        except Exception as fallback_error:
            logger.error(f"Failed to load original image {image_path}: {fallback_error}")
            return None

def display_optimized_image(image_path, caption=None, width=None, use_container_width=False):
    """Display an optimized image in the Streamlit app"""
    img_bytes = load_and_optimize_image(image_path)
    if img_bytes:
        return st.image(
            img_bytes,
            caption=caption,
            width=width,
            use_container_width=use_container_width  # Updated parameter
        )
    else:
        st.error(f"Failed to load image: {image_path}")
        return None

def display_responsive_image(image_path, mobile_width=300, desktop_width=None, caption=None):
    """Display an image with different sizes for mobile and desktop"""
    from responsive_layout import get_device_type
    
    device = get_device_type()
    width = mobile_width if device == "mobile" else desktop_width
    use_container_width = width is None  # Use container width if no specific width is set
    
    return display_optimized_image(
        image_path, 
        caption=caption,
        width=width,
        use_container_width=use_container_width  # Updated parameter
    )

def get_image_base64(image_path: str) -> str:
    """Converts an image file to a base64 string.

    Args:
        image_path: The path to the image file.

    Returns:
        A base64 encoded string of the image.
    """
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
        return ""
    except Exception as e:
        logger.error(f"Error encoding image {image_path} to base64: {e}")
        return ""

def display_remote_image(image_url, caption=None, width=None, use_container_width=False):
    """Display a remote image in the Streamlit app"""
    try:
        import requests
        response = requests.get(image_url)
        if response.status_code == 200:
            img_bytes = response.content
            return st.image(
                img_bytes,
                caption=caption,
                width=width,
                use_container_width=use_container_width  # Updated parameter
            )
        else:
            st.error(f"Failed to load remote image: {image_url}")
            return None
    except Exception as e:
        logger.error(f"Error loading remote image {image_url}: {e}")
        st.error(f"Error loading remote image: {e}")
        return None