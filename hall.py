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

# App title
st.set_page_config(page_title="EEPROM config", layout="wide")

st.markdown("""
    <style>
    /* Entferne Standard-Padding und Abstand der Sidebar */
    [data-testid="stSidebar"] {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    .main {
        padding-top: 0rem !important;
    }
        header {
            visibility: hidden;
        }    
    /* Entferne Abstand oben von Hauptcontainer */
    .css-1d391kg {  
        padding-top: 0rem;
    }
    .css-znku1x.e16nr0p33 {
      margin-top: -75px;
    }
        /* Sidebar-Inhalt ganz oben platzieren */
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem;
        }    
    </style>
    """, unsafe_allow_html=True)

if 'text' not in st.session_state:
    st.session_state.text = ""

# Zeitachse & Signale
# Kombiniere beide: vorwärts und rückwärts
#x = np.concatenate((x_forward, x_backward))
x = np.concatenate([np.linspace(0, 3.5 * np.pi, 600), np.linspace(3.5 * np.pi, 0, 600)])
x_plot = np.linspace(0, 7 * np.pi, 1200)
x = x[:950]
x_plot = x_plot[:950]

# Erzeuge Signale
y_sin = 25. * np.sin(x)
y_cos = 25. * np.cos(x)

# Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
fig.tight_layout()
st.session_state['fig'] = fig  # Diagramm merken

def calc_parity(byte_list):
    parity = 0
    for byte in byte_list:
        while byte:
            parity ^= (byte & 1) # XOR mit LSB
            byte >>= 1
    return parity

# Hysterese-Funktion
def hysterese(signal, thresh_high, thresh_low):
    output = np.zeros_like(signal)
    state = 0
    for i, val in enumerate(signal):
        if state == 0 and val > thresh_high:
            state = 10
        elif state == 10 and val < thresh_low:
            state = 0
        output[i] = state
    return output

def hys_speed_direction(signal):
    output = np.zeros_like(signal)
    state = 0
    for i, val in enumerate(signal):
        if i < 600:
            output[i] = 0
        elif state == 0 and val > .009:
            state = 10
        output[i] = state
    return output

def sphere():
    return pv.Sphere(radius=1.0, center=(0, 0, 0))






res = st.slider("Resolution", 5, 100, 20, 5)

# Set up plotter
plotter = pv.Plotter(window_size=[300, 300])

# Create element
sphere = pv.Sphere(phi_resolution=res, theta_resolution=res)
plotter.add_mesh(sphere, name="sphere", show_edges=True)
plotter.view_isometric()

# Pass the plotter (not the mesh) to stpyvista
stpyvista(plotter, key=f"sphere_{res}")
