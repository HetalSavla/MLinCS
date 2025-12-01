# app_integration.py
import streamlit as st
import pandas as pd
import joblib
import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import io
import shutil
import traceback

# ---------------------------
# Config
# ---------------------------
REMOTE_URL = "https://ai-student-performan-b772.bolt.host"
REMOTE_ASSET_DIR = "remote_assets"
LOCAL_MODEL_PATH = "stacking_model.pkl"  # your existing model
REMOTE_MODEL_CANDIDATES = ["stacking_model.pkl", "model.pkl", "final_model.pkl", "model.joblib"]

# ensure folder
os.makedirs(REMOTE_ASSET_DIR, exist_ok=True)

# ---------------------------
# Utilities: download + scrape
# ---------------------------
def safe_get(url, timeout=8):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception as e:
        return None

def discover_and_download(remote_url, save_dir=REMOTE_ASSET_DIR):
    """
    Fetch remote_url HTML, parse links and download assets we think are models/datasets/images/css.
    Returns dict with status and list of downloaded files.
    """
    results = {"success": False, "message": "", "downloaded": []}
    r = safe_get(remote_url)
    if not r:
        results["message"] = f"Failed to fetch {remote_url} (server unreachable or blocking requests)."
        return results

    try:
        soup = BeautifulSoup(r.text, "html.parser")

        # try to embed raw html copy too
        with open(os.path.join(save_dir, "remote_index.html"), "w", encoding="utf-8") as f:
            f.write(r.text)
        results["downloaded"].append("remote_index.html")

        # find likely asset links
        tags = soup.find_all(["a", "link", "script", "img"])
        found = set()
        for t in tags:
            href = t.get("href") or t.get("src")
            if not href:
                continue
            full = urljoin(remote_url, href)
            # only same-domain assets
            if urlparse(full).netloc != urlparse(remote_url).netloc:
                # skip cross-domain (could be CDNs) - but keep images if they are full url
                pass
            # extension checks
            for ext in [".pkl", ".joblib", ".zip", ".csv", ".xlsx", ".png", ".jpg", ".jpeg", ".svg", ".css", ".js"]:
                if full.lower().endswith(ext):
                    found.add(full)
        # also check for obvious model filenames at root
        base = remote_url.rstrip("/") + "/"
        for candidate in REMOTE_MODEL_CANDIDATES + ["dataset.csv", "data.xlsx", "Dataset22-23.xlsx", "dataset.xlsx"]:
            found.add(urljoin(base, candidate))

        # download found assets
        for asset_url in sorted(found):
            try:
                rr = safe_get(asset_url)
                if not rr:
                    continue
                fname = os.path.basename(urlparse(asset_url).path) or "downloaded_asset"
                target = os.path.join(save_dir, fname)
                with open(target, "wb") as f:
                    f.write(rr.content)
                results["downloaded"].append(fname)
            except Exception as e:
                # continue on errors
                continue

        results["success"] = True
        results["message"] = f"Discovered {len(results['downloaded'])} assets (saved to {save_dir})."
        return results
    except Exception as e:
        results["message"] = f"Error parsing HTML: {e}"
        return results

def try_load_remote_model(save_dir=REMOTE_ASSET_DIR, candidates=REMOTE_MODEL_CANDIDATES):
    """
    Try to load a model file from save_dir. If none present, return None.
    """
    for c in candidates:
        p = os.path.join(save_dir, c)
        if os.path.exists(p):
            try:
                m = joblib.load(p)
                return m, p
            except Exception as e:
                # try joblib vs pickle variants
                try:
                    m = joblib.load(p)  # attempt again
                    return m, p
                except Exception:
                    continue
    # try any .pkl or .joblib present
    for f in os.listdir(save_dir):
        if f.lower().endswith((".pkl", ".joblib")):
            p = os.path.join(save_dir, f)
            try:
                m = joblib.load(p)
                return m, p
            except Exception:
                continue
    return None, None

# ---------------------------
# UI Styling (kept from your original)
# ---------------------------
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
        .btn-predict {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            color: white !important;
            font-size: 22px;
            padding: 14px;
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>AI-Driven Student Performance Prediction System</div>", unsafe_allow_html=True)

# ---------------------------
# Sidebar: Remote sync controls
# ---------------------------
st.sidebar.header("Remote integration")
st.sidebar.write("Try to fetch assets from the remote site and load a remote model if available.")

if st.sidebar.button("🔁 Sync from remote URL"):
    with st.spinner("Fetching remote page and assets..."):
        res = discover_and_download(REMOTE_URL)
        if res["success"]:
            st.sidebar.success(res["message"])
            if res["downloaded"]:
                st.sidebar.write("Downloaded files:")
                for f in res["downloaded"]:
                    st.sidebar.write(f"- {f}")
        else:
            st.sidebar.error(res["message"])

# Try to load remote model, otherwise load local model
model = None
model_path_used = None
remote_model, remote_path = try_load_remote_model()
if remote_model is not None:
    model = remote_model
    model_path_used = remote_path
    st.sidebar.success(f"Loaded remote model: {os.path.basename(remote_path)}")
else:
    # fallback local
    if os.path.exists(LOCAL_MODEL_PATH):
        try:
            model = joblib.load(LOCAL_MODEL_PATH)
            model_path_used = LOCAL_MODEL_PATH
            st.sidebar.info(f"Loaded local model: {LOCAL_MODEL_PATH}")
        except Exception as e:
            st.sidebar.error(f"Failed to load local model `{LOCAL_MODEL_PATH}`: {e}")
            model = None
    else:
        st.sidebar.warning(f"No model found at {LOCAL_MODEL_PATH} and no remote model available.")

# ---------------------------
# Tabs identical to your original layout (kept and extended)
# ---------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Enter Student Activity Data",
    "📘 Research Timeline",
    "📊 Model Output Dashboard",
    "🧪 Model Summary"
])

# ---------------------------
# TAB 1 — Input Form
# ---------------------------
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

    predict_btn = st.button("🔮 Predict Performance", use_container_width=True)

    if predict_btn:
        if model is None:
            st.error("No model available to make predictions. Try 'Sync from remote' in the sidebar or ensure `stacking_model.pkl` exists locally.")
        else:
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
                "overall_efficiency": (completed_easy_exercise + completed_medium_exercise + completed_hard_exercise) /
                                      (easy_exercise_attempt + medium_exercise_attempt + hard_exercise_attempt + 1),
            }

            df = pd.DataFrame([x])
            try:
                prediction = model.predict(df)[0]
                probability = None
                if hasattr(model, "predict_proba"):
                    probability = model.predict_proba(df)[0][1]
                st.markdown(f"<div class='prediction-box'>Prediction: {prediction}</div>", unsafe_allow_html=True)
                if probability is not None:
                    st.markdown(f"<div class='prediction-box'>Success Probability: {probability:.2f}</div>", unsafe_allow_html=True)
                else:
                    st.info("Model has no predict_proba; only class prediction displayed.")
            except Exception as e:
                st.error(f"Failed to run model prediction: {e}")
                st.exception(traceback.format_exc())

# ---------------------------
# TAB 2 — Timeline (keeps original)
# ---------------------------
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

    # Show remote index if we have it
    idx = os.path.join(REMOTE_ASSET_DIR, "remote_index.html")
    if os.path.exists(idx):
        st.markdown("**Remote site snapshot** (saved copy):")
        with open(idx, "r", encoding="utf-8") as f:
            html = f.read()
        # show a small chunk and allow download
        st.code(html[:500] + "\n\n... (truncated) ...", language="html")
        st.download_button("Download remote_index.html", data=html, file_name="remote_index.html")

    # show list of remote assets
    files = os.listdir(REMOTE_ASSET_DIR)
    if files:
        st.markdown("**Remote assets folder**")
        df_files = pd.DataFrame([{"file": f, "size_bytes": os.path.getsize(os.path.join(REMOTE_ASSET_DIR, f))} for f in files])
        st.dataframe(df_files)

# ---------------------------
# TAB 3 — Model Output Dashboard (placeholders, extended)
# ---------------------------
with tab3:
    st.markdown("<div class='section-title'>📊 Model Output Dashboard</div>", unsafe_allow_html=True)
    st.info("Below sections are placeholders. If you provide evaluation artifacts (confusion matrix, classification report, feature importance), this panel will visualize them.")

    if st.button("🔍 Show downloaded images (from remote)"):
        imgs = [f for f in os.listdir(REMOTE_ASSET_DIR) if f.lower().endswith((".png",".jpg",".jpeg",".svg"))]
        if imgs:
            cols = st.columns(3)
            for i, im in enumerate(imgs):
                with cols[i % 3]:
                    st.image(os.path.join(REMOTE_ASSET_DIR, im), caption=im, use_column_width=True)
        else:
            st.warning("No images found in remote_assets.")

    st.markdown("### 🔹 Confusion Matrix  \n*(Upload a CSV with confusion matrix to visualize)*")
    uploaded_cm = st.file_uploader("Upload confusion matrix CSV (optional)", type=["csv"])
    if uploaded_cm:
        try:
            cm_df = pd.read_csv(uploaded_cm, index_col=0)
            st.write(cm_df)
            st.text("You can use seaborn/matplotlib to plot this if desired.")
        except Exception as e:
            st.error(f"Failed to read uploaded file: {e}")

    st.markdown("### 🔹 Classification Report")
    uploaded_cr = st.file_uploader("Upload classification report CSV (optional)", type=["csv"])
    if uploaded_cr:
        try:
            cr_df = pd.read_csv(uploaded_cr)
            st.dataframe(cr_df)
        except Exception as e:
            st.error(f"Failed to read uploaded file: {e}")

# ---------------------------
# TAB 4 — Model Summary
# ---------------------------
with tab4:
    st.markdown("<div class='section-title'>🧪 Final Trained Model Summary</div>", unsafe_allow_html=True)
    if model_path_used:
        st.success(f"Model loaded from: `{model_path_used}`")
    else:
        st.error("No model loaded.")

    st.success("""
        **Model Used:** Stacking Classifier (fallback: your local model)  
        **Base Models:** Random Forest, Gradient Boosting, MLP (as originally described)  
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
        - Probability of success (if model exposes predict_proba)  
        - Early identification of at-risk learners  
    """)

    st.markdown("### Remote site embedding (if allowed by remote host)")
    try:
        # if remote site allows embedding, show it
        st.components.v1.iframe(REMOTE_URL, height=600)
    except Exception as e:
        st.info("Site cannot be embedded (remote server may disallow embedding). Use the 'Sync from remote' button in the sidebar to download assets instead.")

# ---------------------------
# End of app
# ---------------------------
