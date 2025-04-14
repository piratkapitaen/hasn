import numpy as np

import pyvista as pv

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit.components.v1 as components
from helpers import *
import os, time, random, psutil, datetime, pickle, time
import matplotlib.pyplot as plt

from stpyvista import stpyvista

## uncomment following lines for streamlit cloud deployment
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
    .copyright {
        position: fixed;
        bottom: 55px;
        right: 70px;
        font-size: 15px;
        color: black;
        z-index: 100;
    } 
    </style>
    <div class="copyright">
        &copy; v1.5   by MVE, 2025
    </div>    
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

def hys_speed_dir(signal1, signal2):
    output = np.zeros_like(signal1)
    state = 0
    for i, (val1, val2) in enumerate(zip(signal1, signal2)):
        if i < 600:
            output[i] = 0
        elif state == 0 and val1 > .009 and val2 < 0.009:
            state = 10
        elif state == 0 and val2 > .009 and val1 > 0.009 :
            state = 10
        output[i] = state
    return output

def generate_memory():
    if mode=='speed/speed':
        y_sin_hyst = hysterese(y_sin, int(1. * float(threshold)), -1.*int(1. * float(threshold)))
        y_cos_hyst = hysterese(y_cos, int(1. * float(threshold)), -1.*int(1. * float(threshold)))
    else:
        y_sin_hyst = hysterese(y_sin, int(1. * float(threshold)), -1.*int(1. * float(threshold)))
        y_cos_hyst = hysterese(y_cos, int(1. * float(threshold)), -1.*int(1. * float(threshold)))
        y_cos_hyst = hys_speed_dir(y_sin_hyst, y_cos_hyst)


    if inv!='yes':
        y_sin_hyst = 10. - y_sin_hyst
        y_cos_hyst = 10. - y_cos_hyst
        
    memory = []
    # 12 Zeilen mit 4 Hexadezimalzahlen pro Zeile
#    print('Werte: ', int(bw), float(threshold), str(mode) ) # threshold*10 in 0.1mT
    bon = int(10 * float(threshold))
    bandwidth = int(bw)
    res = 0
    if axis=='XY':
        pass
    elif axis=='ZX':
        res = res | 1
    elif axis=='ZY':
        res = res | 2
    memory.append(res);     res = 0;

    if mode=='speed/speed':
        res = res | 8
    else:
        res = 0
    # TC = 0ppm/K
    if int(bw)==5:
        res = res | 6
    elif int(bw)==10:
        res = res | 4
    elif int(bw)==20:
        res = res | 2
    elif int(bw)==40:
        res = res | 0
    if inv=='yes':
        res = res | 192
    memory.append(res);     res = 0;
    memory.append(0);       res = 0;

    if fusi!='disabled':
        res = res | 2
    if poweron!='low':
        res = res | 1
    memory.append(res);     res = 0;
    
    memory.append(256 - bon) #  Two's complement
    memory.append(bon)
    memory.append(256 - bon) #  Two's complement
    memory.append(bon)
    if UID=='0x00000000':
        memory.append(0)
        memory.append(0)
        memory.append(0)
        memory.append(0)
    else:
        memory.append(85)
        memory.append(170)
        memory.append(85)
        memory.append(170)

    memory_masked = []

    # iterate over EEPROM #0 - #7
    for mm, bitmask in zip(memory[:-4], [239, 254, 255, 11, 255, 255, 255, 255]):
        memory_masked.append(mm & bitmask)

    # calculate parity
    parity = calc_parity(memory_masked)
    # correct parity in memory
    memory[1] = memory[1] | parity


# + '     0b'+format(byte, '08b')
    my_str = ""
    arr = '['
    for byte in memory:
        my_str += str(byte)+ '     0b'+format(byte, '08b')+ ' \n'
        arr += str(byte) + ' '
    mem = bytearray(memory)
    arr += ']\n'

    hex_string = mem.hex()
    # Verbinden der Zeilen mit Zeilenumbrüchen
    st.session_state.text = 'EEPROM bytes:   '+arr+ 'HEX String:    ' + hex_string + '\n' + 'Parity: ' + str(parity)+'\n'+my_str

    x_pos = x_plot[600]
    # Channel A and B plots
    ax1.plot(x_plot, y_sin, label='Channel A', alpha=0.4)
    ax1.plot(x_plot, y_sin_hyst, label='OUT1', color='red')
    ax1.axhline(int(1. * float(threshold)), color='green', linestyle='--', label='BON')
    ax1.axhline(-1.*int(1. * float(threshold)), color='orange', linestyle='--', label='BOFF')
    ax1.set_ylabel('Channel A')
#    ax1.set_title('Channel A')
    ax1.legend()
    ax1.grid(True)
    ax2.plot(x_plot, y_cos, label='Channel B', alpha=0.4)
    ax2.plot(x_plot, y_cos_hyst, label='OUT2', color='blue')
    ax2.axhline(int(1. * float(threshold)), color='green', linestyle='--', label='BON')
    ax2.axhline(-1.*int(1. * float(threshold)), color='orange', linestyle='--', label='BOFF')
    ax2.set_ylabel('Channel B')
    ax2.set_xlabel('x')
#    ax2.set_title('Channel B')
    ax2.legend()
    ax2.grid(True)
    ax1.axvline(x_pos, color='black', linestyle=':', linewidth=1.5, label='direction change')
    ax2.axvline(x_pos, color='black', linestyle=':', linewidth=1.5)
    ax1.legend(loc='upper right')
    ax2.legend(loc='upper right')

    if 'fig' in st.session_state:
        st.pyplot(st.session_state['fig'])

# Sidebar
with st.sidebar:
#    st.title("EEPROM")    
    st.markdown('''
    EEPROM Config generator  
    ''', unsafe_allow_html=True)
#    st.image('static/ic_icon.png', width=90)

st.sidebar.button('Generate', on_click=generate_memory)

bw = st.sidebar.radio(
    "bandwidth [kHz]:",
    ["5", "10", "20", "40"])
threshold = st.sidebar.slider('threshold', min_value=0.5, max_value=12.5, value=2.0, step=0.1)
#adj = st.sidebar.slider('temp adjust', min_value=-7, max_value=8, value=0, step=1)
mode = st.sidebar.radio(
    "mode:",
    ["speed/speed", "speed/direction"])
axis = st.sidebar.radio(
    "axis:",
    ["XY", "ZX", "ZY"])
fusi = st.sidebar.radio(
    "fusi:",
    ["enabled", "disabled"])
poweron = st.sidebar.radio(
    "power on state:",
    ["high-Z", "low"])
inv = st.sidebar.radio(
    "outputs inverted:",
    ["no", "yes"])
UID = st.sidebar.radio(
    "UID:",
    ["0x00000000", "ckeckerboard: 0x55AA55AA"])

st.image('static/evm.png', width=64)
txt = '<div class="chat-row">'
#    div += '<img class="chat-icon" src="./app/static/ai_icon1.png" width=40 height=40>'
txt += '<div class="chat-bubble ai-bubble">'+'Hello, please make your inputs and generate.\n'+' </div>  </div>'
  
#st.markdown(txt, unsafe_allow_html=True)
add_vertical_space(1)
st.text_area('Hello, please make your inputs and generate.  EEPROM contents:', value=st.session_state.text, height=370)


# Set up stpyvista 3D plotter
plotter = pv.Plotter(window_size=[300, 300])

# objects
box = pv.Box(bounds=(-4.0, 4.0, 0, 5.0, -0.5, 0.2), level=4)
box.texture_map_to_plane(use_bounds=False,inplace=True)
chip =pv.Box(bounds=(-3.7, 3.7, 0.3, 4.7, 0.0, 0.25), level=4)
chip.texture_map_to_plane(use_bounds=False,inplace=True)
ft1 = pv.Box(bounds=(-3.0, -2.5, -1.0, 0, -0.5, 0.0), level=4)
ft2 = pv.Box(bounds=(2.5, 3.0, -1.0, 0, -0.5, 0.0), level=4)
ft3 = pv.Box(bounds=(-0.25, 0.25, 5.0, 6.0, -0.5, 0.0), level=4)
cyl1 = pv.Cylinder(center=(0.0, 2.01, 3.8), direction=(0.0, 0.0, 1.0), radius=1.8, height=2.0)
cyl2 = pv.Cylinder(center=(0.0, 1.99, 3.8), direction=(0.0, 0.0, 1.0), radius=1.802, height=1.99)

#cyl1.plot(texture=tex)
tx = pv.read_texture('magnet.gif')
chip_tex = pv.read_texture('die.gif')
chip_bottom = pv.read_texture('kdt.gif')
#tx.flip_x()
#tx.flip_y()
#tx.rotate_ccw()
tx.wrap = 3
tx.repeat = False

# Create element
sphere = pv.Sphere(phi_resolution=20, theta_resolution=20)
#plotter.add_mesh(sphere, name="sphere", show_edges=True)
plotter.add_mesh(box, texture=chip_bottom)
plotter.add_mesh(chip, texture=chip_tex)
plotter.add_mesh(ft1, color='grey')
plotter.add_mesh(ft2, color='grey')
plotter.add_mesh(ft3, color='grey')
plotter.add_mesh(cyl1, texture=tx)
plotter.add_mesh(cyl2, color='blue')

plotter.view_isometric()

# Pass the plotter (not the mesh) to stpyvista
stpyvista(plotter, key="Hall")
