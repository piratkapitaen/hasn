import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit.components.v1 as components
from utils import *
from prompts import *
import hashlib
from langchain import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os, time, random, psutil, requests, json, datetime, re, gzip, difflib, pickle, time, sseclient
from together import Together

prompt_template = """Use the following piece of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
---
Question: {question}
Helpful Answer (preferably including C code):"""

# App title
st.set_page_config(page_title="Script AI", layout="wide")

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
        &copy; v1.0   by MVE, 2025
    </div>    
    """, unsafe_allow_html=True)

# "Scroll to bottom" Trick
scroll_script = """
    <script>
        var chatDiv = window.parent.document.querySelector('.main');
        chatDiv.scrollTo({top: chatDiv.scrollHeight, behavior: 'smooth'});
    </script>
"""

pmpt = PromptTemplate(template=template, input_variables=["question"])

# Sidebar
with st.sidebar:

##    st.markdown('''
##    <style>section[data-testid="stSidebar"] { width: 288px !important; # Set the width to your desired value }
##    </style>
##    Script AI Chatbot
##    ''', unsafe_allow_html=True)
    
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
        I'm your AI Agent: Enter your company name, API key and the usecase in the project selector.
      </div>
    </div>
    """, unsafe_allow_html=True)


        
    st.markdown('''<br>''', unsafe_allow_html=True)
#    💡 Note: No API key required!

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


# Display or clear chat messages
for message in st.session_state.messages:
    if message["role"]=="assistant":
        st.markdown(hacker_markdown(message["content"]), unsafe_allow_html=True)
    else:
        # search for QUESTION
        pos = 1
        strin = message["content"]
#        print(strin)
        pos = strin.find('## QUESTION',3000)
#        st.markdown(user_markdown(strin[pos:]), unsafe_allow_html=True)
        st.markdown(user_markdown(message["content"]), unsafe_allow_html=True)

# add clear chat and exit button in sidebar
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

exit_app = st.sidebar.button("Exit App")
if exit_app:
    time.sleep(.3); pid = os.getpid(); p = psutil.Process(pid);  p.terminate();
company = st.sidebar.text_input('Company:')
script_key = st.sidebar.text_input('Enter key:', type='password')
project = st.sidebar.selectbox("project:", ["HASN Matlab", "HASN Verilog","HASN RTL Design"])
#temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.3, step=0.05)
st.sidebar.image('static/hall_sensor.png', width=122)


def generate_bot(prompt_input):
    os.environ["TOGETHER_API_KEY"] = "b706b09225452b9518a6fbbecf505e6f426d24c614fd8a985ead385362"+ script_key
    client = Together()  # API key via api_key param or TOGETHER_API_KEY env var
    stream = client.chat.completions.create(
#        model="meta-llama/Llama-3.3-70B-Instruct-Turbo", # best model for the case :-))
#        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", # laaarge model, very costly...
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", # smallest model, large context 1M size!
        messages=[{"role": "user", "content": prompt_input}],
        stream=True,
    )
    for chunk in stream:
        try:
            content = chunk.choices[0].delta.content #or "", end="", flush=True
            if content:
                yield content
        except Exception as e:
            continue

def generate_sv(prompt_input):
    os.environ["TOGETHER_API_KEY"] = "b706b09225452b9518a6fbbecf505e6f426d24c614fd8a985ead385362"+ script_key
    client = Together()  # API key via api_key param or TOGETHER_API_KEY env var
    stream = client.chat.completions.create(
#        model="meta-llama/Llama-3.3-70B-Instruct-Turbo", # best model for the case :-))
#        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", # laaarge model, very costly...
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", # smallest model, large context 1M size!
        messages=[{"role": "user", "content": prompt_input}],
        stream=True,
    )
    prompt = sv_prompt.format(prompt_input)
    for chunk in stream:
        try:
            content = chunk.choices[0].delta.content #or "", end="", flush=True
            if content:
                yield content
        except Exception as e:
            continue
        
def generate_rtl(prompt_input):
    os.environ["TOGETHER_API_KEY"] = "b706b09225452b9518a6fbbecf505e6f426d24c614fd8a985ead385362"+ script_key
    client = Together()  # API key via api_key param or TOGETHER_API_KEY env var
    stream = client.chat.completions.create(
#        model="meta-llama/Llama-3.3-70B-Instruct-Turbo", # best model for the case :-))
#        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", # laaarge model, very costly...
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", # smallest model, large context 1M size!
        messages=[{"role": "user", "content": prompt_input}],
        stream=True,
    )
    prompt = rtl_prompt.format(prompt_input)
    for chunk in stream:
        try:
            content = chunk.choices[0].delta.content #or "", end="", flush=True
            if content:
                yield content
        except Exception as e:
            continue

def generate_together_stream(prompt_input):
    os.environ["TOGETHER_API_KEY"] = "b706b09225452b9518a6fbbecf505e6f426d24c614fd8a985ead385362"+ script_key

#    model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo" # meta-llama/Llama-3.3-70B-Instruct-Turbo
#    model = "deepseek-ai/DeepSeek-R1"
#    model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

    prompt = f"""## INSTRUCTION
I am programming in a Matlab einvironment.
Generate a script which satisfies the given Question, setting the correct register values in the register master: RegMas.Use also comments in the script as much as possible.
Do not switch to AVDD ratio mode if not explicitly desired.

## CONTEXT: REGISTER MAP
+-----------------+---+----+--+----------------------+--------+---+---+----+--+
| TestRegister        | hex|  | bits| contents       |        |   |   | R/W|  |
+-----------------+---+----+--+-----+----------------+--------+---+---+----+--+
|HARDWARE ID      | 15| 0F |  | 7:0 | IC Type+Variant|    res | 0 | 0 | RW |  | IC Type (7:5) + Variant (4:0)
| CONFIG_1        | 16| 10 |  | 7:5 | bias trim      | no_res | 0 | 0 | RW |  | 011: +23%, 010: +14%. 001:  +7%, 000:   0%, 101:  -6%, 110: -11%, 111: -16%
|                 |   |    |  |   4 | eep reserved   |    res | 0 | 0 |    |  |
|                 |   |    |  | 3:2 |TC mag sw point |    res | 0 | 0 |    |  | 00:     0 ppm/K, 01:  -400 pmm/K, 10: -1200 ppm/K, 11: -2000 ppm/K
|                 |   |    |  | 1:0 |Channel config. |    res | 0 | 0 |    |  | 00: ch1 = ch2 = X-plate, 01: ch1 = ch2 = Z-plate, 10: ch1 = ch2 = Y-plate, 11: ch1 = ch2 = DAC, HTOL-Mode: tst_dac[3:0] increment by +1 with 12us ADC conversion rate and over temperature protection disabled and AVDD set to 3.0V
| CONFIG_2        | 17| 11 |  |   7 |OUT2 inversion  | no_res | 0 | 0 | RW |  | if bit7 set, OUT2 inverted
|                 |   |    |  |   6 |OUT1 inversion  |    res | 0 | 0 |    |  | if bit6 set, OUT1 inverted
|                 |   |    |  |   5 |output swap     |    res | 0 | 0 |    |  | if bit5 set, OUT1 and OUT2 swapped/exchanged
|                 |   |    |  | 4:3 |output function |    res | 0 | 0 |    |  | 00: OUT1 speed & OUT2 direction, 01: OUT1 speed & OUT2 speed, 10: OUT1 direction & OUT2 speed, 11:  ch2   | direction
|                 |   |    |  | 2:1 |iir bandwidth   |    res | 0 | 0 |    |  | 00: 40khz, 01: 20khz, 10: 10khz, 11:  5khz
|                 |   |    |  |   0 |EEPROM parity   |    res | 0 | 0 |    |  | parity of eeprom content, Parity check is disabled if TEST_MODE1.tst_mode = 1, but STATUS_2.parity_err shows the correct actual status
|ADC_TC_OFFSET    | 18| 12 |  | 7:4 | Ch1 TC offset  |    res | 0 | 0 | RW |  | 0111: max. positiv offset, 0000: zero offset, 1111: max. negativ offset
|                 |   |    |  | 3:0 | Ch2 TC offset  |    res | 0 | 0 |    |  | 0111: max. positiv offset, 0000: zero offset, 1111: max. negativ offset
| CONFIG_3        | 19| 13 |  | 7:4 | reserved       | no_res | 0 | 0 | RW |  | reserved
|                 |   |    |  |   3 | single plate   |    res | 0 | 0 |    |  | single plate mode, ch1 and ch2 same Hall-Plate, 0: dual hall-plate mode,  1: single hall-plate mode (ch1 = ch2)
|                 |   |    |  | 2:1 | FuSa mode      |    res | 0 | 0 |    |  | 00: disable all FuSa functinality, 01: FuSa functionality is enabled -> high-Z if FuSa Error, 10: heart-beat fast (1us) enabled -> high-Z if FuSa error, 11: heart-beat slow (1us) enabled -> high-Z if FuSa error
|                 |   |    |  |   0 |out init state  |    res | 0 | 0 |    |  | 0: OUT1 = OUT2 = Low, 1: OUT1 = OUT2 = High-Z
| BON_CH1         | 20| 14 |  | 7:0 | Bon ChannelA/1 | no_res | 0 | 0 | RW |  | Bon threshold CHANNELA/1, signed two's complenent 100uT/LSB, EEPROM margin Test: Floating Gate min Threshold
| BOFF_CH1        | 21| 15 |  | 7:0 |Boff ChannelB/1 | no_res | 0 | 0 | RW |  | Boff threshold CHANNELA/1, signed two's complenent 100uT/LSB, EEPROM margin Test: Floating Gate max Threshold
| ADC_CHA_MSB     | 28| 1C |  | 7:0 |ADCChannelA MSB |    res | 0 | 0 | RW |  | MSB number as two's complement
| ADC_CHB_MSB     | 29| 1D |  | 7:0 |ADCChannelB MSB |    res | 0 | 0 | RW |  | MSB number as two's complement
|ADC_ACCU_MSB     | 30| 1E |  | 7:0 |ADC ACCU MSB    |    res | 0 | 0 | RW |  | MSB number as two's complement
|     ADC_LSB     | 31| 1F |  |   7 |ADCChannelA LSB |    res | 0 | 0 | RW |  | ADC Channel-A LSB bit
|                 |   |    |  |   6 |ADCChannelB LSB |    res | 0 | 0 |    |  | ADC Channel-B LSB bit
|                 |   |    |  |   5 |hallbias satur. |    res | 0 | 0 |    |  | bit ==1: Hall-bias saturation, Error!
|                 |   |    |  | 4:0 |ADC ACCU 5 LSBs |    res | 0 | 0 |    |  | ADC ACCU LSB 5 bits
|ADC_IIR_CTRL     | 32| 20 |  | 7:6 |   iir mode     |    res | 0 | 0 | RW |  | IIR-filter mode: 00: application mode, 01: ATE mode, no (1x) oversampling with IIR enabled, 10: ATE mode, no (1x) oversampling with IIR disabled, pass through, 11: ATE mode, no (1x) oversampling with IIR disabled, not updated,   BON_CH1: upper limit for ATE in-/out-band compare of CH1 and CH2, BOFF_CH1: lower limit for ATE in-/out-band compare of CH1 and CH2
|                 |   |    |  | 5:3 |atb mode enable |    res | 0 | 0 |    |  | 000: application mode, 001: Ch A: EEPROM floating gate voltage 1, Ch B: EEPROM floating gate voltage 2 -> FuSA error trapping disabled for debugging, 010: channel A and B: Floating gate differential voltage, 011: channel A, B and short: Analog test bus (ATB) voltage -> ATB pull down released & ATB applied, independent of CONF1.ch_conf[1:0] , 1X0: channel A, B and short: DAC with 10mV/LSB sensitivity, 1X1: channel A, B and short: DAC with 13mV/LSB sensitivity
|                 |   |    |  |   2 | adc oneshot    |    res | 0 | 0 |    |  | ADC one shot execution, r: read always as zero, write 1: if adc_en = 0 start single ADC conversion after communication, else don't care
|                 |   |    |  |   1 | adc enable     |    res | 0 | 0 |    |  | 0: ADC in IDLE state, ChA & ChB & ACCU keep value, 1:ADC running continousliy, default
|                 |   |    |  |   0 | reserved       |    res | 0 | 0 |    |  | reserved
|    STATUS_1     | 33| 21 |  |   7 |   fusa error   |    res | 0 | 0 | RW |  | 1: FuSa Error detected!
|                 |   |    |  | 6:4 |adc fusa status |    res | 0 | 0 |    |  | FuSa states: 000: FuSa R-HALL north/south of channel A, 001: FuSa R-HALL east/west of channel B, 010: FuSa R-HALL north/south of channel A, 011: FuSa R-HALL east/west of Channel B, 100: FuSa Vbg Bandgap Reference, 101: FuSa AVDD, 110: FuSa DVDD, 111: FuSa I-Ref
|                 |   |    |  |   3 |   ate comp 2   |    res | 0 | 0 |    |  | status of ADC channel A compare:   0: ADC Channel B within channel 1 limits, 1: ADC Channel B not within channel B limits
|                 |   |    |  |   2 |   ate comp 1   |    res | 0 | 0 |    |  | status of ADC channel A compare:   0: ADC Channel A within channel 1 limits, 1: ADC Channel A not within channel A limits
|                 |   |    |  |   1 |   out2         |    res | 0 | 0 |    |  | OUT2 pin level: 0: low level, 1: high level
|                 |   |    |  |   0 |   out1         |    res | 0 | 0 |    |  | OUT1 pin level: 0: low level, 1: high level
|    STATUS_2     | 34| 22 |  |   7 | chipping error |    res | 0 | 0 | RW |  | chipping line status: 0: chipping line output low level, 1: chipping line output high level
|                 |   |    |  |   6 | temp error     |    res | 0 | 0 |    |  | 1: temperature Error detected!
|                 |   |    |  |   5 | show clk err   |    res | 0 | 0 |    |  | 1: clock below lower limit, clock too slow Error!
|                 |   |    |  |   4 | parity error   |    res | 0 | 0 |    |  | 1: parity error detected
|                 |   |    |  | 3:0 | bist_state     |    res | 0 | 0 |    |  | status of IIR Build in self test (BIST):  0000: BIST-INIT 1 state, 0110: BIST-INIT 7 state, 0111: permanent BIST-ERROR state, because of HW defect or parity_err at startup, 1000: BIST-IIR 1 state, 1111: BIST-IIR 8 state, Note: if > 0000 EEPROM copy has been done
|IIR_CH12_MSB     | 35| 23 |  |   7 | iir_ch1_msb    |    res | 0 | 0 | RW |  | IIR-Filter Channel A/1 MSB bit, test-interface write has priority
|                 |   |    |  |   6 | iir_ch2_msb    |    res | 0 | 0 |    |  | IIR-Filter Channel B/2 MSB bit, test-interface write has priority
|                 |   |    |  | 5:0 | reserved       |    res | 0 | 0 |    |  | reserved
|  IIR_CH1_LSB    | 36| 24 |  | 7:0 | IIR CH1 LSB    |    res | 0 | 0 | RW |  | IIR-Filter Channel A/1 LSBs bits, test-interface write priority, signed integer format
|  IIR_CH2_LSB    | 37| 25 |  | 7:0 | IIR CH2 LSB    |    res | 0 | 0 | RW |  | IIR-Filter Channel B/2 LSBs bits, test-interface write priority, signed integer format
|    TEST_DAC     | 38| 26 |  | 7:4 | TEST DAC VALUE |    res | 0 | 0 | RW |  | Test-DAC value (2mV/LSB), 4 bits signed int; double functionality:, xxx1: chipping line level high, xxx0: chipping line level low, 111x: enable test interface, Note: if CONF_1.ch_conf = 11 and CONF_3.single_plate = 1, increment tst_dac by +1 with each 12us ADC conversion wrapping arround from 1111->0000
|                 |   |    |  |   3 |enable chipping |    res | 0 | 0 |    |  | 1: chipping line test enabled, level(chippl_lvl) is defined by tst_dac LSB: tst_dac[0] = 0: chipping line low level, tst_dac[0] = 1: chipping line high level, chipping line output observable by STATUS_2.chippl_stat; double functionality:, 1.) EEPROM data read bus connected to EEPROM data write bus, for, EEPROM read/write refresh, 2.) Force critical path (max. speed) error
|                 |   |    |  |   2 | fast clk error |    res | 0 | 0 |    |  | 1: oscillator clock too fast for critical path, Error!
|                 |   |    |  | 1:0 | reserved       |    res | 0 | 0 |    |  | 
|  EEP_CTRL_1     | 39| 27 |  |   7 | EEPROM enable  |    res | 0 | 0 | RW |  | 0: EEPROM bias currents off, only EEPROM read is enabled, programming and FG read out is disabled (default), 1: EEPROM bias currents enabled for EEPORM prog./erase and floating, gates (FG) read out
|                 |   |    |  | 6:3 | EEPROM ADDRESS |    res | 0 | 0 |  R |  | displays last EEPROM read access: shadow register copy when active or bon_ch2/boff_ch2 for signal path or last margin read address if eep_mode = 11, 0000: eeprom address  0 selected, 1010: eeprom address 12 selected
|                 |   |    |  | 2:1 | EEPROM MODE 11 |    res | 0 | 0 |    |  | EEPROM programming/margin mode: EEPROM programming/margin mode: 00: default write programming mode, 01: do only EEPROM erase step at write access to EEPROM , 10: do only EEPROM prog step at write access to EEPROM, 11: EEPROM margin test enabled, read access to STATUS_1 reg. increments eep_fg_sel by +1, eep_fg_sel transition 7->0 increments eep_addr by +1, eeprom address wraps from 1010 to 0000 (EEPROM has 12 bytes only), Note: Active prog. or erase is shown by pulling OUT2 to Low level
|                 |   |    |  |   0 | reserved       |    res | 0 | 0 |    |  | 
|  EEP_CTRL_2     | 40| 28 |  |   7 | eep fg modif   |    res | 0 | 0 | RW |  | 0: EEPROM normal differential mode, 1: non differential data lines to floating gate cells 1 and 2
|                 |   |    |  |   6 | eep vfg enable |    res | 0 | 0 |    |  | enable floating gate (FG) voltage 1/2 on analog test bus / atb: 1/2, 0: floating gates not connected to FG analog test bus, FG analog test bus tied to ground, 1: floating gates 1 and 2 connected to the FG analog test bus -> ADC
|                 |   |    |  | 5:3 |3b bin position |    res | 0 | 0 |    |  | 3bit binary coded position/address: select bit-postion for floating gate 1/2 read-out, 000: bit position 0, 111: bit position 7
|                 |   |    |  |   2 | eeprom cb odd  |    res | 0 | 0 |    |  | 0: single address programming, 1: multi odd address programming enabled, write to any addr. out of: "1,3,5,7", MIC-ID area is excluded (addr.: 9,11)
|                 |   |    |  |   1 | eeprom cb even |    res | 0 | 0 |    |  | 0: single address programming, 1: multi even address programming enabled, write to any addr. out of: "0,2,4,6", MIC-ID area is excluded (addr.: 8,10)
|                 |   |    |  |   0 | reserved       |    res | 0 | 0 |    |  | 
|  TEST_MODE_1    | 41| 29 |  | 7:6 | out2 mode      |    res | 0 | 0 | RW |  | OUT2 output mode: 00: test interface data output, 01: digital test bus (DTB) output, 10: analog test bus (ATB) direct connected (HV switch closed), ATB pull down released, 11: analog test bus (ATB) via test buffer, externally biased, ATB pull down released
|                 |   |    |  |   5 | overvolt mode  |    res | 0 | 0 |    |  | 0: OUT1/OUT2 test interface default input/output mode when overvolt, 1: XVDD > 26V: OUT1/OUT2 test interface input/output mode, XVDD < 26V: OUT1/OUT2 in application mode
|                 |   |    |  |   4 | treset mask    |    res | 0 | 0 |    |  | enable test mode access to all registers, disable test-interface timeout:  0: test-interface timeout enabled, test-interface diabled after timeout (3ms), set tst_mode = 0 will reset all test registers and exit to application immideatly, 1: test-interface timeout disabled, full register access, parity error check is disabled if test mode is active, to modify shadow registers independent from eep_partiy
|                 |   |    |  | 3:1 | dtb select     |    res | 0 | 0 |    |  | digital test bus (DTB) output selection:  000: toggling with ADC conversion (12us), Tperiod = 24us (Fosc/432), 001: toggling with oversampling rate (1us or 2us) , Tperiod = 2us or 4us (Fosc/36 or Fosc/72) , 010: ate_cmp2, 011: ate_cmp1, 100: test interface clock, 101: test interface data, 110: slow_clk_err monitor,111: hall bias saturation (h_bias_sat_i)
|                 |   |    |  |   0 | reserved       |    res | 0 | 0 |    |  | 
| TEST_MODE_2     | 42| 2A |  | 7:6 | scan mode      |    res | 0 | 0 | RW |  | ATE scan test modes, exit only by POR: w00: normal mode (default), w01: ATE scan mode basic, no OCC, no LOES, OUT1: scan data and scan clock in,  OUT2: scan data out manchaster coded,  XVDD: SCAN_EN=1 if XVDD > XVDD over voltage,  SCAN_EN=0 if XVDD < XVDD over voltage, w10: ATE scan OCC mode with LOES enabled, w11: ATE scan mode IDDQ, OUT2: scan data out if SCAN_EN=1,  OUT2: iddq i/f out if SCAN_EN=0, r: read always 00, Note: switch first in TLM sync mode before switch to any scan mode!
|                 |   |    |  |   5 | tw or          |    res | 0 | 0 |    |  | full custom analog test register check/test: 1: at least one of the checked test bits is at high level, 0: none of the checked test bits is at high level
|                 |   |    |  | 4:3 | ti mode        |    res | 0 | 0 |    |  | test-interface mode:  00: TLM async. mode w/o  output toggling (default), 01: TLM async. mode with output toggling, 10: TLM sync.  mode w/o  output toggling, 11: STI async. mode w/o  output toggling
|                 |   |    |  |   2 | reserved       |    res | 0 | 0 |    |  | reserved
|                 |   |    |  |   1 | test reset     |    res | 0 | 0 |  W |  | execute test reset: w0: no test reset executed, w1: execute test reset with EEPROM download, wait 10us befor next , test interface communication, test reset exceptions (treset mask): TEST_MODE_1.tst_mode, TEST_MODE_2.ti_mode, R: read always 00
|                 |   |    |  |   0 | reserved       |    res | 0 | 0 |    |  | reserved
| FC_TEST_1       | 65| 41 |  |   7 | dvdd disable   |    res | 0 | 0 |  W |  | 0: DVDD regulator enabled, 1: DVDD regulator disable if FC_TEST_3.pvdd_5v_mode = 1 -> POR
|                 |   |    |  |   6 |undervolt dis.  |    res | 0 | 0 |  W |  | AVDD and DVDD under voltage disable, 1: AVDD and DVDD under voltage disabled; Note: In HTOL mode this bit is automatically set
|                 |   |    |  |   5 |avddratio enable|    res | 0 | 0 |  W |  | 1: ratio mode enabled, AVDD follows XVDD for ATE measurements, see FC_TEST_2.set_avdd for AVDD details, Note: to enable SHOVE in scan mode, FC_TEST_3.pvdd_5v_mode and avdd_ratio_en must be enabled
|                 |   |    |  |   4 |vbandgap to atb |    res | 0 | 0 |  W |  | 1: bandgap voltage connected to ATB bus
|                 |   |    |  |   3 |bandgapbias 2atb|    res | 0 | 0 |  W |  | 1: bandgap bias (3uA) connected  to analog test bus/ATB bus
|                 |   |    |  | 2:0 | reserved       |    res | 0 | 0 |  W |  |
| FC_TEST_2       | 66| 42 |  |   7 |avdd load enable|    res | 0 | 0 |  W |  | 1: AVDD and DVDD load enabled (500uA each)
|                 |   |    |  | 6:5 | vdd to atb     |        | 0 | 0 |  W |  | 00: no signal connected to analog test bus (ATB) default, 01: AVDD connected to ATB bus, 10: DVDD connected to ATB bus, 11: DVDD/4 connected to ATB bus
|                 |   |    |  | 4:3 | set avdd       |        | 0 | 0 |  W |  | 000: AVDD = 2.5V (default), 001: AVDD = 2.4V, 010: AVDD = 3.0V (automatically selected in HTOL mode), 011: AVDD = 5.1V EEPROM prog. Mode, 100: AVDD = 0.215 x Vsup (ratio mode) , 111: AVDD = 0.7 x Vsup (ratio mode)
|                 |   |    |  | 2:0 | reserved       |        | 0 | 0 |  W |  |
| FC_TEST_3       | 67| 43 |  |   7 |iddq load enable|    res | 0 | 0 |  W |  | 1: 200nA current sink enabled
|                 |   |    |  |   6 |iddq ItoF enable|    res | 0 | 0 |  W |  | 1: IDDQ I/F converter enabled, if DVDD drops below under voltage level DVDD charge pump is activated until DVDD level is reached again
|                 |   |    |  | 5:4 |PVDD to ATB     |    res | 0 | 0 |  W |  | 00: no signal connected to analog test bus (ATB) (default), 01: aux. band gap (2u bias) connected to ATB bus, 10: pvdd monitor connected to ATB bus, 11: vdiv (pre-regulator start-up voltage) connected to ATB bus
|                 |   |    |  |   3 |undervolt 2 load|    res | 0 | 0 |  W |  | 1: uv comparator output connected to AVDD and DVDD load enable, undervoltage -> Isup + 0mA, no undervoltage -> Isup + 1mA
|                 |   |    |  | 2:0 | reserved       |        | 0 | 0 |  W |  |
| FC_TEST_4       | 68| 44 |  | 7:6 |coil current    |    res | 0 | 0 |  W |  | 00: coil current off (default), 01: 10mA, 10: 30mA coil current enabled, 11: 40mA coil current enabled
|                 |   |    |  |   5 |I coil polarity |        | 0 | 0 |  W |  | 0: positive polarity, 1: negative polarity
|                 |   |    |  | 4:3 |oscillator speed|        | 0 | 0 |  W |  | 00: default, 01: oscillator slow mode enabled (Fosc - 7%), 10: oscillator fast mode enabled (Fosc + 7%)
|                 |   |    |  | 2:0 | reserved       |        | 0 | 0 |  W |  |
| FC_TEST_5       | 69| 45 |  |   7 |testbuffer range|    res | 0 | 0 |  W |  | OUT2 test buffer @OUT2 range:  0: high range: 480mV to AVDD , 1: low range:  130mV to AVDD-0.8V
|                 |   |    |  |   6 | reserved       |    res | 0 | 0 |  W |  | reserved
|                 |   |    |  |   5 | pvdd 5V mode   |    res | 0 | 0 |  W |  | 1: PVDD 5V mode for coil driver mode, SHOVE (SHOrt Voltage Elivation), IDDQ or SW-POR by dvdd_dis, Note: to enable SHOVE in scan mode, pvdd_5v_mode and, FC_TEST_1.avdd_ratio_en must be enabled
|                 |   |    |  |   4 |disable OUT1bias|    res | 0 | 0 |  W |  | 1: OUT1 bias currents disabled for test
|                 |   |    |  |   3 |I2V to ATB      |    res | 0 | 0 |  W |  | 1: I2V converter connected to analog test bus (ATB) 
|                 |   |    |  | 2:0 | reserved       |    res | 0 | 0 |  W |  |
| FC_TEST_6       | 70| 46 |  |   7 | disable adc    |    res | 0 | 0 |  W |  | disable ADC: 1: ADC disabled
|                 |   |    |  | 6:3 | select 2 atb   |        | 0 | 0 |  W |  | analog test bus (ATB) source selection:  0000: no signal connected to ATB bus (default), 0001: tst_irefhall: Hall bias reference current 8uA, 0010: tst_ihall: Hall bias current 400uA, 0011: tst_vhall: Hall plate bias voltage, 0100: tst_intoutn: ADC integ. neg. output, 0101: tst_intoutp: ADC integ. pos. output, 0110: tst_intinn: ADC integ. neg. input, 0111: tst_intinp: ADC integ. pos. input , 1000: tst_irhall: Hall resistance reg. current 10uA, 1001: tst_ibias: 2uA const. bias current 2uA, 1010: tst_itc: TC-current of bias block 5uA
|                 |   |    |  | 2:0 | reserved       |        | 0 | 0 |  W |  | reserved
| FC_TEST_7       | 71| 47 |  | 7:5 | adc test mode  |    res | 0 | 0 |  W |  | ADC test mode:  000: application mode (default), 001: tst_vcmred: 10% reduced common mode levels, 010: tst_cmpneg: ADC single bit mode of neg. comp., 011: tst_cmppos: ADC single bit mode of pos. comp., 100: tst_stopspin_north: stopspin north phase, 101: tst_stopspin_south: stopspin south phase, 110: tst_stopspin_east: stopspin east phase, 111: tst_stopspin_west: stopspin west phase
|                 |   |    |  |   4 |disable overtemp|    res | 0 | 0 |  W |  | 1: overtemperature check disabled
|                 |   |    |  |   3 |reduce overtemp |    res | 0 | 0 |  W |  | 0: 175°C threshold (default), 1: reduced 120°C over temperature threshold
|                 |   |    |  | 2:0 | reserved       |        | 0 | 0 |  W |  | reserved

## EXAMPLE
DUT.read(RegMas.EEPROM_A); % example register read
DUT.write(RegMas.FC_TEST_4.coil_pol,1,'Readback',false); % example register write with initial read
DUT.write(RegMas.FC_TEST_4,0b00000000,'writeOnce',true);  % write command w/o read back, “fire and forget”
twoscomp(DUT.read(RegMas.ADC_CHA_MSB),8) % reading of ADC MSB register, use twoscomplement formatting
CommunicationBoard.VDD_Level = 9; % set VDD supply voltage VSUP to 9V
DUT.unlock();
ID = DUT.get_ID()


## QUESTION
{prompt_input}
"""

    client = Together()  # API key via api_key param or TOGETHER_API_KEY env var
    
    stream = client.chat.completions.create(
#        model="meta-llama/Llama-3.3-70B-Instruct-Turbo", # best model for the case :-))
#        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", # laaarge model, very costly...
        model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", # smallest model, large context 1M size!
#        model="meta-llama/Llama-4-Scout-17B-16E-Instruct", # smallest model, largest context 10M size!
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    
    for chunk in stream:
        try:
            content = chunk.choices[0].delta.content #or "", end="", flush=True
            if content:
                yield content
        except Exception as e:
            continue

prompt = ''
# User-provided prompt
if prompt := st.chat_input(kwargs={ 'disable_spellcheck':'True'}):

    print('PPPROMPT 1: ', prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(user_markdown(prompt), unsafe_allow_html=True)


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
#    with st.chat_message("assistant", avatar="🤖"):
    with st.spinner("Thinking..."):
        context = ''

        # instantiating the prompt template and the GPT4All chain
##        promptt = PromptTemplate(template=context_template, input_variables=["context", "question"]).partial(context=context)
##        print('PPPROMPT 8: ', promptt)
##        promptt = promptt.format(question=prompt)[:-25]
##        print('PPPROMPT 9: ', promptt)

        avatar_placeholder = st.empty()
        placeholder = st.empty()
        txt = hashlib.sha256(('4711' + company + '0815').encode()).hexdigest()
        flag = False
        if txt[3:13] == '2b5cdcae57' and len(prompt.split()) > 6 and len(prompt) > 32:
            flag = True
            # Avatar einmal anzeigen (bleibt bestehen)
            avatar_placeholder.markdown(
                '<div style="display: flex; align-items: flex-start;">'
                '<img class="chat-icon" src="./app/static/hacker.png" width=100 height=95>'
                '<div id="response-text" style="flex: 1;">', 
                unsafe_allow_html=True
            )
            full_response = ''
#            placeholder.markdown('<div class="chat-row"><img class="chat-icon" src="./app/static/steve.png" width=80 height=95></div>')
            try:
                if prompt.startswith('##'):
                    for token in generate_together_stream(prompt[2:]):
                        full_response += token
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
                elif project[:6] == 'HASN M':
                    for token in generate_together_stream(prompt):
                        full_response += token
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
                elif project[:6] == 'HASN V':
                    for token in generate_sv(prompt):
                        full_response += token
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
                elif project[:6] == 'HASN RTL':
                    for token in generate_rtl(prompt):
                        full_response += token
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
            except Exception as e:
                st.error("❌ A problem eccured generating the response.")
#                st.exception(e)  # optional für Debug-Zwecke, entferne das im Produktivbetrieb
    
            st.markdown("</div>", unsafe_allow_html=True)

#            st.markdown(scroll_script, unsafe_allow_html=True)
            # for token in generate_together_response(promptt):
            #     full_response += token
            #     placeholder.markdown(full_response)
            # placeholder.markdown(full_response)
        else:
            st.warning("🚫 The inputs Company/key are not correct or your question needs some more details. Please try again.")
##        bottom_marker = st.empty()
##        bottom_marker.markdown("<div id='scroll-anchor'></div>"
##                               "<script>document.getElementById('scroll-anchor').scrollIntoView({behavior: 'smooth'});</script>",unsafe_allow_html=True)


    if flag:
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
    else:
        message = {"role": "assistant", "content": 'Wrong key. Please try again.'}
        st.session_state.messages.append(message)        
    time.sleep(2.0)

