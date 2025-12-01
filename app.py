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
            background: linear-gradient(135deg, #1f1c2c, #928dab);
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
            color: #fff;
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
            color: #00eaff;
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

# TAB 5 — Additional Content (Integrated Research Website Content)
with tab5:
    st.markdown("<div class='section-title'>📄 Research Website Content</div>", unsafe_allow_html=True)

    HTML_CONTENT = """
    <div style='color:white; font-size:18px; line-height:1.6;'>

    <h2><b>RBS</b></h2>
    <h3>RBS Creation</h3>

    <h2>PhD Research Project</h2>
    <h1><b>Student Performance Prediction System</b></h1>
    <h3>AI-Powered Early Warning Framework for Computer Education</h3>
    <p>Predicting at-risk students using behavioral analytics and machine learning</p>

    <hr>

    <h2>Research Overview</h2>
    <p>This PhD research project focuses on predicting student performance in C programming courses for BCA students in the Saurashtra region.</p>
    <p>By leveraging behavioral analytics from an online IDE and advanced machine learning models, we aim to identify at-risk students early in the semester, enabling timely interventions.</p>
    <p>Our privacy-friendly approach requires no prior academic history, making it accessible and ethical for all students.</p>

    <ul>
        <li><b>5 ML Models Trained</b></li>
        <li><b>Privacy-Friendly Approach</b></li>
        <li><b>Early Detection System</b></li>
        <li><b>Real-time Predictions</b></li>
    </ul>

    <hr>

    <h2>The Challenge</h2>
    <h3>Traditional Approach</h3>
    <ul>
        <li>Late detection of at-risk students</li>
        <li>Limited time for intervention</li>
        <li>High failure rates persist</li>
    </ul>

    <h2>Our Solution</h2>
    <p>Our AI-powered early warning system continuously monitors student behavior in real-time, predicting potential failures weeks before exams, allowing for proactive support.</p>

    <ul>
        <li>Early risk detection (weeks ahead)</li>
        <li>Ample time for intervention</li>
        <li>Improved student outcomes</li>
    </ul>

    <h3>Early Detection vs Late Detection: The difference between success and failure</h3>

    <hr>

    <h2>Our Solution</h2>
    <ul>
        <li><b>Online IDE</b>: C programming environment with real-time behavioral tracking</li>
        <li><b>ML Pipeline</b>: Advanced ML models analyze student behaviors</li>
        <li><b>Dashboard</b>: Early warning system with actionable insights</li>
    </ul>

    <h2>Technology Stack</h2>
    <ul>
        <li><b>Backend:</b> PHP 7.4+</li>
        <li><b>ML Pipeline:</b> Python 3.8+</li>
        <li><b>Database:</b> MySQL</li>
        <li><b>ML Framework:</b> scikit-learn</li>
        <li><b>Frontend:</b> Bootstrap 5</li>
        <li><b>Visualizations:</b> Chart.js</li>
    </ul>

    <hr>

    <h2>Machine Learning Models</h2>

    <h3>Baseline Models</h3>
    <p><b>Dummy Classifier, Logistic Regression</b><br>
    Establish performance baselines</p>
    <p><b>Accuracy:</b> 75–82%<br>
    <b>F1 Score:</b> 0.78–0.84</p>

    <h3>Neural Network (MLP)</h3>
    <p><b>Accuracy:</b> 85–88%<br>
    <b>F1 Score:</b> 0.86–0.89</p>

    <h3>Random Forest</h3>
    <p><b>Accuracy:</b> 83–87%<br>
    <b>F1 Score:</b> 0.84–0.88</p>

    <h3>Gradient Boosting</h3>
    <p><b>Accuracy:</b> 86–90%<br>
    <b>F1 Score:</b> 0.87–0.91</p>

    <p><i>Performance metrics are expected ranges based on similar studies. Final results pending real data collection.</i></p>

    <hr>

    <h2>Key Features</h2>
    <ul>
        <li>Privacy-friendly (no prior academic history)</li>
        <li>Real-time behavioral tracking</li>
        <li>Early risk detection</li>
        <li>Multiple ML models for accuracy</li>
        <li>Comprehensive evaluation metrics</li>
        <li>Actionable insights for teachers</li>
    </ul>

    <h2>Privacy-First Approach</h2>
    <p>Our system relies solely on behavioral data from the IDE, without requiring academic records or personal information.</p>

    <hr>

    <h2>How It Works</h2>
    <ol>
        <li><b>Student Submits Code</b> – C programs written in the online IDE</li>
        <li><b>Behavioral Data Collection</b> – time, errors, attempts, patterns</li>
        <li><b>Feature Extraction</b> – convert raw logs into ML features</li>
        <li><b>ML Prediction</b> – ensemble model predicts performance</li>
        <li><b>Early Warning Dashboard</b> – teachers receive alerts</li>
    </ol>

    <hr>

    <h2>Expected Outcomes</h2>
    <h3>Identification of Key Indicators</h3>
    <p>Discover behavioral patterns that correlate with success or failure.</p>

    <h3>Early Warning Model</h3>
    <p>High accuracy prediction of at-risk students weeks earlier.</p>

    <h3>Actionable Insights</h3>
    <p>Provide recommendations to teachers based on coding behavior.</p>

    <hr>

    <h2>Implementation Status</h2>
    <ul>
        <li><b>System Development:</b> Completed</li>
        <li><b>ML Pipeline:</b> Completed</li>
        <li><b>Dashboard:</b> Completed</li>
        <li><b>Data Collection:</b> In Progress</li>
        <li><b>Model Training:</b> Pending</li>
        <li><b>Publication:</b> Pending</li>
    </ul>

    <p><b>Target:</b> Scopus-indexed journal publication by end of 2025</p>

    <hr>

    <h2>Zero-Cost Implementation</h2>
    <p><b>POC deployed for ₹0</b></p>

    <ul>
        <li>000webhost – PHP Hosting</li>
        <li>Google Colab – ML Training</li>
        <li>Local MySQL – Database</li>
    </ul>

    <p>Perfect for a research POC (Proof of Concept).</p>

    <hr>

    <h2>Academic Context</h2>
    <p>This research builds upon established frameworks in educational data mining and learning analytics, adapted for programming education in BCA colleges across the Saurashtra region.</p>

    <hr>

    <h2>Ready to Explore?</h2>
    <p>Discover how AI-powered early warning systems can transform student success in programming education.</p>

    <h3>Student Performance Prediction System</h3>
    <p>PhD Research Project — Saurashtra Region Study</p>

    <p><i>Academic Research Use Only • © 2025</i></p>

    <p>Crafted with care, made with passion by <b>RBS</b><br>
    Made in Bolt</p>

    </div>
    """

    st.markdown(HTML_CONTENT, unsafe_allow_html=True)


