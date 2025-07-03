import pandas as pd
from prophet import Prophet
from datetime import datetime, timedelta

def prepare_data_for_prophet(df):
    """Prepares CPU usage data for Prophet"""
    cpu_df = df.reset_index()[['timestamp', 'cpu_usage']]
    cpu_df.rename(columns={'timestamp': 'ds', 'cpu_usage': 'y'}, inplace=True)
    return cpu_df

def predict_future_cpu(df, forecast_minutes=15):
    """
    Forecast CPU usage using Prophet
    :param df: DataFrame with 'timestamp' and 'cpu_usage'
    :param forecast_minutes: how many minutes ahead to predict
    :return: DataFrame with predictions
    """
    cpu_df = prepare_data_for_prophet(df)
    model = Prophet(interval_width=0.95, daily_seasonality=True)
    model.fit(cpu_df)

    future = model.make_future_dataframe(periods=forecast_minutes, freq='min')
    forecast = model.predict(future)

    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_minutes)
    forecast.set_index('ds', inplace=True)
    return forecast

# --- Example usage ---
if __name__ == "__main__":
    from monitoring import generate_metrics_data, get_latest_metrics
    
    df = generate_metrics_data(180)  # simulate 3 hours
    latest = get_latest_metrics(df, 60)  # use past hour for prediction

    forecast_df = predict_future_cpu(latest, forecast_minutes=15)
    print(forecast_df)
