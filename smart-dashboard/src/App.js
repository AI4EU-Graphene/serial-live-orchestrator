import React, { useEffect, useState } from "react";
import axios from "axios";
import "./dashboard.css";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:5013/smart-run")
      .then((response) => {
        console.log("SMART RESPONSE >>>", response.data);
        setData(response.data);
      })
      .catch((error) => {
        console.error("ERROR FETCHING SMART DATA >>>", error);
      });
  }, []);

  if (!data) {
    return <div className="terminal loading">Initializing Smart Grid Agent...</div>;
  }

  const { pipeline = [], results = {} } = data;

  const masterNodes = [
    "Data Source",
    "Demand Forecaster",
    "Grid Rebalancer",
    "Storage Optimizer",
    "Anomaly Detector"
  ];

  const nodeRenderMap = {
    "Data Source": () => (
      <TerminalCard
        title="📥 DATA SOURCE"
        content={`> STATUS: ${results["Data Source"]?.status || 'Unavailable'}\n> LAST MODIFIED: ${results["Data Source"]?.last_modified || 'N/A'}`}
      />
    ),
    "Demand Forecaster": () => (
      <TerminalCard
        title="📊 DEMAND FORECAST"
        content={`> MODEL: ${results["Demand Forecaster"]?.model_path?.split("/").pop() || 'N/A'}\n> MSE: ${results["Demand Forecaster"]?.mse_on_test ?? 'N/A'}`}
      />
    ),
    "Grid Rebalancer": () => (
      <TerminalCard
        title="⚖️ GRID REBALANCER"
        content={`> PEAK DEMAND: ${results["Grid Rebalancer"]?.rebalancing_summary?.ALL?.peak_demand || 'N/A'}\n> REBALANCING: ${results["Grid Rebalancer"]?.rebalancing_summary?.ALL?.rebalancing_required ? 'YES' : 'NO'}`}
      />
    ),
    "Storage Optimizer": () => (
      <TerminalCard
        title="🔋 STORAGE OPTIMIZER"
        content={`> ACTION: ${results["Storage Optimizer"]?.action || 'N/A'}\n> STATUS: ${results["Storage Optimizer"]?.status || 'N/A'}`}
      />
    ),
    "Anomaly Detector": () => (
      <div className="terminal-card">
        <h2 className="terminal-header">🧯 ANOMALY DETECTOR</h2>
        <p className="terminal-subtext">
          > TOTAL ANOMALIES DETECTED: {results["Anomaly Detector"]?.anomalies_found || 0}
        </p>
        <div className="terminal-log">
          {results["Anomaly Detector"]?.anomaly_timestamps?.length > 0 ? (
            results["Anomaly Detector"].anomaly_timestamps.slice(0, 300).map((timestamp, index) => (
              <div key={index}>
                [{index + 1}] {timestamp}
              </div>
            ))
          ) : (
            <p>> NO ANOMALIES FOUND</p>
          )}
        </div>
        <p className="terminal-footer">> Showing first 300 timestamps</p>
      </div>
    )
  };

  return (
    <div className="terminal">
      <h1 className="terminal-title">⚡ SMART GRID ORCHESTRATOR COMMAND CENTER</h1>
      <div className="terminal-grid">
        {masterNodes.map((node) => (
          pipeline.includes(node) ? (
            <React.Fragment key={node}>{nodeRenderMap[node]()}</React.Fragment>
          ) : (
            <TerminalCard key={node} title={`❌ ${node.toUpperCase()}`} content="> NODE NOT EXECUTED IN PIPELINE" dimmed />
          )
        ))}
      </div>
    </div>
  );
}

function TerminalCard({ title, content, dimmed }) {
  return (
    <div className={`terminal-card${dimmed ? " dimmed" : ""}`}>
      <h2 className="terminal-header">{title}</h2>
      <pre className="terminal-content">{content}</pre>
    </div>
  );
}
