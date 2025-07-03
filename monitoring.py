import numpy as np
import pandas as pd
from datetime import datetime

def generate_metrics_data(duration_minutes=180):
    """Legacy single-tier metrics generator (still usable for testing)"""
    time_index = pd.date_range(end=datetime.now(), periods=duration_minutes, freq='min')
    base_cpu = 50 + 20 * np.sin(np.linspace(0, 4 * np.pi, duration_minutes))
    noise = np.random.normal(0, 3, duration_minutes)
    spikes = np.random.choice([0, 25], size=duration_minutes, p=[0.98, 0.02])
    cpu = np.clip(base_cpu + noise + spikes, 0, 100)
    rps = cpu * 10 + np.random.normal(0, 10, duration_minutes)
    mem = 40 + 0.5 * cpu + np.random.normal(0, 2, duration_minutes)

    df = pd.DataFrame({
        'timestamp': time_index,
        'cpu_usage': cpu,
        'rps': rps,
        'memory_usage': mem
    })
    df.set_index('timestamp', inplace=True)
    return df

def generate_multitier_metrics(duration_minutes=180):
    """Simulate multi-tier metrics for App + DB tiers"""
    time_index = pd.date_range(end=datetime.now(), periods=duration_minutes, freq='min')

    # App Tier
    base_cpu = 50 + 20 * np.sin(np.linspace(0, 4 * np.pi, duration_minutes))
    noise = np.random.normal(0, 3, duration_minutes)
    spikes = np.random.choice([0, 25], size=duration_minutes, p=[0.98, 0.02])
    cpu = np.clip(base_cpu + noise + spikes, 0, 100)
    rps = cpu * 10 + np.random.normal(0, 10, duration_minutes)

    # DB Tier
    db_latency = 100 + 30 * np.sin(np.linspace(0, 2 * np.pi, duration_minutes)) + np.random.normal(0, 10, duration_minutes)
    queue_length = 20 + 5 * np.sin(np.linspace(0, 6 * np.pi, duration_minutes)) + np.random.normal(0, 3, duration_minutes)
    spikes_db = np.random.choice([0, 40], size=duration_minutes, p=[0.97, 0.03])
    db_latency += spikes_db

    df = pd.DataFrame({
        'timestamp': time_index,
        'cpu_usage': cpu,
        'rps': rps,
        'db_latency': db_latency,
        'queue_length': queue_length
    })
    df.set_index('timestamp', inplace=True)
    return df

def get_latest_metrics(df, window_minutes=60):
    """Slice last N minutes from a time-indexed DataFrame"""
    cutoff = datetime.now() - pd.Timedelta(minutes=window_minutes)
    return df[df.index >= cutoff]
