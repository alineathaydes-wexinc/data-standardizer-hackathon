# app.py
import streamlit as st
import pandas as pd
import jellyfish

st.set_page_config(layout="wide", page_title="Data Standardization Agent")

st.title("🚀 Data Standardization Agent")
st.write("Hackathon PoC - MVP 1")

st.info("Environment is set up and ready to go!")

# --- Sanity Check for Libraries ---
with st.expander("Display Library Sanity Check"):
    st.header("Library Sanity Check")
    df = pd.DataFrame({
        'column_1': [1, 2],
        'column_2': [3, 4]
    })
    st.write("Pandas is working:")
    st.dataframe(df)

    similarity_score = jellyfish.jaro_winkler_similarity("Gogle", "Google")
    st.write(f"Jellyfish is working: The similarity score between 'Gogle' and 'Google' is **{similarity_score:.2f}**")