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
    t = np.linspace(-0.1, 0.02, 1200)
    frequency = 60 / (0.01 - t + 1e-5)**0.25 
    amplitude = 1e-21 * (0.01 - t + 1e-5)**-0.25
    amplitude[t > 0.01] = 0  
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
            "Roughly the inverse of the Fine-Structure Constant, which dictates electromagnetic interaction strength."
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
    
    # Render layout metrics natively
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
        fig_s.update_traces(line_color="#3B82F6")
        st.plotly_chart(fig_s, use_container_width=True)
        
    with t2:
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatter(x=df_wave["Time (s)"], y=df_wave["Orbital Radius (km)"], name="Radius", line=dict(color="#F59E0B")))
        fig_r.update_layout(title="Orbital Distance Contraction", template="plotly_dark", xaxis_title="Time (s)", yaxis_title="Separation (km)")
        st.plotly_chart(fig_r, use_container_width=True)

    if submit_button:
        st.write("---")
        st.subheader("🔮 Dynamically Generated Insights")
        
        with st.spinner("Processing event horizons and tidal disruptions..."):
            time.sleep(1.2)
            
        tot_mass = bh_mass + ns_mass
        horizon = 2.95 * bh_mass
        
        rc1, rc2 = st.columns(2)
        with rc1:
            st.info("### 🧬 Computed System Outputs")
            results_df = pd.DataFrame({
                "Physical Parameter": ["Total Binary Mass", "Black Hole Event Horizon Radius", "Starting Orbital Energy Status"],
                "Calculated Output": [f"{tot_mass:.2f} M☉", f"{horizon:.2f} km", "Alpha-State Balanced"]
            })
            st.table(results_df)
            
        with rc2:
            st.info("### 💡 Tidal Disruption Fate Matrix")
            if (bh_mass / ns_mass) > 6.0:
                st.warning("⚠️ High Mass Ratio: The mass ratio is highly asymmetrical. The neutron star will likely cross the event horizon whole without leaving any significant accretion disk remnant.")
            else:
                st.success("✨ Accretion Disk Formed: Tidal forces will tear the neutron star apart before it collapses into the horizon. This is expected to release a bright electromagnetic short Gamma-Ray Burst (sGRB)!")
                
        fig_f = px.area(df_wave, x="Time (s)", y="Frequency (Hz)", title="Dynamic Frequency Shift (Chirp Phenomenon Profile)", color_discrete_sequence=['#EC4899'])
        fig_f.update_layout(template="plotly_dark")
        st.plotly_chart(fig_f, use_container_width=True)
        
    else:
        st.info("💡 Adjust the metrics in the left sidebar and hit Simulate Coalescence to reveal advanced predictions.")


# ==========================================
# MODULE 2: MATHEMATICAL TRIVIA ORACLE
# ==========================================
else:
    st.title("🔢 Mathematical Trivia Oracle")
    st.caption("Exploring properties, relationships, and hidden trivia behind numerical entities.")
    st.markdown("Every number has an identity. This system parses mathematical properties to find structural relationships.")
    
    with st.expander("📂 Inspect Raw Math Facts Database Matrix"):
        st.dataframe(df_facts, use_container_width=True)
        
    st.write("---")
    
    st.subheader("📊 Numerical Frequency Spectrum Analysis")
    fig_bar = px.bar(df_facts, x="number", y="number", title="Stored Fact Identity Indexes", labels={"number":"Value Spectrum"}, color="number", color_continuous_scale="Viridis")
    fig_bar.update_layout(template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

    if submit_button:
        st.write("---")
        st.subheader("🎯 Fact Extraction Breakdown")
        
        with st.spinner("Querying matrix properties..."):
            time.sleep(0.6)
            
        matched_row = df_facts[df_facts["number"] == selected_num]
        
        if not matched_row.empty:
            fact_text = matched_row.iloc[0]["text"]
            st.balloons()
            st.success(f"### 🎉 Mathematical Profile for Number {selected_num}")
            st.markdown(f"> **{fact_text}**")
        else:
            st.warning(f"Number {selected_num} is not cached in the core CSV database. However, here is its baseline structural property:")
            is_even = "Even" if selected_num % 2 == 0 else "Odd"
            st.info(f"**Generic Property Matrix:** Number {selected_num} is an {is_even} integer, its square is {selected_num**2}, and its square root calculates to {np.sqrt(selected_num):.4f}.")
            
        st.subheader("📐 Multiplier Matrix Map")
        x_vals = np.arange(1, 11)
        y_vals = x_vals * selected_num
        
        fig_line = px.line(x=x_vals, y=y_vals, title=f"Linear Multiplier Scalability for Factor {selected_num}", labels={"x": "Multiplier Range", "y": "Product Amplitude"})
        fig_line.update_layout(template="plotly_dark")
        fig_line.update_traces(line_color="#10B981")
        st.plotly_chart(fig_line, use_container_width=True)
        
    else:
        st.info("💡 Pick an integer on the left panel and click Extract Trivia Fact to run an index look-up.")
