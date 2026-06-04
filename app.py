import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Cosmic Numbers & Merger Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATA GENERATION (Dataset 1: BH-NS Mergers) ---
@st.cache_data
def load_waveform_data():
    # Simulated mapping mimicking William Henry Lee's Newtonian physics SPH calculations
    t = np.linspace(-0.1, 0.02, 1200)
    frequency = 60 / (0.01 - t + 1e-5)**0.25 
    amplitude = 1e-21 * (0.01 - t + 1e-5)**-0.25
    amplitude[t > 0.01] = 0  # Coalescence/disruption cutoff point
    strain = amplitude * np.sin(2 * np.pi * frequency * t)
    radius = np.maximum(12, 110 * (0.01 - t + 1e-5)**0.25)
    energy_loss = 1e52 * (radius**-5)
    
    return pd.DataFrame({
        "Time (s)": t,
        "Strain": strain,
        "Orbital Radius (km)": radius,
        "Frequency (Hz)": np.clip(frequency, 0, 2500),
        "Energy Flux (ergs/s)": energy_loss
    })

# --- DATA GENERATION (Dataset 2: Math Facts) ---
@st.cache_data
def load_math_facts():
    # Structured to explicitly map to column fields: 'number' and 'text'
    facts = {
        "number": [1, 2, 3, 7, 12, 28, 42, 137],
        "text": [
            "The most fundamental building block. It is neither prime nor composite.",
            "The only even prime number in existence and the base of the binary system.",
            "The first odd prime number and the number of spatial dimensions we experience.",
            "The lowest number that cannot be represented as the sum of three squares.",
            "The number of edges on a cube and the base of the duodecimal numerical system.",
            "A perfect number equal to the exact sum of its proper positive divisors.",
            "The Answer to the Ultimate Question of Life, the Universe, and Everything.",
            "Roughly the inverse of the Fine-Structure Constant, which dictates the strength of electromagnetic interaction."
        ]
    }
    return pd.DataFrame(facts)

# Load data assets safely
df_wave = load_waveform_data()
df_facts = load_math_facts()

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.image("https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=300&q=80", caption="Deep Space Simulation")
st.sidebar.title("🛠️ Universal Control Desk")
st.sidebar.markdown("Configure parameters below and hit Submit to process.")

# Module Selector Matrix
app_mode = st.sidebar.selectbox("Choose Dashboard Module", ["🌌 BH-NS Binary Mergers", "🔢 Mathematical Trivia Oracle"])

if app_mode == "🌌 BH-NS Binary Mergers":
    st.sidebar.subheader("Physics Tuning")
    bh_mass = st.sidebar.slider("Black Hole Mass (M☉)", 3.0, 30.0, 8.0, 0.5)
    ns_mass = st.sidebar.slider("Neutron Star Mass (M☉)", 1.1, 2.5, 1.4, 0.1)
    separation = st.sidebar.number_input("Initial Orbit Separation (km)", 100, 600, 250)
    gamma_index = st.sidebar.selectbox("Ideal Gas Gamma Index (Equation of State)", [1.4, 1.67, 2.0])
    
    submit_button = st.sidebar.button("💥 Simulate Coalescence", use_container_width=True)
else:
    st.sidebar.subheader("Trivia Tuning")
    selected_num = st.sidebar.slider("Pick a Number to Inspect", 1, 150, 28)
    submit_button = st.sidebar.button("🔮 Extract Trivia Fact", use_container_width=True)


# ==========================================
# MODULE 1: BLACK HOLE - NEUTRON STAR MERGER
# ==========================================
if app_mode == "🌌 BH-NS Binary Mergers":
    st.title("🌌 Black Hole - Neutron Star Binary Mergers")
    st.caption("Investigating point-mass gravitational radiation backreaction and tidal disruptions via 3D SPH simulations.")
    st.markdown("This module explores gravitational radiation waveforms modeled using Newtonian physics combined with gas equations of state.")
    
    # Render layout metrics natively to avoid HTML string token errors
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Mass Ratio (q)", f"{bh_mass / ns_mass:.2f}")
    with c2:
        m_chirp = ((bh_mass * ns_mass)**(3/5)) / ((bh_mass + ns_mass)**(1/5))
        st.metric("Chirp Mass (Mchirp)", f"{m_chirp:.2f} M☉")
    with c3:
        st.metric("EOS Gamma Index", f"{gamma_index}")
    with c4:
        st.metric("Simulation Method", "3D SPH")
        
    st.write("---")
    
    st.subheader("📊 Base Waveform Profiles")
    t1, t2 = st.tabs(["🔊 Gravitational Wave Strain h(t)", "🪐 Orbital Separation Decay"])
    
    with t1:
        fig_s = px.line(df_wave, x="Time (s)", y="Strain", title="Gravitational Radiation Strain Signature")
        fig_s.update_layout(template="plotly_dark")
        fig_s.update_traces(line_color="#3B8
