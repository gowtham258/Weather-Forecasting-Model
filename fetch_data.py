import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

def fetch_weather_data():

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
	    "latitude": 9.9399,
	    "longitude": 76.2602,
	    "start_date": "1940-12-31",
	    "end_date": "2025-04-11",
	    "daily": ["weather_code", "temperature_2m_mean", "daylight_duration", "sunshine_duration", "precipitation_sum",
                "wind_speed_10m_max", "temperature_2m_min", "cloud_cover_mean", "dew_point_2m_mean", 
                "apparent_temperature_mean", "apparent_temperature_max", "apparent_temperature_min", 
                "temperature_2m_max", "wind_gusts_10m_max", "dew_point_2m_max", "dew_point_2m_min",
                "cloud_cover_max", "cloud_cover_min", "relative_humidity_2m_mean", "relative_humidity_2m_max",
                "relative_humidity_2m_min", "pressure_msl_mean", "pressure_msl_max", "pressure_msl_min", "wind_speed_10m_mean", 
                "wind_gusts_10m_min", "wind_speed_10m_min", "wind_gusts_10m_mean", "surface_pressure_min", 
                "surface_pressure_max", "surface_pressure_mean"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_mean = daily.Variables(1).ValuesAsNumpy()
    daily_daylight_duration = daily.Variables(2).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(3).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(4).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(5).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(6).ValuesAsNumpy()
    daily_cloud_cover_mean = daily.Variables(7).ValuesAsNumpy()
    daily_dew_point_2m_mean = daily.Variables(8).ValuesAsNumpy()
    daily_apparent_temperature_mean = daily.Variables(9).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(10).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(11).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(12).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(13).ValuesAsNumpy()
    daily_dew_point_2m_max = daily.Variables(14).ValuesAsNumpy()
    daily_dew_point_2m_min = daily.Variables(15).ValuesAsNumpy()
    daily_cloud_cover_max = daily.Variables(16).ValuesAsNumpy()
    daily_cloud_cover_min = daily.Variables(17).ValuesAsNumpy()
    daily_relative_humidity_2m_mean = daily.Variables(18).ValuesAsNumpy()
    daily_relative_humidity_2m_max = daily.Variables(19).ValuesAsNumpy()
    daily_relative_humidity_2m_min = daily.Variables(20).ValuesAsNumpy()
    daily_pressure_msl_mean = daily.Variables(21).ValuesAsNumpy()
    daily_pressure_msl_max = daily.Variables(22).ValuesAsNumpy()
    daily_pressure_msl_min = daily.Variables(23).ValuesAsNumpy()
    daily_wind_speed_10m_mean = daily.Variables(24).ValuesAsNumpy()
    daily_wind_gusts_10m_min = daily.Variables(25).ValuesAsNumpy()
    daily_wind_speed_10m_min = daily.Variables(26).ValuesAsNumpy()
    daily_wind_gusts_10m_mean = daily.Variables(27).ValuesAsNumpy()
    daily_surface_pressure_min = daily.Variables(28).ValuesAsNumpy()
    daily_surface_pressure_max = daily.Variables(29).ValuesAsNumpy()
    daily_surface_pressure_mean = daily.Variables(30).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
	    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	    freq = pd.Timedelta(seconds = daily.Interval()),
	    inclusive = "left"
    )}

    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
    daily_data["daylight_duration"] = daily_daylight_duration
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["cloud_cover_mean"] = daily_cloud_cover_mean
    daily_data["dew_point_2m_mean"] = daily_dew_point_2m_mean
    daily_data["apparent_temperature_mean"] = daily_apparent_temperature_mean
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
    daily_data["dew_point_2m_max"] = daily_dew_point_2m_max
    daily_data["dew_point_2m_min"] = daily_dew_point_2m_min
    daily_data["cloud_cover_max"] = daily_cloud_cover_max
    daily_data["cloud_cover_min"] = daily_cloud_cover_min
    daily_data["relative_humidity_2m_mean"] = daily_relative_humidity_2m_mean
    daily_data["relative_humidity_2m_max"] = daily_relative_humidity_2m_max
    daily_data["relative_humidity_2m_min"] = daily_relative_humidity_2m_min
    daily_data["pressure_msl_mean"] = daily_pressure_msl_mean
    daily_data["pressure_msl_max"] = daily_pressure_msl_max
    daily_data["pressure_msl_min"] = daily_pressure_msl_min
    daily_data["wind_speed_10m_mean"] = daily_wind_speed_10m_mean
    daily_data["wind_gusts_10m_min"] = daily_wind_gusts_10m_min
    daily_data["wind_speed_10m_min"] = daily_wind_speed_10m_min
    daily_data["wind_gusts_10m_mean"] = daily_wind_gusts_10m_mean
    daily_data["surface_pressure_min"] = daily_surface_pressure_min
    daily_data["surface_pressure_max"] = daily_surface_pressure_max
    daily_data["surface_pressure_mean"] = daily_surface_pressure_mean

    daily_dataframe = pd.DataFrame(data = daily_data)

    daily_dataframe.to_csv("historical_weather_daily.csv", index = False)
    print("✅ Weather data fetched and saved to 'historical_weather_daily.csv'")

if __name__ == "__main__":
    fetch_weather_data()