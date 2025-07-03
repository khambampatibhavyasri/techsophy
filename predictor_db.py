from prophet import Prophet
import pandas as pd

def prepare_db_latency_data(df):
    db_df = df.reset_index()[['timestamp', 'db_latency']].dropna()
    db_df.rename(columns={'timestamp': 'ds', 'db_latency': 'y'}, inplace=True)
    return db_df

def predict_future_db_latency(df, forecast_minutes=15):
    """
    Forecast DB latency using Prophet.
    """
    db_df = prepare_db_latency_data(df)

    if db_df.empty or len(db_df) < 10:
        raise ValueError("Not enough DB latency data to fit Prophet model.")

    model = Prophet(interval_width=0.95, daily_seasonality=False)
    model.fit(db_df)

    future = model.make_future_dataframe(periods=forecast_minutes, freq='min')
    forecast = model.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_minutes)
    forecast.set_index('ds', inplace=True)
    return forecast

# Example usage
if __name__ == "__main__":
    from monitoring import generate_multitier_metrics
    df = generate_multitier_metrics(180)
    forecast = predict_future_db_latency(df, 15)
    print(forecast.tail())
