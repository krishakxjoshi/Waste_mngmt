import streamlit as st
import pandas as pd
from utils import get_prediction

st.set_page_config(page_title="Waste Classifier", layout="wide")

# ----------- PAGE STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "records" not in st.session_state:
    st.session_state.records = []

# ----------- NAVBAR ----------
col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Upload Page"):
        st.session_state.page = "home"

with col2:
    if st.button("📊 Dashboard"):
        st.session_state.page = "dashboard"

st.divider()

# ----------- HOME PAGE ----------
if st.session_state.page == "home":

    st.title("Upload Waste Image")

    uploaded = st.file_uploader("Choose Image")

    if uploaded:

        st.image(uploaded, width=300)

        if st.button("Predict"):

            with st.spinner("Predicting..."):
                result = get_prediction(uploaded)

            st.success(
                f"{result['label']} ({result['confidence']:.2f})"
            )

            st.session_state.records.append({
                "image": uploaded,
                "label": result["label"],
                "confidence": result["confidence"]
            })

# ----------- DASHBOARD ----------
elif st.session_state.page == "dashboard":

    st.title("Prediction Dashboard")

    records = st.session_state.records

    if len(records) == 0:
        st.warning("No predictions yet")
        st.stop()

    cols = st.columns(4)

    for i, r in enumerate(records):
        with cols[i % 4]:
            st.image(r["image"])
            st.write(r["label"])
            st.write(round(r["confidence"], 2))

    df = pd.DataFrame(records)

    total = len(df)
    bio = len(df[df["label"] == "Biodegradable"])
    nonbio = total - bio

    bio_percent = round((bio / total) * 100, 2)
    nonbio_percent = round((nonbio / total) * 100, 2)

    st.divider()

    c1, c2 = st.columns(2)
    c1.metric("Biodegradable %", bio_percent)
    c2.metric("NonBiodegradable %", nonbio_percent)

    st.bar_chart({
        "Biodegradable": [bio],
        "NonBio": [nonbio]
    })

    st.divider()

    if st.button("🔄 Reset Dashboard"):
        st.session_state.records = []
        st.success("Dashboard Reset!")