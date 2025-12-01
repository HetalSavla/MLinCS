import streamlit as st
import pandas as pd
import joblib

model = joblib.load("stacking_model.pkl")

# ------------------- Modern UI Styles -------------------
st.markdown("""
    <style>
        .stApp {
          background: linear-gradient(#7abfad, #eef2f3, #8e9eab);
        }
        .input-card {
            background: rgba(181, 235, 204,0.6);
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            backdrop-filter: blur(8px);
        }
        .title {
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            color: #222;
            margin-bottom: 15px;
        }
        .prediction-box {
            background: #ffffffdd;
            padding: 22px;
            border-radius: 16px;
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            border-left: 7px solid #6a11cb;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='title'>Student Performance Prediction</div>", unsafe_allow_html=True)

# ------------------- Input Section -------------------

col1, col2, col3 = st.columns(3)

# ---------- EASY ----------
with col1:
    st.subheader("Easy Level")
    total_easy_exercise = st.number_input("Total easy exercise", min_value=0, step=1, key="easy_total")
    completed_easy_exercise = st.number_input("Completed easy exercise", min_value=0, step=1, key="easy_completed")
    easy_exercise_completion_time = st.number_input("Completion time (Easy)", min_value=0, step=1, key="easy_ctime")
    easy_exercise_attempt = st.number_input("Attempts (Easy)", min_value=0, step=1, key="easy_attempt")
    easy_exercise_syntax_error = st.number_input("Syntax errors (Easy)", min_value=0, step=1, key="easy_error")

# ---------- MEDIUM ----------
with col2:
    st.subheader("Medium Level")
    total_medium_exercise = st.number_input("Total medium exercise", min_value=0, step=1, key="med_total")
    completed_medium_exercise = st.number_input("Completed medium exercise", min_value=0, step=1, key="med_completed")
    medium_exercise_completion_time = st.number_input("Completion time (Medium)", min_value=0, step=1, key="med_ctime")
    medium_exercise_attempt = st.number_input("Attempts (Medium)", min_value=0, step=1, key="med_attempt")
    medium_exercise_syntax_error = st.number_input("Syntax errors (Medium)", min_value=0, step=1, key="med_error")

# ---------- HARD ----------
with col3:
    st.subheader("Hard Level")
    total_hard_exercise = st.number_input("Total hard exercise", min_value=0, step=1, key="hard_total")
    completed_hard_exercise = st.number_input("Completed hard exercise", min_value=0, step=1, key="hard_completed")
    hard_exercise_completion_time = st.number_input("Completion time (Hard)", min_value=0, step=1, key="hard_ctime")
    hard_exercise_attempt = st.number_input("Attempts (Hard)", min_value=0, step=1, key="hard_attempt")
    hard_exercise_syntax_error = st.number_input("Syntax errors (Hard)", min_value=0, step=1, key="hard_error")

# ---------- Time Span ----------
st.subheader("Time Span")
time_span_label = st.selectbox("Select Time Span", ["Early", "Mid", "End"], key="ts_label")
time_span_mapping = {"Early": 1, "Mid": 2, "End": 3}
which_time_span_encoded = time_span_mapping[time_span_label]

st.markdown("</div>", unsafe_allow_html=True)

# ------------------- Predict Button -------------------
predict_btn = st.button("🔮 Predict Performance", use_container_width=True)

# ------------------- Prediction Logic -------------------
if predict_btn:
    x = {
        "total_easy_exercise": total_easy_exercise,
        "completed_easy_exercise": completed_easy_exercise,
        "easy_exercise_completion_time": easy_exercise_completion_time,
        "easy_exercise_attempt": easy_exercise_attempt,
        "easy_exercise_syntax_error": easy_exercise_syntax_error,
        "total_medium_exercise": total_medium_exercise,
        "completed_medium_exercise": completed_medium_exercise,
        "medium_exercise_completion_time": medium_exercise_completion_time,
        "medium_exercise_attempt": medium_exercise_attempt,
        "medium_exercise_syntax_error": medium_exercise_syntax_error,
        "total_hard_exercise": total_hard_exercise,
        "completed_hard_exercise": completed_hard_exercise,
        "hard_exercise_completion_time": hard_exercise_completion_time,
        "hard_exercise_attempt": hard_exercise_attempt,
        "hard_exercise_syntax_error": hard_exercise_syntax_error,
        "easy_completion_ratio": completed_easy_exercise / total_easy_exercise if total_easy_exercise else 0,
        "medium_completion_ratio": completed_medium_exercise / total_medium_exercise if total_medium_exercise else 0,
        "hard_completion_ratio": completed_hard_exercise / total_hard_exercise if total_hard_exercise else 0,
        "easy_effort_efficiency": easy_exercise_completion_time / completed_easy_exercise + 1 if completed_easy_exercise else 1,
        "medium_effort_efficiency": medium_exercise_completion_time / completed_medium_exercise + 1 if completed_medium_exercise else 1,
        "hard_effort_efficiency": hard_exercise_completion_time / completed_hard_exercise + 1 if completed_hard_exercise else 1,
        "easy_error_rate": easy_exercise_syntax_error / easy_exercise_attempt + 1 if easy_exercise_attempt else 1,
        "medium_error_rate": medium_exercise_syntax_error / medium_exercise_attempt + 1 if medium_exercise_attempt else 1,
        "hard_error_rate": hard_exercise_syntax_error / hard_exercise_attempt + 1 if hard_exercise_attempt else 1,
        "completed_weighted_score": completed_easy_exercise * 1 + completed_medium_exercise * 2 + completed_hard_exercise * 3,
        "attempts_weighted_score": easy_exercise_attempt * 1 + medium_exercise_attempt * 2 + hard_exercise_attempt * 3,
        "syntax_error_weighted_score": easy_exercise_syntax_error * 1 + medium_exercise_syntax_error * 2 + hard_exercise_syntax_error * 3,
        "which_time_span_encoded": which_time_span_encoded,
        "total_completed_all": completed_easy_exercise + completed_medium_exercise + completed_hard_exercise,
        "total_attempt_all": easy_exercise_attempt + medium_exercise_attempt + hard_exercise_attempt,
        "total_error_all": easy_exercise_syntax_error + medium_exercise_syntax_error + hard_exercise_syntax_error,
        "overall_efficiency": (completed_easy_exercise + completed_medium_exercise + completed_hard_exercise) /
                              (easy_exercise_attempt + medium_exercise_attempt + hard_exercise_attempt) + 1
                              if (easy_exercise_attempt + medium_exercise_attempt + hard_exercise_attempt) else 1,
    }

    df = pd.DataFrame([x])
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    st.markdown(f"<div class='prediction-box'>Prediction: {prediction}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='prediction-box'>Success Probability: {probability:.2f}</div>", unsafe_allow_html=True)






