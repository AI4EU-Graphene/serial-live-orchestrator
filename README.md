# ⚡ Smart Grid AI Orchestrator

A modular AI microservice system built for orchestrating, forecasting, and analyzing real-time energy grid data using real-world inputs from EirGrid.

---

## 🔧 Architecture Overview

This orchestrator handles smart grid data using containerized AI nodes:

- **`data-ingestor`** – Downloads energy data (demand, wind, CO₂, etc.)
- **`data-preprocessor`** – Merges and pivots region-wise CSVs
- **`demand-forecaster`** – Forecasts short-term demand using ARIMA
- **`anomaly-detector`** – Detects anomalies using Isolation Forest
- **`alert-node`** – Raises system alerts if anomaly count crosses threshold
- **`cube-node` & `square-node`** – Test nodes for mathematical ops
- **`load-optimizer`** – *(coming soon)* Optimize load across grid
- **`orchestrator-client`** – *(optional)* For future gRPC orchestration

---

## 📁 Directory Structure

```bash
generic-serial-orchestrator/
├── data_ingestor/
│   ├── ingestor_service.py
│   └── EirGrid_Data_Download/
├── data_preprocessor/
│   └── preprocessor_service.py
├── demand_forecaster/
│   └── forecast_service.py
├── anomaly_detector/
│   └── anomaly_service.py
├── data_alert_node/
│   └── alert_service.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 🐳 Run all services with Docker Compose

```bash
docker-compose up --build
```

### ✅ Check running containers

```bash
docker ps
```

---

## 🌐 Available API Endpoints

| Node               | Endpoint               | Port   | Function                                |
|--------------------|------------------------|--------|------------------------------------------|
| data-ingestor      | `/get-demand`          | 5004   | Trigger data download from EirGrid       |
| data-preprocessor  | `/preprocess`          | 5005   | Merge & pivot CSVs into one DataFrame    |
| demand-forecaster  | `/forecast`            | 5002   | ARIMA-based short-term demand forecast   |
| anomaly-detector   | `/detect-anomalies`    | 5006   | Identify anomalies in the demand data    |
| alert-node         | `/check-alert`         | 5007   | Raise alert if anomalies exceed threshold|

---

## 📊 Pivoted Data Format Example

| Timestamp           | Region | SYSTEM_DEMAND | CO2_INTENSITY | WIND_ACTUAL | SNSP_ALL |
|---------------------|--------|----------------|----------------|-------------|-----------|
| 2024-04-01 00:00:00 | ALL    | 3770.0         | 200            | 1624.0      | 50.86     |
| 2024-04-01 00:00:00 | ROI    | 3223.0         | 175            | 1467.0      | NaN       |
| 2024-04-01 00:00:00 | NI     | 547.0          | 346            | 157.0       | NaN       |

---

## 🧠 Machine Learning Models Used

- **ARIMA (AutoRegressive Integrated Moving Average)**  
  For forecasting next 48 intervals of system demand

- **Isolation Forest**  
  For unsupervised anomaly detection on key metrics

---

## ⚠️ Anomaly Alerting

`alert-node` returns an `"ALERT"` status if anomalies exceed the set threshold (default: 20)

```json
{
  "status": "ALERT",
  "anomalies_detected": 3165,
  "threshold": 20
}
```

---

## 🗺️ Roadmap

- ✅ Real-time demand ingestion
- ✅ Unified pivoting of multiple regions
- ✅ Forecasting + Anomaly Detection
- ✅ Threshold-based alert node
- ⏳ Coming soon: Load optimization node
- ⏳ Future: Kafka event pipeline + real-time dashboard

---

## 👤 Author

**Vaibhav Rana**  
MSc Business Analytics, Maynooth University  
[GitHub](https://github.com/VaibhavTechie)

_Last updated: 2025-03-28_
