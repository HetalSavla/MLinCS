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
