import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Загрузка данных
# Предположим, что у вас есть CSV-файл с двумя столбцами: 'Date' и 'Temperature'
data = pd.read_csv('data/temperature_data.csv', parse_dates=['timestamp'], index_col='timestamp')
# Параметр окна для скользящего среднего и стандартного отклонения (например, 30 дней)
window_size = 30

# Вычисление скользящего среднего и стандартного отклонения
data['Rolling_Mean'] = data['temperature'].rolling(window=30).mean()
data['Rolling_Std'] = data['temperature'].rolling(window=30).std()

# Определение порогов для аномалий
data['Upper_Bound'] = data['Rolling_Mean'] + 2 * data['Rolling_Std']
data['Lower_Bound'] = data['Rolling_Mean'] - 2 * data['Rolling_Std']
data['Anomaly'] = (data['temperature'] > data['Upper_Bound']) | (data['temperature'] < data['Lower_Bound'])

# Использование скользящего среднего с большим окном (например, 365 дней)
long_term_window = 365
data['Long_Term_Trend'] = data['temperature'].rolling(window=long_term_window).mean()

plt.figure(figsize=(15, 10))

# График температуры
plt.plot(data.index, data['temperature'], label='temperature', color='blue', alpha=0.5)

# График скользящего среднего
plt.plot(data.index, data['Rolling_Mean'], label=f'Rolling Mean ({window_size} days)', color='orange')

# График границ для аномалий
plt.plot(data.index, data['Upper_Bound'], label='Upper Bound (+2σ)', color='red', linestyle='--')
plt.plot(data.index, data['Lower_Bound'], label='Lower Bound (-2σ)', color='red', linestyle='--')

# График долгосрочного тренда
plt.plot(data.index, data['Long_Term_Trend'], label=f'Long Term Trend ({long_term_window} days)', color='green')

# Выделение аномалий
plt.scatter(data.index[data['Anomaly']], data['temperature'][data['Anomaly']], color='red', label='Anomalies', s=50)

plt.title('Temperature Time Series Analysis')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.legend()
plt.show()


# Выбор города (например, 'New York')
city_name = 'New York'

# Фильтрация данных для выбранного города
city_data = data[data['city'] == city_name]

# Построение графика температуры для выбранного города
plt.figure(figsize=(15, 6))
plt.plot(city_data.index, city_data['temperature'], label=f'Temperature in {city_name}', color='blue')
plt.title(f'Temperature Over Time in {city_name}')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.legend()
plt.show()