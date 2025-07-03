import schedule
import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from monitoring import generate_multitier_metrics, get_latest_metrics
from predictor import predict_future_cpu
from predictor_db import predict_future_db_latency
from decision_engine import detect_bottlenecks, decide_scaling_action_multitier
from scaling_executor import scale_resources

# Initial instance counts
app_instances = 2
db_instances = 1

# Separate cooldown timers
last_app_scaled = datetime.now() - timedelta(minutes=10)
last_db_scaled = datetime.now() - timedelta(minutes=10)

def cooldown_passed(last_scaled_time, cooldown_minutes=5):
    return datetime.now() - last_scaled_time > timedelta(minutes=cooldown_minutes)

def autoscale_job():
    global app_instances, db_instances, last_app_scaled, last_db_scaled

    print(f"\n🕒 Running Multi-Tier AutoScaler @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Step 1: Generate and slice multi-tier metrics
    df = generate_multitier_metrics(180)
    latest = get_latest_metrics(df, 60)

    # Step 2: Bottlenecks
    bottlenecks = detect_bottlenecks(latest)
    print(f"🧠 Detected Bottlenecks: {', '.join(bottlenecks) if bottlenecks else 'None'}")

    # Step 3: Forecast both CPU and DB latency
    cpu_forecast = predict_future_cpu(latest, 15)
    db_forecast = predict_future_db_latency(latest, 15)

    # Step 4: Multi-tier scaling decision
    (new_app_instances, new_db_instances), (app_msg, db_msg) = decide_scaling_action_multitier(
        cpu_forecast, db_forecast,
        app_instances, db_instances,
        latest_metrics=latest
    )

    print("📈 App Tier Decision:", app_msg)
    print("📊 DB Tier Decision:", db_msg)

    # Step 5: Apply per-tier scaling with cooldowns
    if new_app_instances != app_instances:
        if cooldown_passed(last_app_scaled):
            scale_resources(new_app_instances, tier="App")
            last_app_scaled = datetime.now()
            app_instances = new_app_instances
        else:
            print("⏳ App scaling cooldown active. Skipping App scale this round.")

    if new_db_instances != db_instances:
        if cooldown_passed(last_db_scaled):
            scale_resources(new_db_instances, tier="DB")
            last_db_scaled = datetime.now()
            db_instances = new_db_instances
        else:
            print("⏳ DB scaling cooldown active. Skipping DB scale this round.")

    # Step 6: Optional plotting of CPU and DB Latency
    plt.figure(figsize=(10, 5))
    plt.subplot(2, 1, 1)
    plt.plot(latest.index, latest['cpu_usage'], label="CPU Usage (%)")
    plt.axhline(80, color='r', linestyle='--', label="CPU Scale-Up")
    plt.axhline(30, color='g', linestyle='--', label="CPU Scale-Down")
    plt.legend()
    plt.title("App Tier: CPU Usage")

    plt.subplot(2, 1, 2)
    plt.plot(latest.index, latest['db_latency'], label="DB Latency (ms)", color='orange')
    plt.axhline(150, color='r', linestyle='--', label="Latency Scale-Up")
    plt.axhline(90, color='g', linestyle='--', label="Latency Scale-Down")
    plt.legend()
    plt.title("DB Tier: Latency")

    plt.tight_layout()
    plt.savefig("multi_tier_metrics_plot.png")
    print("📊 Saved multi-tier plot to multi_tier_metrics_plot.png")

# Run every 5 minutes
schedule.every(5).minutes.do(autoscale_job)

if __name__ == "__main__":
    print("🚀 Multi-Tier Smart Auto-Scaler Started\n")
    autoscale_job()

    while True:
        schedule.run_pending()
        time.sleep(1)
