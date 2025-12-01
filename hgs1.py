# app_embedded.py
import streamlit as st
import pandas as pd
import joblib
import os

# -------------------
# Load Model
# -------------------
MODEL_PATH = "stacking_model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    st.error(f"Model file not found: {MODEL_PATH}")
    st.stop()

# -------------------
# Styling
# -------------------
st.set_page_config(page_title="AI-Driven Student Performance Prediction System", layout="wide")
st.markdown("""
    <style>
        .stApp {
            # background: linear-gradient(135deg, #1f1c2c, #928dab);
            font-family: 'Segoe UI';
        }
        .glass-card {
            background: rgba(255,255,255,0.18);
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
            margin-bottom: 25px;
        }
        .title {
            font-size: 48px;
            font-weight: 800;
            text-align: center;
            color: #ffffff;
            margin-bottom: 20px;
            text-shadow: 2px 2px 10px #000;
        }
        .section-title { font-size: 30px; font-weight: 700; color: #fff; margin-bottom: 10px; }
        .timeline-item {
            background: rgba(255,255,255,0.2);
            padding: 18px;
            border-left: 6px solid #00eaff;
            border-radius: 10px;
            margin-bottom: 15px;
            # color: #fff;
            font-size: 17px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .prediction-box {
            background: rgba(0,0,0,0.45);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            font-size: 22px;
            font-weight: 700;
            # color: #00eaff;
            border: 2px solid #00eaff;
            box-shadow: 0 4px 20px rgba(0, 255, 255, 0.4);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>AI-Driven Student Performance Prediction System</div>", unsafe_allow_html=True)

# -------------------
# Tabs
# -------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📌 Enter Student Activity Data",
    "📘 Research Timeline",
    "📊 Model Output Dashboard",
    "🧪 Model Summary",
    "📄 Additional Content"
])

# TAB 1 — Input Form + Prediction
with tab1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Enter Activity Details</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    # EASY
    with col1:
        st.subheader("Easy Level")
        total_easy_exercise = st.number_input("Total easy exercise", min_value=0, step=1, key="easy_total")
        completed_easy_exercise = st.number_input("Completed easy exercise", min_value=0, step=1, key="easy_completed")
        easy_exercise_completion_time = st.number_input("Completion time (Easy)", min_value=0, step=1, key="easy_ctime")
        easy_exercise_attempt = st.number_input("Attempts (Easy)", min_value=0, step=1, key="easy_attempt")
        easy_exercise_syntax_error = st.number_input("Syntax errors (Easy)", min_value=0, step=1, key="easy_error")
    # MEDIUM
    with col2:
        st.subheader("Medium Level")
        total_medium_exercise = st.number_input("Total medium exercise", min_value=0, step=1, key="med_total")
        completed_medium_exercise = st.number_input("Completed medium exercise", min_value=0, step=1, key="med_completed")
        medium_exercise_completion_time = st.number_input("Completion time (Medium)", min_value=0, step=1, key="med_ctime")
        medium_exercise_attempt = st.number_input("Attempts (Medium)", min_value=0, step=1, key="med_attempt")
        medium_exercise_syntax_error = st.number_input("Syntax errors (Medium)", min_value=0, step=1, key="med_error")
    # HARD
    with col3:
        st.subheader("Hard Level")
        total_hard_exercise = st.number_input("Total hard exercise", min_value=0, step=1, key="hard_total")
        completed_hard_exercise = st.number_input("Completed hard exercise", min_value=0, step=1, key="hard_completed")
        hard_exercise_completion_time = st.number_input("Completion time (Hard)", min_value=0, step=1, key="hard_ctime")
        hard_exercise_attempt = st.number_input("Attempts (Hard)", min_value=0, step=1, key="hard_attempt")
        hard_exercise_syntax_error = st.number_input("Syntax errors (Hard)", min_value=0, step=1, key="hard_error")
    time_span_label = st.selectbox("Select Time Span", ["Early", "Mid", "End"])
    time_span_mapping = {"Early": 1, "Mid": 2, "End": 3}
    which_time_span_encoded = time_span_mapping[time_span_label]
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔮 Predict Performance", use_container_width=True):
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
            "easy_completion_ratio": (completed_easy_exercise / total_easy_exercise) if total_easy_exercise else 0,
            "medium_completion_ratio": (completed_medium_exercise / total_medium_exercise) if total_medium_exercise else 0,
            "hard_completion_ratio": (completed_hard_exercise / total_hard_exercise) if total_hard_exercise else 0,
            "easy_effort_efficiency": easy_exercise_completion_time / (completed_easy_exercise + 1),
            "medium_effort_efficiency": medium_exercise_completion_time / (completed_medium_exercise + 1),
            "hard_effort_efficiency": hard_exercise_completion_time / (completed_hard_exercise + 1),
            "easy_error_rate": easy_exercise_syntax_error / (easy_exercise_attempt + 1),
            "medium_error_rate": medium_exercise_syntax_error / (medium_exercise_attempt + 1),
            "hard_error_rate": hard_exercise_syntax_error / (hard_exercise_attempt + 1),
            "completed_weighted_score": completed_easy_exercise*1 + completed_medium_exercise*2 + completed_hard_exercise*3,
            "attempts_weighted_score": easy_exercise_attempt*1 + medium_exercise_attempt*2 + hard_exercise_attempt*3,
            "syntax_error_weighted_score": easy_exercise_syntax_error*1 + medium_exercise_syntax_error*2 + hard_exercise_syntax_error*3,
            "which_time_span_encoded": which_time_span_encoded,
            "total_completed_all": completed_easy_exercise + completed_medium_exercise + completed_hard_exercise,
            "total_attempt_all": easy_exercise_attempt + medium_exercise_attempt + hard_exercise_attempt,
            "total_error_all": easy_exercise_syntax_error + medium_exercise_syntax_error + hard_exercise_syntax_error,
            "overall_efficiency": (completed_easy_exercise + completed_medium_exercise + completed_hard_exercise) / (easy_exercise_attempt + medium_exercise_attempt + hard_exercise_attempt + 1),
        }
        df = pd.DataFrame([x])
        try:
            prediction = model.predict(df)[0]
            prob = None
            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(df)[0][1]
            st.markdown(f"<div class='prediction-box'>Prediction: {prediction}</div>", unsafe_allow_html=True)
            if prob is not None:
                st.markdown(f"<div class='prediction-box'>Success Probability: {prob:.2f}</div>", unsafe_allow_html=True)
            else:
                st.info("Model has no predict_proba; only class prediction displayed.")
        except Exception as e:
            st.error(f"Model prediction error: {e}")

# TAB 2 — Timeline
with tab2:
    st.markdown("<div class='section-title'>📘 Research & Model Development Timeline</div>", unsafe_allow_html=True)
    timeline_items = [
        "Dataset collected from online IDE-based programming platform.",
        "Data cleaned, normalized, and feature engineered (30+ derived features).",
        "ML models trained: Random Forest, Gradient Boosting, SVM, MLP.",
        "Stacking Model developed with best cross-validation accuracy.",
        "Full ML pipeline automated with preprocessing + tuning.",
        "Final Stacking Model exported as .pkl.",
        "Streamlit Web App developed for real-time predictions.",
        "UI upgraded to advanced glassmorphism interface.",
    ]
    for step in timeline_items:
        st.markdown(f"<div class='timeline-item'>✔️ {step}</div>", unsafe_allow_html=True)

# TAB 3 — Model Output Dashboard (placeholders)
with tab3:
    st.markdown("<div class='section-title'>📊 Model Output Dashboard</div>", unsafe_allow_html=True)
    st.info("Placeholders. Add your evaluation graphs / metrics here (confusion matrix, feature importances, etc.).")

# TAB 4 — Model Summary
with tab4:
    st.markdown("<div class='section-title'>🧪 Final Trained Model Summary</div>", unsafe_allow_html=True)
    st.success(f"Model loaded from: `{MODEL_PATH}`")
    st.markdown("""
        **Model Used:** Stacking Classifier  
        **Base Models:** Random Forest, Gradient Boosting, MLP  
    """)
    st.markdown("""
        ### 🔹 Why Stacking Performed Best?
        - Handles diverse feature types  
        - Reduces variance  
        - Combines strengths of multiple ML models  
    """)
    st.markdown("""
        ### 🔹 What This Model Predicts
        - Student final performance category  
        - Probability of success (if model supports `predict_proba`)  
        - Early identification of at-risk learners  
    """)

# TAB 5 — Additional Content (embedded text / HTML / Markdown)
with tab5:
    st.markdown("<div class='section-title'>📄 Additional Content</div>", unsafe_allow_html=True)
    CONTENT_FILE = "site_content.html"  # or .md if you'd prefer
    if os.path.exists(CONTENT_FILE):
        # if HTML
        text = open(CONTENT_FILE, "r", encoding="utf-8").read()
        st.markdown(text, unsafe_allow_html=True)
    else:
        st.info(f"No content file found at `{CONTENT_FILE}` — please place your content there.")






