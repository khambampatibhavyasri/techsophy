# Smart Auto-Scaler – Multi-Tier Forecast-Based Auto Scaling

A complete AI-driven auto-scaling simulation for cloud-native applications. This project forecasts system metrics and automatically adjusts resources across multiple tiers (App + DB) based on predicted demand, anomalies, and scaling rules.

---

##  Features

✅ Simulated monitoring of key metrics (CPU, RPS, DB Latency)  
✅ Time Series Forecasting using [Facebook Prophet](https://facebook.github.io/prophet/)  
✅ Rule-based auto-scaling logic with anomaly detection and cooldown  
✅ Multi-tier architecture with independent scaling for App & DB  
✅ Visual performance metrics saved as PNG  
✅ Clean modular design – ready for real-world extensions

---

## Architecture

```
[Monitoring] → [Prediction] → [Decision Engine] → [Scaling Executor]
```

Modules:
- `monitoring.py` → Generates time-series metrics (CPU, latency)
- `predictor.py` & `predictor_db.py` → Forecast CPU and DB latency
- `decision_engine.py` → Detects bottlenecks, decides scaling
- `scaling_executor.py` → Logs simulated scaling actions
- `autoscaler.py` → Runs the pipeline in a loop

---

##  Project Structure

```
smart-autoscaler/
├── autoscaler.py             # Main scheduler
├── monitoring.py             # Metric simulation
├── predictor.py              # CPU forecast (Prophet)
├── predictor_db.py           # DB latency forecast (Prophet)
├── decision_engine.py        # Scaling logic
├── anomaly_detector.py       # Anomaly detection (Z-score)
├── scaling_executor.py       # Scaling simulator
├── multi_tier_metrics_plot.png
└── README.md                 # You're reading it
```

---

## 🧪 How to Run

### 1. Install Dependencies

```bash
pip install prophet pandas matplotlib numpy schedule
```

> Tip: For Windows/macOS, use `cmdstanpy` backend for Prophet

```bash
pip install cmdstanpy
```

### 2. Start Auto-Scaler

```bash
python autoscaler.py
```

- Runs every 5 minutes
- Simulates metrics, forecasts, makes decisions
- Outputs saved to: `multi_tier_metrics_plot.png`

---

## Sample Output

```
 Detected Bottlenecks: CPU
 App Tier Decision: ⬆ App Scale UP: CPU 87.3% → 3 instances
DB Tier Decision: DB Scaling: Latency avg 102ms. No change.
[2025-07-03 11:49:54]  Scaling App Tier → 3 instances
```

---

## Skills Demonstrated

- AI/ML: Forecasting with Prophet, anomaly detection
- DevOps: Resource scaling logic with cooldown, rules
- Critical Thinking: Bottleneck detection, resource control
- Modular Codebase: Extensible, testable components
- Problem Solving: Handles traffic spikes, multi-tier logic

---

## License

MIT License © 2025 Varun Teja Kalakoti

---

Built for cloud simulation, intelligent systems coursework, and DevOps readiness.  
Let it forecast, auto-scale, and impress! 
