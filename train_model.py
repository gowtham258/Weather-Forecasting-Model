# train_models.py

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

def train_models():
    df = pd.read_csv("preprocessed_weather.csv")

    # Drop NA (in case)
    df.dropna(inplace=True)

    # Input features
    feature_cols = [col for col in df.columns if ("lag" in col and "description" not in col)] 
    X = df[feature_cols]

    # Targets
    y_temp = df["temperature_2m_mean"]
    y_precip = df["precipitation_sum"]
    y_weather_code = df["weather_code"]

    # Train-test split
    X_train, X_test, y_temp_train, y_temp_test = train_test_split(X, y_temp, test_size=0.2, random_state=42)
    _, _, y_precip_train, y_precip_test = train_test_split(X, y_precip, test_size=0.2, random_state=42)
    _, _, y_code_train, y_code_test = train_test_split(X, y_weather_code, test_size=0.2, random_state=42)

    # 1. Temperature Model
    model_temp = RandomForestRegressor(random_state=42)
    model_temp.fit(X_train, y_temp_train)
    preds_temp = model_temp.predict(X_test)
    temp_rmse = mean_squared_error(y_temp_test, preds_temp) ** 0.5
    print(f"🌡️ Temperature RMSE: {temp_rmse:.2f}")

    # 2. Precipitation Model
    model_precip = RandomForestRegressor(random_state=42)
    model_precip.fit(X_train, y_precip_train)
    preds_precip = model_precip.predict(X_test)
    precip_rmse = mean_squared_error(y_precip_test, preds_precip) ** 0.5
    print(f"🌧️ Precipitation RMSE: {precip_rmse:.2f}")

    # 3. Weather Code Classifier (with class weights)
    class_weights = compute_class_weight(class_weight="balanced", classes=np.unique(y_code_train), y=y_code_train)
    weights_dict = {cls: w for cls, w in zip(np.unique(y_code_train), class_weights)}

    model_code = RandomForestClassifier(random_state=42, class_weight=weights_dict)
    model_code.fit(X_train, y_code_train)
    preds_code = model_code.predict(X_test)
    print(f"⛅ Weather Code Accuracy: {accuracy_score(y_code_test, preds_code) * 100:.2f}%")

    # Save
    joblib.dump(model_temp, "model_temperature.pkl")
    joblib.dump(model_precip, "model_precipitation.pkl")
    joblib.dump(model_code, "model_weather_code.pkl")
    joblib.dump(X.columns.tolist(), "features.pkl")

    print("✅ All models trained and saved successfully.")

if __name__ == "__main__":
    train_models()
