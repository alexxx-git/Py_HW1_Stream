import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app.analysis import calculate_moving_average, calculate_seasonal_statistics, detect_anomalies
from app.weather_api import get_current_weather

# Загрузка данных
def load_data(file):
    return pd.read_csv(file, parse_dates=['timestamp'])

# Формы ввода
api_key = st.text_input("Введите API-ключ для OpenWeatherMap")

# Выбор города
city = st.selectbox("Выберите город", ["New York", "London", "Berlin"])

# Загрузка и анализ исторических данных
data = load_data('data/temperature_data.csv')
seasonal_stats = calculate_seasonal_statistics(data)
moving_avg = calculate_moving_average(data)

# Детекция аномалий
anomalies = detect_anomalies(data, seasonal_stats)

# Визуализация
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(data['timestamp'], data['temperature'], label='Temperature')
ax.scatter(anomalies['timestamp'], anomalies['temperature'], color='red', label='Anomalies')
st.pyplot(fig)

# Получение текущей температуры
if api_key:
    temp, error = get_current_weather(city, api_key)
    if temp is not None:
        st.write(f"Текущая температура в {city}: {temp}°C")
        # Сравнение с историческими данными
        season = data[data['city'] == city].iloc[0]['season']
        season_mean = seasonal_stats.loc[season, 'mean']
        season_std = seasonal_stats.loc[season, 'std']
        if abs(temp - season_mean) > 2 * season_std:
            st.write("Температура аномальна для этого сезона!")
        else:
            st.write("Температура в пределах нормы.")
    else:
        st.error(error)
