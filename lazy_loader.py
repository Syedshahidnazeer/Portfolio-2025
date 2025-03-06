# lazy_loader.py
import streamlit as st
from typing import Callable, Dict, Any
import importlib
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LazyComponentLoader:
    """Lazy loads components to improve initial load time"""
    
    def __init__(self):
        self.loaded_components = {}
        self.loading_states = {}
    
    @st.cache_resource
    def _import_module(self, module_name: str):
        """Import a module and cache it"""
        try:
            if module_name in sys.modules:
                return sys.modules[module_name]
            logger.info(f"Importing module: {module_name}")
            return importlib.import_module(module_name)
        except ImportError as e:
            logger.error(f"Failed to import {module_name}: {e}")
            st.error(f"Failed to import {module_name}. Please check the logs for details.")
            return None
    
    def load_component(self, module_name: str, component_name: str) -> Callable:
        """
        Lazy load a component function from a module
        
        Args:
            module_name: Name of the module (e.g., 'certifications')
            component_name: Name of the function to import (e.g., 'render_certifications_section')
            
        Returns:
            The loaded component function
        """
        component_key = f"{module_name}.{component_name}"
        
        # Return if already loaded
        if component_key in self.loaded_components:
            return self.loaded_components[component_key]
        
        # Show loading indicator if not already showing
        if component_key not in self.loading_states:
            self.loading_states[component_key] = True
            with st.spinner(f"Loading {component_name}..."):
                # Import the module
                module = self._import_module(module_name)
                if module is None:
                    return lambda *args, **kwargs: st.error(f"Failed to load {component_name}")
                
                # Get the component function
                if hasattr(module, component_name):
                    component = getattr(module, component_name)
                    self.loaded_components[component_key] = component
                    # Clear loading state
                    self.loading_states.pop(component_key, None)
                    return component
                else:
                    logger.error(f"Component {component_name} not found in {module_name}")
                    st.error(f"Component {component_name} not found in {module_name}")
                    # Clear loading state
                    self.loading_states.pop(component_key, None)
                    return lambda *args, **kwargs: st.error(f"Component {component_name} not found")
        else:
            # Return placeholder while loading
            return lambda *args, **kwargs: st.info(f"Loading {component_name}...")

    def load_data(self, module_name: str, data_name: str) -> Any:
        """
        Lazy load a data object from a module
        
        Args:
            module_name: Name of the module (e.g., 'data')
            data_name: Name of the data object to load (e.g., 'sample_certifications')
            
        Returns:
            The loaded data object
        """
        return self.load_component(module_name, data_name)

# Create a singleton instance
lazy_loader = LazyComponentLoader()

def load_component(module_name: str, component_name: str) -> Callable:
    """Helper function to lazy load a component"""
    return lazy_loader.load_component(module_name, component_name)

def load_data(module_name: str, data_name: str) -> Any:
    """Helper function to lazy load data objects"""
    return lazy_loader.load_data(module_name, data_name)