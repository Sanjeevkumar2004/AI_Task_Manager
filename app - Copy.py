import streamlit as st
import pickle
import pandas as pd

# Load models
svm = pickle.load(open("task_classifier.pkl", "rb"))
rf = pickle.load(open("priority_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

# Load dataset
df = pd.read_csv("issues.csv")

# Workload balancing
workload = df.groupby('assignee_id')['story_points'].sum()
least_busy = workload.idxmin()

st.title("AI Powered Task Management System")

task = st.text_area("Enter Task Description")

if st.button("Predict"):

    task_vector = tfidf.transform([task])

    category = svm.predict(task_vector)[0]

    priority = rf.predict(task_vector)[0]

    st.success(f"Category: {category}")
    st.success(f"Priority: {priority}")
    st.success(f"Assign To Employee ID: {least_busy}")