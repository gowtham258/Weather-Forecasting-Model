import pandas as pd
import joblib
from datetime import datetime
import os




WEATHER_CODE_MAP = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
    55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
    82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}


def predict_next_day():
    # Load the preprocessed data
    df = pd.read_csv("preprocessed_weather.csv", parse_dates=["date"])
    
    # Sort by date and select the latest row
    latest = df.sort_values("date").iloc[-1:]
    
    # Extract feature columns
    X_new = latest[[col for col in df.columns if ("lag" in col and "description" not in col)]]
    
    # Load the trained models
    model_temp = joblib.load("model_temperature.pkl")
    model_precip = joblib.load("model_precipitation.pkl")
    model_weather = joblib.load("model_weather_code.pkl")
    
    # Make predictions
    temp_pred = model_temp.predict(X_new)[0]
    precip_pred = model_precip.predict(X_new)[0]
    weather_pred_code = model_weather.predict(X_new)[0]
    weather_pred_desc = WEATHER_CODE_MAP.get(weather_pred_code, "Unknown")
    
    # Display predictions
    print("📅 Forecast for next day:")
    print(f"🌡️ Temperature: {temp_pred:.2f}°C")
    print(f"🌧️ Precipitation: {precip_pred:.2f} mm")
    print(f"☁️ Weather: {weather_pred_desc} (Code: {weather_pred_code})")

    
    prediction_row = {
        "date": datetime.today().date().isoformat(),
        "temperature_2m_mean": round(temp_pred, 2),
        "precipitation_sum": round(precip_pred, 2),
        "weather_description": weather_pred_desc
    }


if __name__ == "__main__":
    predict_next_day()
