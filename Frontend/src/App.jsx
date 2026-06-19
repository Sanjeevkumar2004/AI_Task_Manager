import { useState } from "react";
import axios from "axios";

function App() {
  const [task, setTask] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const predictTask = async () => {
    if (!task.trim()) {
      alert("Please enter a task description");
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:5000/predict",
        {
          task: task
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Backend connection failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "800px",
        margin: "50px auto",
        padding: "20px",
        fontFamily: "Arial"
      }}
    >
      <h1>🤖 AI Task Management System</h1>

      <textarea
        rows="6"
        style={{
          width: "100%",
          padding: "10px",
          fontSize: "16px"
        }}
        placeholder="Enter task description..."
        value={task}
        onChange={(e) => setTask(e.target.value)}
      />

      <br />
      <br />

      <button
        onClick={predictTask}
        style={{
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer"
        }}
      >
        Predict Task
      </button>

      <br />
      <br />

      {loading && <h3>Processing...</h3>}

      {result && (
        <div
          style={{
            border: "1px solid #ccc",
            padding: "20px",
            borderRadius: "10px"
          }}
        >
          <h2>Prediction Result</h2>

          <p>
            <strong>Task:</strong> {result.task}
          </p>

          <p>
            <strong>Category:</strong> {result.category}
          </p>

          <p>
            <strong>Priority:</strong> {result.priority}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;