import pandas as pd
import numpy as np
from multiprocessing import Pool

def process_chunk(chunk):
    # Пример обработки части данных: вычисление среднего и стандартного отклонения
    return chunk.groupby('season')['temperature'].agg(['mean', 'std'])


def parallel_analysis(data, num_chunks=4):
    chunks = np.array_split(data, num_chunks)
    pool = Pool(processes=num_chunks)
    result = pool.map(process_chunk, chunks)
    pool.close()
    pool.join()
    return pd.concat(result)

def detect_anomalies(city_data, season_stats):
    anomalies = []
    for _, row in city_data.iterrows():
        season = row['season']
        mean = season_stats.loc[season, 'mean']
        std = season_stats.loc[season, 'std']
        if abs(row['temperature'] - mean) > 2 * std:
            anomalies.append(row)
    return pd.DataFrame(anomalies)

def calculate_moving_average(data, window=30):
    data['moving_average'] = data['temperature'].rolling(window=window).mean()
    return data

def seasonal_statistics(city_data):
    return city_data.groupby('season')['temperature'].agg(['mean', 'std'])
