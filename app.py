import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Mathematical Trivia Oracle",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CORE DATA INITIALIZATION ---
@st.cache_data
def load_math_facts():
    # Tailored dataset mapping strictly to 'Number' and 'Math Facts' structure
    facts = {
        "Number": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 28, 42, 100, 137],
        "Math Facts": [
            "The most fundamental building block of arithmetic. It is neither prime nor composite.",
            "The only even prime number in existence and the base of the binary system.",
            "The first odd prime number and the minimum number of sides required to form a polygon.",
            "The smallest composite number and the number of human blood types (A, B, AB, O).",
            "The only prime number that ends in the digit 5 and the number of platonic solids.",
            "The smallest perfect number—equal to the sum of its proper positive divisors (1 + 2 + 3).",
            "The lowest number that cannot be represented as the sum of three numerical squares.",
            "The first perfect cube greater than 1 (2 cubed) and the number of bits in a standard byte.",
            "The maximum single digit in base 10 and a highly symmetric square number.",
            "The foundational base of our decimal system, likely chosen due to human finger counts.",
            "The number of edges on a geometric cube and the base of the duodecimal numerical system.",
            "A majestic perfect number equal to the exact sum of its proper divisors (1 + 2 + 4 + 7 + 14).",
            "The Answer to the Ultimate Question of Life, the Universe, and Everything, according to hitchhikers.",
            "The basis for percentages, the sum of the first nine prime numbers, and a perfect square.",
            "Roughly the inverse of the Fine-Structure Constant, dictating electromagnetic interaction strength."
        ]
    }
    return pd.DataFrame(facts)

# Safely build data frame
df_facts = load_math_facts()

# --- HEADER APP BANNER ---
st.title("🔢 The Mathematical Trivia Oracle")
st.caption("Exploring properties, relationships, and elegant hidden trivia behind numerical entities.")
st.write("---")

# --- SIDEBAR CONTROL DESK ---
st.sidebar.image("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=300&q=80", caption="Numerical Matrix Engine")
st.sidebar.title("🛠️ Oracle Control Panel")
st.sidebar.markdown("Pick your target numbers to query properties from the primary database framework.")

# Dynamic query slider restricted to positive integers
selected_num = st.sidebar.slider("Select Number to Inspect", min_value=1, max_value=150, value=28, step=1)
submit_button = st.sidebar.button("🔮 Extract Trivia Fact", use_container_width=True)

# --- BASE VISUALIZATIONS (Always Visible) ---
st.subheader("📊 Primary Database Spectrum Map")
st.markdown("This bar metric maps out the current density distribution indexes matching cached numbers inside the system matrix.")

# Plotly data distribution graph
fig_bar = px.bar(
    df_facts, 
    x="Number", 
    y="Number", 
    title="Numerical Frequency Index Hierarchy", 
    labels={"Number": "Value Spectrum"}, 
    color="Number", 
    color_continuous_scale="Plasma"
)
fig_bar.update_layout(template="plotly_dark")
st.plotly_chart(fig_bar, use_container_width=True)

with st.expander("📂 Inspect Raw System Matrix Dataframe"):
    st.dataframe(df_facts, use_container_width=True, hide_index=True)

# --- ACTIONS TRIGGERED ON SUBMIT BUTTON ---
if submit_button:
    st.write("---")
    st.subheader("🎯 Fact Extraction Breakthrough")
    
    with st.spinner("Parsing matrix properties..."):
        time.sleep(0.5)
        
    # Perform strict data frame filtering query
    matched_row = df_facts[df_facts["Number"] == selected_num]
    
    if not matched_row.empty:
        # Extract string property cleanly
        fact_text = matched_row.iloc[0]["Math Facts"]
        st.balloons()
        st.success(f"### 🎉 Mathematical Profile Verified for Integer {selected_num}")
        st.markdown(f"> **{fact_text}**")
    else:
        # Dynamic fallback logic calculations for values outside the raw hardcoded framework
        st.warning(f"Number {selected_num} is not cached in the local spreadsheet array. Generating programmatic fallback insights:")
        
        is_even = "Even" if selected_num % 2 == 0 else "Odd"
        square_val = selected_num ** 2
        sqrt_val = np.sqrt(selected_num)
        
        st.info(f"**Structural Blueprint:** Number `{selected_num}` is an **{is_even}** integer. Its calculated square value resolves to **{square_val}**, and its absolute square root resolves to **{sqrt_val:.4f}**.")

    # Premium Scalability chart rendered strictly upon confirmation
    st.subheader("📐 Factor Multiplication Matrix Scaling")
    x_vals = np.arange(1, 11)
    y_vals = x_vals * selected_num
    
    df_line = pd.DataFrame({"Multiplier": x_vals, "Product Value": y_vals})
    
    fig_line = px.line(
        df_line, 
        x="Multiplier", 
        y="Product Value", 
        title=f"Linear Scalar Trajectory for Base Multiple {selected_num}"
    )
    fig_line.update_layout(template="plotly_dark")
    fig_line.update_traces(line_color="#10B981")
    st.plotly_chart(fig_line, use_container_width=True)

else:
    st.info("💡 Adjust the integer configuration on the left sidebar and click **Extract Trivia Fact** to query advanced numbers.")
