# app_workflow.py
import streamlit as st
import pandas as pd
import joblib
import os
import io
import traceback

st.set_page_config(page_title="PhD Research — Student Performance & Workflow", layout="wide")

# -------------------------
# Utility: Safe model load
# -------------------------
def load_model_from_path(path):
    try:
        m = joblib.load(path)
        return m, None
    except Exception as e:
        return None, e

def save_uploaded_file(uploaded_file, target_path):
    with open(target_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return target_path

# -------------------------
# Attempt to load default model
# -------------------------
DEFAULT_MODEL_PATH = "stacking_model.pkl"
model = None
model_load_error = None

if os.path.exists(DEFAULT_MODEL_PATH):
    model, err = load_model_from_path(DEFAULT_MODEL_PATH)
    if err:
        model_load_error = err
else:
    model_load_error = FileNotFoundError(f"{DEFAULT_MODEL_PATH} not found")

# -------------------------
# Styling (simple)
# -------------------------
st.markdown("""
    <style>
        .stApp { background: linear-gradient(#7abfad, #eef2f3, #8e9eab); }
        .glass { background: rgba(255,255,255,0.85); padding:12px; border-radius:10px; }
        .title { font-size:28px; font-weight:700; text-align:center; }
        .muted { color: #444; font-size:14px; }
        .mono { font-family: monospace; font-size:13px; background:#f7f7f7; padding:8px; border-radius:6px; }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar: Model status & uploader
# -------------------------
st.sidebar.header("Model Status")
if model is not None:
    st.sidebar.success(f"Model loaded from `{DEFAULT_MODEL_PATH}`")
else:
    st.sidebar.error("No working model loaded")
    if model_load_error is not None:
        st.sidebar.write("Load error:")
        st.sidebar.code(str(model_load_error))

st.sidebar.markdown("---")
st.sidebar.write("Upload `stacking_model.pkl` (if default is corrupted):")
uploaded = st.sidebar.file_uploader("Upload model (.pkl, joblib)", type=["pkl", "joblib"], accept_multiple_files=False)
if uploaded:
    target = os.path.join(".", uploaded.name)
    save_uploaded_file(uploaded, target)
    new_model, err = load_model_from_path(target)
    if new_model:
        model = new_model
        st.sidebar.success(f"Uploaded model loaded: {uploaded.name}")
    else:
        st.sidebar.error(f"Uploaded file failed to load: {err}")
        st.sidebar.exception(traceback.format_exc())

st.sidebar.markdown("---")
st.sidebar.info("If you still see EOFError, re-create the .pkl using `joblib.dump(model, 'stacking_model.pkl', compress=3)` on your training machine and upload via sidebar.")

# -------------------------
# Page layout: header & nav
# -------------------------
st.markdown("<div class='title'>PhD Research — Student Performance Prediction System</div>", unsafe_allow_html=True)
st.markdown("<div class='muted' style='text-align:center'>AI-powered early warning framework — Research workflow, model training outputs, and prediction UI</div>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------
# Top-level tabs
# -------------------------
tab_main, tab_workflow, tab_models, tab_predict = st.tabs([
    "Overview",
    "📘 Research Workflow (Steps 1–5)",
    "📊 Model Results & Exports",
    "🔮 Predict Student"
])

# -------------------------
# Overview tab
# -------------------------
with tab_main:
    st.header("Research Overview")
    st.write("""
This PhD research focuses on predicting student performance in C programming courses (BCA, Saurashtra region)
using behavioral analytics from an online IDE and advanced ML models. Privacy-first: no prior academic history required.
""")
    st.info("Highlights: 5 ML models trained, privacy-friendly approach, early detection, real-time predictions.")
    st.markdown("---")
    st.subheader("Status")
    st.write("""
- System Development: Completed  
- ML Pipeline: Completed  
- Dashboard: Completed  
- Data Collection: Completed  
- Model Training: Completed (stacking ensemble)  
- Publication: Pending (target Scopus by end of 2025)
    """)

# -------------------------
# Workflow tab: Expandable sections A
# -------------------------
with tab_workflow:
    st.header("🔧 Research Workflow — Stepwise Details")
    st.markdown("Each step expands to show details and outputs produced during the research pipeline.")

    # Step 1
    with st.expander("Step 1 — Derived dataset)"):
        st.markdown("**From Primary MySQL Database** we created a derived dataset `ds1.csv` containing IDE behavioral features and the target `result` (pass/fail).")
        st.markdown("Example schema / columns included:")
        st.code("""student_id, total_easy_exercise, completed_easy_exercise, easy_exercise_completion_time, easy_exercise_attempt, easy_exercise_syntax_error, ... , which_time_span, result""", language="csv")
        st.info("`ds1.csv` used as the baseline dataset for model training in Step 2.")

    # Step 2
    with st.expander("Step 2 — Training baseline models"):
        st.markdown("**Models trained on Dataset:**")
        st.write("- LogisticRegression  - RandomForest  - GradientBoosting  - MLP  - SVM  - (XGBoost also tested)")
        st.markdown("**Model definitions** (example):")
        st.code("""
models = {
    "LogisticRegression": LogisticRegression(max_iter=2000, solver='liblinear'),
    "RandomForest": RandomForestClassifier(random_state=42),
    "GradientBoosting": GradientBoostingClassifier(random_state=42),
    "MLP": MLPClassifier(max_iter=1000, random_state=42),
    "SVM": SVC(probability=True, random_state=42)
}
        """, language="python")

        st.markdown("**Training logs & best CV results (excerpt):**")
        st.code("""
================================================================================
Tuning: LogisticRegression
Fitting 5 folds for each of 4 candidates, totalling 20 fits
Best CV F1: 0.85 Best params: {'model__C': 1}
Test accuracy, precision, recall, f1, roc: 0.78 0.81 0.85 0.83 0.86
Classification Report:
               precision    recall  f1-score   support

           0       0.73      0.68      0.70       927
           1       0.81      0.85      0.83      1512

    accuracy                           0.78      2439
...
================================================================================
        """, language="text")

        st.markdown("Repeat for RandomForest, GradientBoosting, MLP, SVM, XGBoost. See full 'Model Results' tab for consolidated table and exports.")

    # Step 3
    with st.expander("Step 3 — Feature engineering"):
        st.markdown("Feature engineering steps used to create Engineered Dataset:")
        st.code("""
# examples from code1.py / code0.py
df["easy_completion_ratio"] = df["completed_easy_exercise"] / df["total_easy_exercise"]
df["easy_effort_efficiency"] = df["easy_exercise_completion_time"] / (df["completed_easy_exercise"] + 1)
df["easy_error_rate"] = df["easy_exercise_syntax_error"] / (df["easy_exercise_attempt"] + 1)
df["completed_weighted_score"] = df["completed_easy_exercise"]*1 + df["completed_medium_exercise"]*2 + df["completed_hard_exercise"]*3
df["overall_efficiency"] = df["total_completed_all"] / (df["total_attempt_all"] + 1)
        """, language="python")
        st.success("Saved engineered dataset to `engineered_ds1.csv`")

    # Step 4.1
    with st.expander("Step 4.1 — Test on engineered dataset"):
        st.markdown("Tried models on `engineered_ds1.csv` to measure improvement from feature engineering. Outputs guided stacking decisions.")
        st.info("Outcome: further tuning improved stability; stacking chosen to combine strengths of base learners.")

    # Step 4.2
    with st.expander("Step 4.2 — Stacking model"):
        st.markdown("**Stacked models used as base learners:** RandomForest, GradientBoosting, MLP, SVM, XGBoost")
        st.markdown("**Training output (stacking model)**")
        st.code("""
Training Stacking Model...

==============================
📌 STACKING MODEL PERFORMANCE
==============================
Accuracy: 0.818
Precision: 0.849
Recall: 0.865
F1 Score: 0.857
ROC AUC: 0.907

Classification Report:
              precision    recall  f1-score   support

           0       0.76      0.74      0.75       902
           1       0.85      0.87      0.86      1536

    accuracy                           0.82      2438
...
Stacking model trained successfully!
        """, language="text")
        st.success("Stacking model metrics: F1=0.857, ROC_AUC=0.907")

    # Step 5
    with st.expander("Step 5 — Visualization & Graphs"):
        st.markdown("Graphs generated from training/validation runs: confusion matrices, ROC curves, feature importances, and metric trends.")
        st.code("""
⏳ Training model ...

==============================
📌 MODEL PERFORMANCE RESULTS
==============================
Accuracy: 0.818
Precision: 0.849
Recall: 0.865
F1 Score: 0.857
ROC AUC: 0.907
...
🎯 All Graphs Generated Successfully in Single Cell!
        """, language="text")
        st.info("Graphs were generated and saved during experimentation (not embedded here). If you provide the image files, I can show them inside the app.")

# -------------------------
# Models tab: consolidated results & export
# -------------------------
with tab_models:
    st.header("Model Performance Summary")

    # create the DataFrame from the summary provided
    summary = pd.DataFrame({
        "Model": ["LogisticRegression","RandomForest","GradientBoosting","MLP","SVM","XGBoost"],
        "Best_CV_F1": [0.85, 0.86, 0.86, 0.85, 0.86, 0.86],
        "Accuracy": [0.78, 0.80, 0.80, 0.79, 0.80, 0.80],
        "Precision": [0.81, 0.83, 0.83, 0.82, 0.83, 0.82],
        "Recall": [0.85, 0.85, 0.86, 0.84, 0.85, 0.86],
        "F1": [0.83, 0.84, 0.84, 0.83, 0.84, 0.84],
        "ROC_AUC": [0.86, 0.89, 0.89, 0.88, 0.89, 0.89],
    })

    st.dataframe(summary.style.format({
        "Best_CV_F1":"{:.2f}","Accuracy":"{:.2f}","Precision":"{:.2f}","Recall":"{:.2f}","F1":"{:.2f}","ROC_AUC":"{:.2f}"
    }), use_container_width=True)

    st.markdown("**Classification reports** (sample excerpts shown in Workflow tab).")
    st.markdown("---")

    # Provide export buttons
    csv = summary.to_csv(index=False).encode("utf-8")
    st.download_button("Download model_results.csv", data=csv, file_name="model_results.csv", mime="text/csv")
    try:
        import openpyxl
        xlsx_io = io.BytesIO()
        with pd.ExcelWriter(xlsx_io, engine="openpyxl") as writer:
            summary.to_excel(writer, index=False, sheet_name="model_results")
        st.download_button("Download model_results.xlsx", data=xlsx_io.getvalue(), file_name="model_results.xlsx")
    except Exception:
        st.info("Install openpyxl to enable XLSX export (app will continue to function without it).")

# -------------------------
# Prediction tab
# -------------------------
with tab_predict:
    st.header("🔮 Predict Student Performance (Realtime)")
    if model is None:
        st.error("No usable model loaded. Use the sidebar to upload a valid `stacking_model.pkl` or fix the existing file.")
        st.stop()

    # input UI
    st.markdown("Enter activity data (counts/times/errors). Features will be derived automatically.")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Easy Level")
        total_easy_exercise = st.number_input("Total easy exercise", min_value=0, step=1, value=0, key="p_easy_total")
        completed_easy_exercise = st.number_input("Completed easy exercise", min_value=0, step=1, value=0, key="p_easy_completed")
        easy_exercise_completion_time = st.number_input("Completion time (Easy)", min_value=0, step=1, value=0, key="p_easy_ctime")
        easy_exercise_attempt = st.number_input("Attempts (Easy)", min_value=0, step=1, value=0, key="p_easy_attempt")
        easy_exercise_syntax_error = st.number_input("Syntax errors (Easy)", min_value=0, step=1, value=0, key="p_easy_error")

    with col2:
        st.subheader("Medium Level")
        total_medium_exercise = st.number_input("Total medium exercise", min_value=0, step=1, value=0, key="p_med_total")
        completed_medium_exercise = st.number_input("Completed medium exercise", min_value=0, step=1, value=0, key="p_med_completed")
        medium_exercise_completion_time = st.number_input("Completion time (Medium)", min_value=0, step=1, value=0, key="p_med_ctime")
        medium_exercise_attempt = st.number_input("Attempts (Medium)", min_value=0, step=1, value=0, key="p_med_attempt")
        medium_exercise_syntax_error = st.number_input("Syntax errors (Medium)", min_value=0, step=1, value=0, key="p_med_error")

    with col3:
        st.subheader("Hard Level")
        total_hard_exercise = st.number_input("Total hard exercise", min_value=0, step=1, value=0, key="p_hard_total")
        completed_hard_exercise = st.number_input("Completed hard exercise", min_value=0, step=1, value=0, key="p_hard_completed")
        hard_exercise_completion_time = st.number_input("Completion time (Hard)", min_value=0, step=1, value=0, key="p_hard_ctime")
        hard_exercise_attempt = st.number_input("Attempts (Hard)", min_value=0, step=1, value=0, key="p_hard_attempt")
        hard_exercise_syntax_error = st.number_input("Syntax errors (Hard)", min_value=0, step=1, value=0, key="p_hard_error")

    time_span_label = st.selectbox("Select Time Span", ["Early", "Mid", "End"], key="p_timespan")
    time_span_map = {"Early":1,"Mid":2,"End":3}
    which_time_span_encoded = time_span_map[time_span_label]

    if st.button("🔮 Predict", use_container_width=True):
        # derive features safely (avoid zero division)
        def safe_div(a,b):
            return (a / b) if b != 0 else 0

        easy_completion_ratio = safe_div(completed_easy_exercise, total_easy_exercise)
        medium_completion_ratio = safe_div(completed_medium_exercise, total_medium_exercise)
        hard_completion_ratio = safe_div(completed_hard_exercise, total_hard_exercise)

        easy_effort_efficiency = safe_div(easy_exercise_completion_time, (completed_easy_exercise + 1))
        medium_effort_efficiency = safe_div(medium_exercise_completion_time, (completed_medium_exercise + 1))
        hard_effort_efficiency = safe_div(hard_exercise_completion_time, (completed_hard_exercise + 1))

        easy_error_rate = safe_div(easy_exercise_syntax_error, (easy_exercise_attempt + 1))
        medium_error_rate = safe_div(medium_exercise_syntax_error, (medium_exercise_attempt + 1))
        hard_error_rate = safe_div(hard_exercise_syntax_error, (hard_exercise_attempt + 1))

        completed_weighted_score = (completed_easy_exercise*1 + completed_medium_exercise*2 + completed_hard_exercise*3)
        attempts_weighted_score = (easy_exercise_attempt*1 + medium_exercise_attempt*2 + hard_exercise_attempt*3)
        syntax_error_weighted_score = (easy_exercise_syntax_error*1 + medium_exercise_syntax_error*2 + hard_exercise_syntax_error*3)
        total_completed_all = completed_easy_exercise + completed_medium_exercise + completed_hard_exercise
        total_attempt_all = easy_exercise_attempt + medium_exercise_attempt + hard_exercise_attempt
        total_error_all = easy_exercise_syntax_error + medium_exercise_syntax_error + hard_exercise_syntax_error
        overall_efficiency = safe_div(total_completed_all, (total_attempt_all + 1))

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
            "easy_completion_ratio": easy_completion_ratio,
            "medium_completion_ratio": medium_completion_ratio,
            "hard_completion_ratio": hard_completion_ratio,
            "easy_effort_efficiency": easy_effort_efficiency,
            "medium_effort_efficiency": medium_effort_efficiency,
            "hard_effort_efficiency": hard_effort_efficiency,
            "easy_error_rate": easy_error_rate,
            "medium_error_rate": medium_error_rate,
            "hard_error_rate": hard_error_rate,
            "completed_weighted_score": completed_weighted_score,
            "attempts_weighted_score": attempts_weighted_score,
            "syntax_error_weighted_score": syntax_error_weighted_score,
            "which_time_span_encoded": which_time_span_encoded,
            "total_completed_all": total_completed_all,
            "total_attempt_all": total_attempt_all,
            "total_error_all": total_error_all,
            "overall_efficiency": overall_efficiency,
        }

        df_pred = pd.DataFrame([x])
        try:
            prediction = model.predict(df_pred)[0]
            prob = None
            if hasattr(model, "predict_proba"):
                try:
                    prob = model.predict_proba(df_pred)[0][1]
                except Exception:
                    prob = None

            st.markdown(f"<div class='glass'><strong>Prediction:</strong> <span style='font-size:20px'>{prediction}</span></div>", unsafe_allow_html=True)
            if prob is not None:
                st.markdown(f"<div class='glass'><strong>Success Probability:</strong> {prob:.2f}</div>", unsafe_allow_html=True)
            else:
                st.info("Model does not expose predict_proba. Only class label shown.")
        except Exception as e:
            st.error("Failed to run prediction — model may be incompatible with current feature set.")
            st.exception(traceback.format_exc())

# -------------------------
# End of app
# -------------------------




