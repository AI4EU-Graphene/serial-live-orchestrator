// src/SmartResults.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const SmartResults = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:5013/smart-run")
      .then(res => setData(res.data))
      .catch(err => setError(err.message));
  }, []);

  if (error) return <div className="text-red-500 p-4">Error: {error}</div>;
  if (!data) return <div className="p-4">Loading...</div>;

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Smart Agent Pipeline Execution</h2>
      <p className="mb-2"><strong>Status:</strong> {data.status}</p>
      <p className="mb-2"><strong>Pipeline:</strong> {data.pipeline.join(" → ")}</p>

      <h3 className="text-lg font-semibold mt-4">Node Results:</h3>
      <ul className="list-disc ml-6">
        {Object.entries(data.results).map(([node, result]) => (
          <li key={node}>
            <strong>{node}</strong>: {typeof result === "object" ? JSON.stringify(result) : result}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SmartResults;