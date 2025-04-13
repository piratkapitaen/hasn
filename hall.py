import numpy as np

import pyvista as pv

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit.components.v1 as components
from helpers import *
import os, time, random, psutil, datetime, pickle, time
import matplotlib.pyplot as plt

from stpyvista import stpyvista
from stpyvista.utils import is_the_app_embedded, start_xvfb

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
