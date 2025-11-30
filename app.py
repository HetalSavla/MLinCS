import streamlit as st
import pandas as pd
import joblib

model = joblib.load("stacking_model.pkl")

st.title("Student Performance Prediction")

total_easy_exercise = st.number_input("Total easy exercise", min_value=0, step=1)
completed_easy_exercise = st.number_input("Completed easy exercise", min_value=0, step=1)
easy_exercise_completion_time = st.number_input("Easy exercise completion time", min_value=0, step=1)
easy_exercise_attempt = st.number_input("Easy exercise attempt", min_value=0, step=1)
easy_exercise_syntax_error = st.number_input("Easy exercise syntax error", min_value=0, step=1)

total_medium_exercise = st.number_input("Total medium exercise", min_value=0, step=1)
completed_medium_exercise = st.number_input("Completed medium exercise", min_value=0, step=1)
medium_exercise_completion_time = st.number_input("Medium exercise completion time", min_value=0, step=1)
medium_exercise_attempt = st.number_input("Medium exercise attempt", min_value=0, step=1)
medium_exercise_syntax_error = st.number_input("Medium exercise syntax error", min_value=0, step=1)

total_hard_exercise = st.number_input("Total hard exercise", min_value=0, step=1)
completed_hard_exercise = st.number_input("Completed hard exercise", min_value=0, step=1)
hard_exercise_completion_time = st.number_input("Hard exercise completion time", min_value=0, step=1)
hard_exercise_attempt = st.number_input("Hard exercise attempt", min_value=0, step=1)
hard_exercise_syntax_error = st.number_input("Hard exercise syntax error", min_value=0, step=1)

which_time_span_encoded = st.selectbox("Time Span", [1, 2, 3])

if st.button("Predict"):
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

    st.write("### Prediction:", prediction)
    st.write("### Probability:", probability)
