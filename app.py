
import streamlit as st
import pandas as pd
import joblib
from datetime import timedelta, datetime
from preprocess import WEATHER_CODE_MAP

# ---------- Custom CSS for Minimal Look and Weather Theme ----------
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 800px;
        margin: auto;
        background-color: #e0f7fa;
        color: #006064;
        padding: 20px;
        border-radius: 10px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #006064;
        text-align: center;
    }
    .stButton>button {
        background-color: #006064;
        color: #ffffff;
        border: none;
        border-radius: 5px;
        padding: 0.5em 1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Load Models and Data ----------
model_temp = joblib.load("model_temperature.pkl")
model_precip = joblib.load("model_precipitation.pkl")
model_code = joblib.load("model_weather_code.pkl")
feature_cols = joblib.load("features.pkl")

df = pd.read_csv("preprocessed_weather.csv", parse_dates=["date"])
# Make sure 'date' is timezone-naive and normalized
df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.normalize()

# ---------- Helper: Recursive Forecasting Function ----------
def recursive_forecast(days_ahead, base_row):
    forecasts = []
    current_features = base_row.copy()

    for day in range(days_ahead):
        # Predict using the features (ensuring we select only training features)
        temp_pred = model_temp.predict(current_features[feature_cols])[0]
        precip_pred = model_precip.predict(current_features[feature_cols])[0]
        code_pred = model_code.predict(current_features[feature_cols])[0]

        # Map weather code to description
        weather_desc = WEATHER_CODE_MAP.get(int(code_pred), "Unknown")

        # Calculate forecast date (using .iloc[0] to get a pandas Timestamp)
        forecast_date = current_features["date"].iloc[0] + timedelta(days=1)

        # Store forecast for the day
        forecasts.append({
            "date": forecast_date,
            "temperature_2m_mean": temp_pred,
            "precipitation_sum": precip_pred,
            "weather_code": code_pred,
            "weather_description": weather_desc
        })

        # Update current_features for next iteration:
        # For each key feature, shift lag features by one.
        for feature in ["temperature_2m_mean", "precipitation_sum", "weather_code"]:
            for lag in range(7, 1, -1):
                col_current = f"{feature}_lag{lag}"
                col_previous = f"{feature}_lag{lag-1}"
                if col_previous in current_features.columns and col_current in current_features.columns:
                    current_features[col_current] = current_features[col_previous]
            # Set lag1 to predicted value
            current_features[f"{feature}_lag1"] = temp_pred if feature=="temperature_2m_mean" else \
                                                  precip_pred if feature=="precipitation_sum" else \
                                                  code_pred
        # Update the date in current_features for the next iteration
        current_features["date"] = forecast_date

    return pd.DataFrame(forecasts)

# ---------- Streamlit App UI ----------
st.title("🌤️ Kerala Weather Forecast Dashboard")
st.caption("A minimal dashboard for historical and future weather forecasting.")

# Define forecast range
latest_date = df["date"].max().date()
max_predict_date = latest_date + timedelta(days=7)

# Date input: user can select any date from historical to 7 days in the future
selected_date = st.date_input(
    "Select a date for weather details:",
    min_value=df["date"].min().date(),
    max_value=max_predict_date,
    value=latest_date  # default to latest date
)
selected_date = pd.to_datetime(selected_date).tz_localize(None).normalize()

# ---------- Display Historical Data or Forecast ----------
if selected_date <= pd.Timestamp(latest_date):
    st.subheader(f"📖 Historical Weather on {selected_date.date()}")
    historical_row = df[df["date"] == selected_date]
    if not historical_row.empty:
        st.metric("🌡️ Temperature (°C)", round(historical_row["temperature_2m_mean"].values[0], 2))
        st.metric("🌧️ Precipitation (mm)", round(historical_row["precipitation_sum"].values[0], 2))
        weather_code = int(historical_row["weather_code"].values[0])
        st.metric("🌥️ Weather", f"{WEATHER_CODE_MAP.get(weather_code, 'Unknown')} (Code {weather_code})")
        with st.expander("🔍 View Raw Data"):
            st.dataframe(historical_row.T)
    else:
        st.warning("No historical data available for this date.")
else:
    st.subheader(f"📊 Forecast for {selected_date.date()}")
    # Calculate how many days ahead we are forecasting
    days_ahead = (selected_date - pd.Timestamp(latest_date)).days
    st.write(f"Forecasting {days_ahead} day(s) into the future, using the latest data from {latest_date}.")

    # Get the latest row (base row) for recursive forecasting
    base_row = df[df["date"] == pd.Timestamp(latest_date)]
    if base_row.empty:
        st.error("No historical data available for the latest date.")
    else:
        forecast_df = recursive_forecast(days_ahead, base_row)
        st.dataframe(forecast_df)
        with st.expander("🔍 View Final Input Features for Forecasting"):
            st.dataframe(base_row[feature_cols].T)
