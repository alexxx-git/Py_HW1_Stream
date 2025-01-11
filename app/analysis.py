import pandas as pd
import numpy as np
from multiprocessing import Pool

def calculate_moving_average(data, window=30):
    return data['temperature'].rolling(window=window).mean()

def calculate_seasonal_statistics(data):
    seasonal_stats = data.groupby('season')['temperature'].agg(['mean', 'std'])
    return seasonal_stats

def detect_anomalies(data, season_stats):
    anomalies = []
    for _, row in data.iterrows():
        season = row['season']
        mean = season_stats.loc[season, 'mean']
        std = season_stats.loc[season, 'std']
        if row['temperature'] < mean - 2 * std or row['temperature'] > mean + 2 * std:
            anomalies.append(row)
    return anomalies

def parallel_analysis(data):
    pool = Pool()
    chunks = np.array_split(data, 4)  # Разбиение данных на 4 части
    result = pool.map(process_chunk, chunks)
    pool.close()
    pool.join()
    return result
