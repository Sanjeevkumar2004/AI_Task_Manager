import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("issues.csv")

print("Dataset Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Task Classification
df_task = df[['summary', 'issue_type']].dropna()

tfidf = TfidfVectorizer(max_features=1000)

X_task = tfidf.fit_transform(df_task['summary'])
y_task = df_task['issue_type']

svm = SVC()

print("Training Task Classifier...")
svm.fit(X_task, y_task)

# Priority Prediction
df_priority = df[['summary', 'priority']].dropna()

X_priority = tfidf.transform(df_priority['summary'])
y_priority = df_priority['priority']

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

print("Training Priority Model...")
rf.fit(X_priority, y_priority)

# Save Models
pickle.dump(svm, open("task_classifier.pkl", "wb"))
pickle.dump(rf, open("priority_model.pkl", "wb"))
pickle.dump(tfidf, open("tfidf.pkl", "wb"))

print("Models saved successfully!")