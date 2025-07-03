import pandas as pd

def detect_anomalies(df, column="cpu_usage", threshold=3):
    """
    Detects anomalies using Z-score method.

    :param df: DataFrame with the metric column to analyze
    :param column: Column to detect anomalies in (default: 'cpu_usage')
    :param threshold: Z-score threshold above which values are considered anomalies
    :return: DataFrame with 'z_score' and 'anomaly' (True/False)
    """
    df = df.copy()
    
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    mean = df[column].mean()
    std = df[column].std()

    if std == 0:
        df['z_score'] = 0
        df['anomaly'] = False
    else:
        df['z_score'] = (df[column] - mean) / std
        df['anomaly'] = df['z_score'].abs() > threshold

    return df[['z_score', 'anomaly']]

# --- Example usage ---
if __name__ == "__main__":
    from monitoring import generate_metrics_data

    df = generate_metrics_data(180)  # simulate 3 hours
    anomalies = detect_anomalies(df, column="cpu_usage")
    result = df.join(anomalies)
    print(result[result['anomaly'] == True].tail())
