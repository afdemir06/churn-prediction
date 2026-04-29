import streamlit as st
import requests
import os
import pandas as pd
import json

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #0a0e1a;
    color: #c9d1e0;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3rem 4rem 3rem;
    max-width: 1100px;
}

/* ── Header ── */
.page-header {
    border-bottom: 1px solid #1e2a40;
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
}
.page-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    margin: 0 0 0.25rem 0;
}
.page-header p {
    font-size: 0.85rem;
    color: #4a5a78;
    margin: 0;
    font-family: 'Space Mono', monospace;
}
.accent { color: #00d4aa; }

/* ── Mode selector (radio) ── */
div[role="radiogroup"] {
    display: flex;
    gap: 0.75rem;
    background: transparent !important;
}
div[role="radiogroup"] label {
    flex: 1;
    border: 1px solid #1e2a40;
    border-radius: 8px;
    padding: 0.75rem 1.25rem !important;
    cursor: pointer;
    transition: all 0.2s;
    background: #0e1525 !important;
    color: #4a5a78 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
div[role="radiogroup"] label:has(input:checked) {
    border-color: #00d4aa !important;
    background: #001f1a !important;
    color: #00d4aa !important;
}
div[role="radiogroup"] label:hover {
    border-color: #2a3a55 !important;
    color: #c9d1e0 !important;
}
div[role="radiogroup"] p { margin: 0 !important; }

/* ── Section label ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #4a5a78;
    margin-bottom: 0.6rem;
}

/* ── Cards ── */
.card {
    background: #0e1525;
    border: 1px solid #1e2a40;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1.5px dashed #1e2a40;
    border-radius: 10px;
    background: #080c17;
    padding: 0.5rem;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #00d4aa55;
}
[data-testid="stFileUploader"] label {
    color: #4a5a78 !important;
    font-size: 0.85rem !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #0e1525 !important;
    border: 1px solid #1e2a40 !important;
    border-radius: 8px !important;
    color: #c9d1e0 !important;
    font-size: 0.875rem !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #00d4aa !important;
    box-shadow: 0 0 0 2px #00d4aa22 !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: #00d4aa !important;
    color: #0a0e1a !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: #00f0c0 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px #00d4aa33 !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Alerts ── */
.stSuccess {
    background: #001f1a !important;
    border-left: 3px solid #00d4aa !important;
    border-radius: 0 8px 8px 0 !important;
    color: #00d4aa !important;
}
.stInfo {
    background: #001020 !important;
    border-left: 3px solid #0088ff !important;
    border-radius: 0 8px 8px 0 !important;
    color: #4499ff !important;
}
.stError {
    background: #1a0808 !important;
    border-left: 3px solid #ff4444 !important;
    border-radius: 0 8px 8px 0 !important;
}
[data-testid="stNotification"] {
    background: #001f1a !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1e2a40 !important;
    border-radius: 10px !important;
    overflow: hidden;
}
[data-testid="stDataFrame"] table {
    background: #0a0e1a !important;
}

/* ── Divider ── */
hr {
    border-color: #1e2a40 !important;
    margin: 1.5rem 0 !important;
}

/* ── Model info tag ── */
.model-tag {
    display: inline-block;
    background: #001f1a;
    border: 1px solid #00d4aa33;
    color: #00d4aa;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    padding: 0.25rem 0.65rem;
    border-radius: 4px;
    margin-top: 0.3rem;
}

/* ── Spinner ── */
[data-testid="stSpinner"] {
    color: #00d4aa !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="page-header">
    <h1>⚡ Churn <span class="accent">Prediction</span></h1>
    <p>// ML-powered customer retention analysis</p>
</div>
""", unsafe_allow_html=True)

os.makedirs("data/raw_data", exist_ok=True)
os.makedirs("models", exist_ok=True)
model_exists = len([f for f in os.listdir("models") if f.endswith(".joblib")])>0

st.markdown('<p class="section-label">Mode</p>', unsafe_allow_html=True)
mode = st.radio(
    "Select mode:",
    ["Train Model", "Predict with Existing Model"] if model_exists else ["Train Model"],
    label_visibility="collapsed"
)

st.markdown("<hr>", unsafe_allow_html=True)

if mode == "Train Model":

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown('<p class="section-label">Training Data</p>', unsafe_allow_html=True)
        raw_train_data = st.file_uploader(
            "Upload your train data",
            type=["csv", "xlsx"],
            label_visibility="collapsed"
        )

    if raw_train_data is not None:
        if raw_train_data.name.endswith(".csv"):
            train_df = pd.read_csv(raw_train_data)
        else:
            train_df = pd.read_excel(raw_train_data)

        with col_side:
            st.markdown('<p class="section-label">File Info</p>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="margin-top:0">
                <div style="color:#4a5a78;font-size:0.75rem;margin-bottom:0.3rem">FILENAME</div>
                <div style="color:#c9d1e0;font-size:0.85rem;font-weight:500">{raw_train_data.name}</div>
                <div style="color:#4a5a78;font-size:0.75rem;margin-top:0.75rem;margin-bottom:0.3rem">DIMENSIONS</div>
                <div style="color:#c9d1e0;font-size:0.85rem">{train_df.shape[0]:,} rows &nbsp;×&nbsp; {train_df.shape[1]} cols</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<p class="section-label" style="margin-top:1rem">Target Column</p>', unsafe_allow_html=True)
        col_sel, col_btn = st.columns([2, 1])

        with col_sel:
            target_column = st.selectbox(
                "Select target column",
                options=train_df.columns,
                label_visibility="collapsed"
            )

        with col_btn:
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            train_btn = st.button("Train & Save Model")

        if train_btn:
            RAW_DATA_PATH = f"data/raw_data/train_data.{raw_train_data.name.split('.')[-1]}"
            with open(RAW_DATA_PATH, "wb") as f:
                f.write(raw_train_data.getbuffer())

            with st.spinner("Training model..."):
                response = requests.post(
                    url="http://api:8000/train-model",
                    json={"raw_train_data_path": RAW_DATA_PATH, "target_column": target_column}
                )

            if response.status_code == 200:
                st.success("Model started to get trained")
                if response.json()["status"] == "success":
                    version = response.json().get("version", "")
                    st.info(f"Model has been trained — saved as {version}")
                    st.rerun()
            else:
                st.error(f"Error: {response.text}")

elif mode == "Predict with Existing Model":

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<p class="section-label">Select Model</p>', unsafe_allow_html=True)
        selected_model = st.selectbox(
            "Select model:",
            [f for f in os.listdir("models") if f.endswith(".joblib")],
            label_visibility="collapsed"
        )
        if selected_model:
            st.markdown(f'<span class="model-tag">📦 {selected_model}</span>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<p class="section-label">Prediction Data</p>', unsafe_allow_html=True)
        data_for_prediction = st.file_uploader(
            "Upload data for prediction",
            type=["csv", "xlsx"],
            label_visibility="collapsed"
        )

    if data_for_prediction is not None:
        meta_path = os.path.join("models", selected_model.replace(".joblib", "_metadata.json"))
        with open(meta_path, "r") as f:
            metadata = json.load(f)
            expected_columns = metadata["features"]

        prediction_df = pd.read_csv(data_for_prediction) if data_for_prediction.name.endswith(".csv") else pd.read_excel(data_for_prediction)
        prediction_df = prediction_df[expected_columns]

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        col_info, col_btn = st.columns([3, 1])
        with col_info:
            st.markdown(f"""
            <div class="card" style="padding:0.9rem 1.25rem">
                <span style="color:#4a5a78;font-size:0.75rem">READY TO PREDICT &nbsp;·&nbsp; </span>
                <span style="color:#c9d1e0;font-size:0.8rem">{prediction_df.shape[0]:,} customers &nbsp;·&nbsp; {len(expected_columns)} features</span>
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            predict_btn = st.button("Run Prediction")

        if predict_btn:
            RAW_PRED_PATH = f"data/raw_data/prediction_data.{data_for_prediction.name.split('.')[-1]}"
            with open(RAW_PRED_PATH, "wb") as f:
                f.write(data_for_prediction.getbuffer())

            with st.spinner("Running inference..."):
                response = requests.post(
                    url="http://api:8000/predict",
                    json={"model_name": selected_model, "raw_prediction_data_path": RAW_PRED_PATH}
                )

            if response.status_code == 200:
                prediction_df["Churn_Probability"] = response.json()["prediction"]

                high_risk = (prediction_df["Churn_Probability"] >= 0.7).sum()
                avg_prob = prediction_df["Churn_Probability"].mean()

                m1, m2, m3 = st.columns(3)
                m1.metric("Total Customers", f"{len(prediction_df):,}")
                m2.metric("High Risk (≥70%)", f"{high_risk:,}")
                m3.metric("Avg Churn Probability", f"{avg_prob:.1%}")

                st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
                st.dataframe(
                    prediction_df,
                    column_config={
                        "Churn_Probability": st.column_config.ProgressColumn(
                            format="%.2f",
                            min_value=0,
                            max_value=1
                        )
                    },
                    use_container_width=True
                )