# 🌤️ Kerala Weather Forecasting ML Project

This project builds a machine learning-based weather forecasting system for Kerala using 85+ years of historical weather data fetched from the **Open-Meteo API**. The forecasts are visualized through an interactive **Streamlit dashboard**.

---

## 🚀 Project Overview

- **Goal**: Predict daily weather conditions (temperature, precipitation, and weather type) for Kerala using historical data.
- **Data Source**: [Open-Meteo API](https://open-meteo.com/)
- **Region**: Kerala, India
- **Predictions**:
  - `temperature_2m_mean` (°C)
  - `precipitation_sum` (mm)
  - `weather_code` (classification using weather description)

---

## 🧠 ML Models Used

- **RandomForestRegressor** for temperature and precipitation
- **RandomForestClassifier** for weather condition (weather code)
- **Feature Engineering**:
  - Lag features (e.g., past 1-3 days of key weather metrics)
  - Time-based features (month, season)
  - Weather code descriptions (not grouped)
  
---

## 📂 Project Structure

```
weather_forecasting_project/
│
├── fetch_data.py           # Fetches historical weather data via API
├── preprocess.py           # Preprocesses and feature engineers the dataset
├── train_model.py          # Trains ML models and saves them using joblib
├── predict.py              # Predicts next day’s weather using trained models
├── app.py                  # Streamlit dashboard for data viewing and forecasting
├── daily_scheduler.py      # Script using `schedule` library to automate daily updates
├── requirements.txt        # Project dependencies
├── preprocessed_weather.csv
├── model_temperature.pkl
├── model_precipitation.pkl
├── model_weather_code.pkl
└── README.md
```

---

## 🖥️ Streamlit Dashboard

You can view:
- **Today’s Forecast**
- Recent temperature and precipitation trend
- Predicted weather condition (with description)

Run the app:

```bash
streamlit run app.py
```
Check out the [Streamlit](https://weather-forecasting-model-2axjjdhdun8zamgnsckff5.streamlit.app/).

---

## 🗓️ Daily Updates

To automate daily model retraining and forecasting, this project uses the **`schedule`** Python library.

- `scheduler.py` runs the following scripts in order:
  1. `fetch_data.py`
  2. `preprocess.py`
  3. `train_model.py`
  4. `predict.py`


Run it manually with:

```bash
python scheduler.py
```

---

## 🛠️ Installation

Clone the project and install dependencies:

```bash
git clone https://github.com/your-username/kerala-weather-forecast.git
cd kerala-weather-forecast
pip install -r requirements.txt
```

---

## 📌 Note

- Ensure your internet connection is stable to fetch data from the API.
- No Supabase or external database is used.
- All data and models are stored and run **locally**.

---

## 🙌 Author

**Jango**  
Project built with ❤️ using Python, Streamlit, and Machine Learning.
