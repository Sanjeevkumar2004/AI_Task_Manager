from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# Load models
svm = pickle.load(open("task_classifier.pkl", "rb"))
rf = pickle.load(open("priority_model.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))

@app.route("/")
def home():
    return "AI Task Manager Backend Running"

@app.route("/test")
def test():
    try:
        task = "Fix login issue in dashboard"

        vector = tfidf.transform([task])

        category = svm.predict(vector)[0]
        priority = rf.predict(vector)[0]

        return jsonify({
            "sample_task": task,
            "category": str(category),
            "priority": str(priority)
        })

    except Exception as e:
        print("TEST ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        print("Received Data:", data)

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        task = data.get("task")

        if not task:
            return jsonify({"error": "Task is empty"}), 400

        print("Task:", task)

        vector = tfidf.transform([task])

        print("Vector Shape:", vector.shape)

        category = svm.predict(vector)[0]
        priority = rf.predict(vector)[0]

        return jsonify({
            "task": task,
            "category": str(category),
            "priority": str(priority)
        })

    except Exception as e:
        print("PREDICT ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)