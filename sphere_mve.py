import streamlit as st
import pyvista as pv

from stpyvista import stpyvista
from stpyvista.utils import is_the_app_embedded, start_xvfb
import pantry.stpyvista_pantry as stpv
from pantry.webapp_fragments import (
    gallery,
    fill_up_main_window,
    fill_install_instructions,
)

start_xvfb()
st.session_state.is_app_embedded = st.session_state.get("is_app_embedded", is_the_app_embedded())

res = st.slider("Resolution", 5, 100, 20, 5)

# Set up plotter
plotter = pv.Plotter(window_size=[300, 300])

# Create element
sphere = pv.Sphere(phi_resolution=res, theta_resolution=res)
plotter.add_mesh(sphere, name="sphere", show_edges=True)
plotter.view_isometric()

# Pass the plotter (not the mesh) to stpyvista
stpyvista(plotter, key=f"sphere_{res}")
