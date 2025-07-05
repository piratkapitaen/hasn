import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit.components.v1 as components
from helpers import *
from ema_lib import *
import os, time, random, psutil, datetime, pickle, time
import numpy as np
#import matplotlib.pyplot as plt
import plotly.graph_objects as go
##import pyvista as pv
##from stpyvista import stpyvista

# CSS für weniger Abstand nach oben
##st.markdown("""
##    <style>
##    .css-1d391kg {  /* Haupt-Container */
##        padding-top: 0rem;
##    }
##    .css-1d391kg > div:nth-child(1) {  /* Sidebar spezifisch */
##        padding-top: -1rem;
##    }
##    </style>
##    """, unsafe_allow_html=True)

# App title
st.set_page_config(page_title="Filter designer", layout="wide")

st.markdown("""
    <style>
    /* Entferne Standard-Padding und Abstand der Sidebar */
    [data-testid="stSidebar"] {
        padding-top: 0rem;
        margin-top: 0rem !important;
        padding-bottom: 0rem;
    }
    .main {
        padding-top: 0rem !important;
    }
        header {
            visibility: hidden;
        }    
        /* Sidebar-Inhalt ganz oben platzieren */
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0rem;
        }
    .copyright {
        position: fixed;
        bottom: 118px;
        right: 55px;
        font-size: 14px;
        color: black;
        z-index: 100;
    }
    div[data-baseweb="select"] input {
        pointer-events: none;
    }
    .stSelectbox, .stSlider, .stButton {
        margin-bottom: 3px;
    }
    .stSidebar .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }    
    </style>
    <div class="copyright">
        &copy; v1.2   by NeuroCode, 2025
    </div>    
    """, unsafe_allow_html=True)

if 'text' not in st.session_state:
    st.session_state.text = ""

# Plot
fig = go.Figure()
#st.plotly_chart(fig)

st.session_state['fig'] = fig  # Diagramm merken

    
def generate_filter():
##    i_bits =   # unused. Use Amplitude for max input signal
    accubits = int(accu_bits)
    PADDING = int(ov)
##    if int(ov)  == 0:
##        PADDING = 1
##    elif int(ov) == 1:
##        PADDING = 2
##    elif int(ov) == 2:
##        PADDING = 3
##    elif int(ov) == 3:
##        PADDING = 4
##    else:
##        PADDING = 1

    # select one out of different source signals
    if sig == 'test':
        t = np.linspace(0, 64+64, int((64+64)/2))
        c = amp * np.sin(2*np.pi * t / 128) + 0
        z = np.zeros((16,))
        m = amp * np.ones((16,))

        x = np.concatenate((c, z, m))
    elif sig=='sine':
        x = amp * np.sin(2*np.pi * np.linspace(0, 140, int((140)/2)) / 128) + 0
    elif sig=='impulse':
        x = np.zeros((64,))
        x[1] = int(amp)
    else:
        x = np.concatenate((np.zeros((16,)), amp *np.ones((16,)), np.zeros((16,)), amp *np.ones((16,))))
        
    x = x + amp_noise * np.random.randn(*x.shape)   # add noise to the signal
    x = np.repeat(x, repeats=PADDING + 1)           # oversampling: repeat samples N times

    # K is shiftfactor
    if alpha.find('2') >= 0:
        K = 1
    elif alpha.find('4') >= 0:
        K = 2
    elif alpha.find('8') >= 0:
        K = 3
    else:
        K = 2

##    if truncation == '0':
##        pass
##    elif truncation == '2':
##        pass

    EMA_no_round = EMA_shift_no_round(K)            # calculate filter
#    EMA_round = EMA_round(K)
    EMA_hw = EMA_shift_no_round_HWlike(K,accubits)        # calculate filter similar to digital hardware

    y_no_round = np.array(list(map(lambda x: EMA_no_round(int(round(x))), x)))
#    y_round    = np.array(list(map(lambda x: EMA_round(int(round(x))), x)))
    y_hw    = np.array(list(map(lambda x: EMA_hw(int(round(x))), x)))


    # bandwidth calculation with rise time
    EMA_hw_step = EMA_shift_no_round_HWlike(K,accubits)
    x_step = np.concatenate((np.zeros((1,)), 63 *np.ones((64,))))
    y_step    = np.array(list(map(lambda x: EMA_hw_step(int(round(x))), x_step)))

    target = 63 * (1 - 1 / np.e)  # ≈ 39.82
    tau_index = np.argmax(y_step >= target) - 1
    tau_real_time = tau_index / (PADDING + 1)
    f_3db = 1 / (2 * np.pi * tau_real_time)
#    print('Bandwidth: ', f_3db)
                             


    # Linien hinzufügen
    fig.add_trace(go.Scatter(x=list(range(len(x))), y=x,
                             mode='lines',
                             name='input',
                             opacity=0.4))

    fig.add_trace(go.Scatter(x=list(range(len(x))), y=y_no_round,
                             mode='lines',
                             name='not rounded',
                             line=dict(color='orange', width=5)))

    fig.add_trace(go.Scatter(x=list(range(len(x))), y=y_hw,
                             mode='markers+lines',
                             name='Hardware',
                             line=dict(color='green'),
                             marker=dict(symbol='x')))

    # Achsen-Beschriftungen und Titel
    fig.update_layout(
        yaxis_title='LSBs #',
        xaxis_title='sample number, includes oversampling',
        title=f'filtered sig.: Ampl.: {amp} , oversampl.: {ov} BW: {round(f_3db, 4)}',
        title_x=0.1,  # Titel zentrieren
        legend=dict(x=0, y=1),
        margin=dict(l=40, r=40, t=40, b=40),
        template='plotly_white',
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    # Gitter anzeigen (ist standardmäßig aktiv bei 'plotly_white', sonst explizit aktivieren)
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    if 'fig' in st.session_state:
        st.plotly_chart(st.session_state['fig'])

# Sidebar
with st.sidebar:
#    st.title("EEPROM")    
    animated_svg = """
<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
 width="337.000000pt" height="294.000000pt" viewBox="0 0 337.000000 294.000000"
 preserveAspectRatio="xMidYMid meet">
<svg version="1.0" xmlns="http://www.w3.org/2000/svg"
 width="337.000000pt" height="294.000000pt" viewBox="0 0 337.000000 294.000000"
 preserveAspectRatio="xMidYMid meet">
  <style>
    .pulse {
      transform: translate(0px, 73px) scale(0.025, -0.025);
      animation: pulse 2.2s infinite ease-in-out;
      transform-origin: center;
      fill: #1420bb;
    }

    @keyframes pulse {
      0%   { transform: translate(-162px, -107px) scale(0.011, -0.011); }
      50%  { transform: translate(-166px, -105px) scale(0.015, -0.015); }
      100% { transform: translate(-162px, -107px) scale(0.011, -0.011); }
    }
  </style>
<g class="pulse" fill="#1420bb" stroke="none">
<path d="M1350 2635 l305 -305 -303 -303 c-166 -166 -302 -305 -302 -310 0 -4
275 -7 610 -7 336 0 610 1 610 3 0 1 -138 141 -307 310 l-308 307 305 305 306
305 -611 0 -610 0 305 -305z"/>
<path d="M2280 2333 l0 -611 248 -143 c136 -78 265 -155 287 -169 64 -43 516
-302 519 -299 2 2 -219 389 -491 859 -271 470 -509 882 -528 915 l-34 60 -1
-612z"/>
<path d="M521 2038 c-282 -489 -516 -899 -518 -909 -5 -18 196 92 452 247 39
23 186 109 327 191 l257 148 1 608 c0 334 -1 607 -2 607 -2 -1 -234 -402 -517
-892z"/>
<path d="M2263 1696 c-10 -12 -296 -508 -516 -896 -42 -74 -83 -142 -89 -150
-12 -15 -152 -97 -791 -466 l-259 -149 525 -3 c289 -1 764 -1 1056 0 l530 3
-207 120 c-114 66 -225 129 -248 140 -68 34 -594 340 -594 346 0 3 134 41 298
84 163 43 351 93 417 110 66 18 121 32 121 31 1 0 50 -180 109 -400 58 -219
109 -406 113 -416 5 -13 72 95 252 407 135 234 255 446 268 471 13 25 39 72
58 105 19 33 34 61 32 62 -5 5 -683 -177 -688 -184 -8 -10 -132 -43 -138 -36
-5 5 -170 610 -209 768 -9 37 -19 67 -22 67 -3 -1 -11 -7 -18 -14z"/>
<path d="M1031 1653 c-8 -27 -15 -52 -17 -58 -2 -5 -5 -19 -7 -30 -3 -11 -11
-40 -18 -65 -7 -25 -14 -49 -15 -55 -2 -5 -5 -19 -8 -30 -77 -274 -144 -541
-138 -546 10 -9 802 -221 813 -217 5 2 -18 50 -52 108 -34 58 -66 117 -73 131
-19 43 -461 809 -466 809 -3 0 -12 -21 -19 -47z"/>
<path d="M0 1078 c0 -7 10 -29 22 -48 11 -19 35 -62 52 -95 41 -79 519 -906
522 -902 1 1 50 182 108 402 59 220 109 407 112 416 3 12 -11 20 -63 34 -38
10 -70 21 -73 25 -5 6 -655 181 -672 180 -5 0 -8 -6 -8 -12z"/>
</g>
</svg>
    """
    with st.sidebar:
        st.components.v1.html(animated_svg, height=86, scrolling=False)
    st.markdown("""
    <style>
    @keyframes ticker {
      0%   { transform: translateX(75%); }
      100% { transform: translateX(-99%); }
    }

    .ticker-container {
      overflow: hidden;
      white-space: nowrap;
      width: 100%;
      background: #95D2FB;
      padding: 0.5rem 0;
    }

    .ticker-text {
      display: inline-block;
      animation: ticker 20s linear infinite;
      font-size: 1.2rem;
      color: #111111;
    }
    </style>

    <div class="ticker-container">
      <div class="ticker-text">
        IIR Filter designer: select your inputs below and click Generate.
      </div>
    </div>
    """, unsafe_allow_html=True)


        
    st.markdown('''<br>''', unsafe_allow_html=True)


st.sidebar.button('Generate', on_click=generate_filter)

#i_bits = st.sidebar.selectbox("input_bits (signed):", ["8","9","10","11","12","13","14","15","16"])
accu_bits = st.sidebar.selectbox("Accu width (signed):", ["9","10","11","12","13","14","15","16"])
alpha = st.sidebar.selectbox("alpha:", ["1/2","1/4","1/8"])
ov = st.sidebar.selectbox("oversampling:", ["0", "1", "2", "3","4","6"])
sig = st.sidebar.selectbox("signal:", ["test", "sine", "impulse", "rect"])

##exit_app = st.sidebar.button("Exit App")
##if exit_app:
##    time.sleep(.3); pid = os.getpid(); p = psutil.Process(pid);  p.terminate();

amp = st.sidebar.slider('Amplitude', min_value=62, max_value=1023, value=110, step=1)
amp_noise = st.sidebar.slider('Noise Amplitude', min_value=0, max_value=32, value=3, step=1)
#adj = st.sidebar.slider('temp adjust', min_value=-7, max_value=8, value=0, step=1)
##mode = st.sidebar.radio(
##    "mode:",
##    ["EMA", "SMA"])
#truncation = st.sidebar.selectbox("truncate:", ["0", "2", "3", "4"])


st.image('static/hacker2.png', width=64)
txt = '<div class="chat-row">'
#    div += '<img class="chat-icon" src="./app/static/ai_icon1.png" width=40 height=40>'
txt += '<div class="chat-bubble ai-bubble">'+'Hello, please make your desired inputs and generate.\n'+' </div>  </div>'
  
#st.markdown(txt, unsafe_allow_html=True)
add_vertical_space(1)
st.text_area('Hello, please make your desired inputs and generate.  Generated filter:', value=st.session_state.text, height=320)



