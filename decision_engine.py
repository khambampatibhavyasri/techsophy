from anamoly_detector import detect_anomalies

# Bottleneck detection logic
def detect_bottlenecks(latest_metrics):
    """
    Analyze real metrics and detect bottlenecks.
    :param latest_metrics: DataFrame with CPU, memory, DB latency, etc.
    :return: List of bottleneck types (e.g., ["CPU", "Memory", "DB Latency"])
    """
    bottlenecks = []

    if 'cpu_usage' in latest_metrics:
        avg_cpu = latest_metrics['cpu_usage'].mean()
        if avg_cpu > 75:
            bottlenecks.append("CPU")

    if 'memory_usage' in latest_metrics:
        avg_mem = latest_metrics['memory_usage'].mean()
        if avg_mem > 70:
            bottlenecks.append("Memory")

    if 'db_latency' in latest_metrics:
        avg_db_latency = latest_metrics['db_latency'].mean()
        if avg_db_latency > 150:
            bottlenecks.append("DB Latency")

    return bottlenecks


# Multi-tier decision logic
def decide_scaling_action_multitier(cpu_forecast_df, db_forecast_df, current_app_instances, current_db_instances, latest_metrics,
                                    max_app_instances=5, max_db_instances=3):
    # 1. Forecast averages and maxes
    avg_cpu = cpu_forecast_df['yhat'].mean()
    max_cpu = cpu_forecast_df['yhat'].max()

    avg_latency = db_forecast_df['yhat'].mean()
    max_latency = db_forecast_df['yhat'].max()

    # 2. Anomaly detection on CPU and DB
    cpu_anomalies = detect_anomalies(latest_metrics, column="cpu_usage")
    db_anomalies = detect_anomalies(latest_metrics, column="db_latency")

    cpu_anom_count = cpu_anomalies['anomaly'].tail(15).sum()
    db_anom_count = db_anomalies['anomaly'].tail(15).sum()

    # 3. App Tier Scaling Decision
    new_app_instances = current_app_instances
    if max_cpu > 80 or cpu_anom_count > 3:
        if current_app_instances < max_app_instances:
            new_app_instances += 1
            app_msg = f"⬆️ App Scale UP: CPU {max_cpu:.1f}% or {cpu_anom_count} anomalies → {new_app_instances} instances"
        else:
            app_msg = f"⚠️ CPU high but App instances capped at {max_app_instances}"
    elif avg_cpu < 30 and current_app_instances > 1:
        new_app_instances -= 1
        app_msg = f"⬇️ App Scale DOWN: CPU avg {avg_cpu:.1f}% → {new_app_instances} instances"
    else:
        app_msg = f"✅ App Scaling: CPU avg {avg_cpu:.1f}%. No change."

    # 4. DB Tier Scaling Decision
    new_db_instances = current_db_instances
    if max_latency > 150 or db_anom_count > 3:
        if current_db_instances < max_db_instances:
            new_db_instances += 1
            db_msg = f"⬆️ DB Scale UP: Latency {max_latency:.1f}ms or {db_anom_count} anomalies → {new_db_instances} instances"
        else:
            db_msg = f"⚠️ DB latency high but DB instances capped at {max_db_instances}"
    elif avg_latency < 90 and current_db_instances > 1:
        new_db_instances -= 1
        db_msg = f"⬇️ DB Scale DOWN: Latency avg {avg_latency:.1f}ms → {new_db_instances} instances"
    else:
        db_msg = f"✅ DB Scaling: Latency avg {avg_latency:.1f}ms. No change."

    return (new_app_instances, new_db_instances), (app_msg, db_msg)

# --- Example test run ---
if __name__ == "__main__":
    from monitoring import generate_multitier_metrics, get_latest_metrics
    from predictor import predict_future_cpu
    from predictor_db import predict_future_db_latency

    df = generate_multitier_metrics(180)
    latest = get_latest_metrics(df, 60)

    cpu_forecast = predict_future_cpu(latest, 15)
    db_forecast = predict_future_db_latency(latest, 15)

    (app_new, db_new), (app_msg, db_msg) = decide_scaling_action_multitier(
        cpu_forecast, db_forecast,
        current_app_instances=2,
        current_db_instances=1,
        latest_metrics=latest
    )

    print(app_msg)
    print(db_msg)
