import streamlit as st
import joblib
import numpy as np

# ---------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="ML Student Performance Predictor",
    layout="centered",
    page_icon="🚀"
)

# ---------------------- CUSTOM CSS -------------------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3 {
    color: #FFFFFF;
    text-shadow: 0px 0px 10px #00eaff;
}

.stApp {
    background: transparent;
}

.card {
    background: rgba(255,255,255,0.12);
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}

input, select {
    border-radius: 10px !important;
}

.stButton>button {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    color: white;
    padding: 12px 25px;
    font-size: 18px;
    border-radius: 10px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #dd2476, #ff512f);
    transform: scale(1.05);
}

.pred-box {
    padding: 18px;
    border-radius: 12px;
    font-size: 22px;
    color: white;
    text-align: center;
    background: linear-gradient(135deg, #00b09b, #96c93d);
    box-shadow: 0px 0px 20px rgba(0,255,200,0.4);
}

</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER -----------------------------
st.markdown("<h1 style='text-align:center;'>🚀 Student Performance Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#cce7ff;'>AI-powered prediction system using ML model</p>", unsafe_allow_html=True)

# ---------------------- LOAD MODEL -------------------------
model = joblib.load("stacking_model.pkl")

# ---------------------- INPUT CARD -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Enter Details")

col1, col2, col3 = st.columns(3)

# ---------------------- EASY (COL 1) -----------------------
with col1:
    total_easy_exercise = st.number_input("Total Easy", min_value=0, step=1)
    completed_easy_exercise = st.number_input("Completed Easy", min_value=0, step=1)
    easy_exercise_completion_time = st.number_input("Easy Time", min_value=0, step=1)
    easy_exercise_attempt = st.number_input("Easy Attempts", min_value=0, step=1)
    easy_exercise_syntax_error = st.number_input("Easy Syntax Errors", min_value=0, step=1)

# ---------------------- MEDIUM (COL 2) ---------------------
with col2:
    total_medium_exercise = st.number_input("Total Medium", min_value=0, step=1)
    completed_medium_exercise = st.number_input("Completed Medium", min_value=0, step=1)
    medium_exercise_completion_time = st.number_input("Medium Time", min_value=0, step=1)
    medium_exercise_attempt = st.number_input("Medium Attempts", min_value=0, step=1)
    medium_exercise_syntax_error = st.number_input("Medium Syntax Errors", min_value=0, step=1)

# ---------------------- HARD (COL 3) -----------------------
with col3:
    total_hard_exercise = st.number_input("Total Hard", min_value=0, step=1)
    completed_hard_exercise = st.number_input("Completed Hard", min_value=0, step=1)
    hard_exercise_completion_time = st.number_input("Hard Time", min_value=0, step=1)
    hard_exercise_attempt = st.number_input("Hard Attempts", min_value=0, step=1)
    hard_exercise_syntax_error = st.number_input("Hard Syntax Errors", min_value=0, step=1)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------- PREDICT BUTTON ----------------------
if st.button("Predict Result"):
    features = np.array([[

        # EASY
        total_easy_exercise,
        completed_easy_exercise,
        easy_exercise_completion_time,
        easy_exercise_attempt,
        easy_exercise_syntax_error,

        # MEDIUM
        total_medium_exercise,
        completed_medium_exercise,
        medium_exercise_completion_time,
        medium_exercise_attempt,
        medium_exercise_syntax_error,

        # HARD
        total_hard_exercise,
        completed_hard_exercise,
        hard_exercise_completion_time,
        hard_exercise_attempt,
        hard_exercise_syntax_error

    ]])

    prediction = model.predict(features)[0]

    st.markdown(
        f"<div class='pred-box'>Predicted Result: <strong>{prediction}</strong></div>",
        unsafe_allow_html=True
    )
