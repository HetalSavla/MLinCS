import streamlit as st

def research_overview_section():

    st.title("🎓 PhD Research Project – Student Performance Prediction System")
    st.subheader("AI-Powered Early Warning Framework for Computer Education")
    st.write("Predicting at-risk students using behavioral analytics and machine learning.")

    st.markdown("---")

    # -----------------------------
    # Research Overview
    # -----------------------------
    st.header("📘 Research Overview")
    st.write("""
This PhD research project focuses on predicting student performance in C programming courses 
for BCA students in the Saurashtra region.

By leveraging behavioral analytics from an online IDE and advanced machine learning models, 
we aim to identify at-risk students early in the semester, enabling timely interventions.

Our privacy-friendly approach requires no prior academic history.
""")

    st.info("""
**Key Highlights**
- 5 ML Models Trained  
- Privacy-Friendly Approach  
- Early Detection System  
- Real-time Predictions  
    """)

    st.markdown("---")

    # -----------------------------
    # The Challenge
    # -----------------------------
    st.header("⚠️ The Challenge")

    st.subheader("Traditional Approach")
    st.write("""
Traditional academic systems are reactive — struggling students are identified only 
after failing tests or assignments.

By then, it's too late for meaningful intervention.

- Late detection of at-risk students  
- Limited time for intervention  
- High failure rates persist  
    """)

    st.markdown("---")

    # -----------------------------
    # Our Solution
    # -----------------------------
    st.header("✅ Our Solution")

    st.write("""
Our AI-powered early warning system continuously monitors students’ coding behavior 
in real-time and predicts potential failures weeks before exams.
""")

    st.success("""
**System Benefits**
- Early risk detection (weeks ahead)  
- Ample time for intervention  
- Improved student outcomes  
    """)

    st.markdown("### 🔄 System Components")
    st.write("""
- **Online IDE** – Tracks real-time behavior  
- **ML Pipeline** – Analyzes features & patterns  
- **Dashboard** – Provides early warning alerts  
    """)

    st.markdown("---")

    # -----------------------------
    # Technology Stack
    # -----------------------------
    st.header("🧱 Technology Stack")
    st.write("""
- **Backend:** PHP 7.4+  
- **ML Pipeline:** Python 3.8+  
- **Database:** MySQL  
- **Framework:** scikit-learn  
- **Frontend:** Bootstrap 5  
- **Visualizations:** Chart.js  

A fully integrated end-to-end ML solution.
""")

    st.markdown("---")

    # -----------------------------
    # ML Models
    # -----------------------------
    st.header("🧠 Machine Learning Models")

    st.subheader("Baseline Models")
    st.write("""
- Dummy Classifier  
- Logistic Regression  
Accuracy: **75–82%**, F1: **0.78–0.84**
""")

    st.subheader("Neural Network (MLP)")
    st.write("""
- Accuracy: **85–88%**  
- F1 Score: **0.86–0.89**
""")

    st.subheader("Random Forest")
    st.write("""
- Accuracy: **83–87%**  
- F1 Score: **0.84–0.88**
""")

    st.subheader("Gradient Boosting")
    st.write("""
- Accuracy: **86–90%**  
- F1 Score: **0.87–0.91**
""")

    st.warning("Performance numbers are based on similar studies; final results pending real dataset analysis.")

    st.markdown("---")

    # -----------------------------
    # Key Features
    # -----------------------------
    st.header("⭐ Key Features")
    st.write("""
- Privacy-friendly (no prior academic data)  
- Real-time behavioral tracking  
- Early risk detection  
- Multiple ML models  
- Comprehensive evaluation metrics  
- Actionable insights for teachers  
    """)

    st.markdown("---")

    # -----------------------------
    # Privacy Approach
    # -----------------------------
    st.header("🔒 Privacy-First Approach")
    st.write("""
The system uses only IDE behavioral data — no personal or academic history is required.
""")

    st.markdown("---")

    # -----------------------------
    # How It Works
    # -----------------------------
    st.header("⚙️ How It Works (Pipeline Steps)")
    st.markdown("""
1. **Student Submits Code**  
2. **Behavioral Data Collection**  
3. **Feature Extraction**  
4. **ML Model Prediction**  
5. **Early Warning Dashboard**  
""")

    st.markdown("---")

    # -----------------------------
    # Expected Outcomes
    # -----------------------------
    st.header("🎯 Expected Outcomes")
    st.write("""
- Identify key behavioral indicators  
- Build a high-accuracy early warning model  
- Provide teachers with actionable insights  
    """)

    st.markdown("---")

    # -----------------------------
    # Implementation Status
    # -----------------------------
    st.header("📌 Implementation Status")

    st.write("""
- System Development – ✔ Completed  
- ML Pipeline – ✔ Completed  
- Dashboard – ✔ Completed  
- Data Collection – 🔄 In Progress  
- Model Training – ⏳ Pending  
- Publication – ⏳ Pending  
Target: **Scopus-indexed journal, end of 2025**
""")

    st.markdown("---")

    # -----------------------------
    # Dataset Engineering (Your Steps)
    # -----------------------------
    st.header("🧪 Dataset Engineering Workflow")

    st.code("""
Step-1: Derived ds1.csv from primary MySQL database  
Step-2: Trained 5 ML models using:
    - Logistic Regression
    - Random Forest
    - Gradient Boosting
    - MLP
    - SVM
Results saved in model_results.csv / .xlsx

Step-3: code1.py → engineered_ds1.csv created  
Step-4.1: Tried improved models on engineered dataset  
Step-4.2: Stacking (RF, GB, MLP, SVM, XGB)
Best stack score: F1 = 0.857, ROC = 0.907  

Step-5: Visualization (code3.py)
""")

    st.markdown("---")



# Call the function inside main page
research_overview_section()

