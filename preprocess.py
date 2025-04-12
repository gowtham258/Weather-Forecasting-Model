# preprocess.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Weather code to description mapping
WEATHER_CODE_MAP = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}

def preprocess_weather_data(input_path="historical_weather_daily.csv", output_path="preprocessed_weather.csv"):
    df = pd.read_csv(input_path, parse_dates=["date"])

    # Map weather code to description
    df["weather_description"] = df["weather_code"].map(WEATHER_CODE_MAP)

    # Create lag features
    lag_features = [
        "temperature_2m_mean", "temperature_2m_max",
        "relative_humidity_2m_mean", "precipitation_sum", "weather_code",
        "wind_speed_10m_mean", "wind_gusts_10m_mean", "surface_pressure_mean",
        "daylight_duration", "sunshine_duration", "dew_point_2m_mean",
        "cloud_cover_mean", "pressure_msl_mean"
    ]

    for col in lag_features:
        df[f"{col}_lag1"] = df[col].shift(7)

    # Lag for weather description
    df["weather_description_lag1"] = df["weather_description"].shift(7)

    # Encode weather description lag
    le = LabelEncoder()
    df["weather_description_lag1_encoded"] = le.fit_transform(df["weather_description_lag1"].astype(str))

    # Drop NaN rows caused by lagging
    df.dropna(inplace=True)

    # Save processed dataset
    df.to_csv(output_path, index=False)
    print(f"✅ Preprocessed data saved to '{output_path}'")

if __name__ == "__main__":
    preprocess_weather_data()
