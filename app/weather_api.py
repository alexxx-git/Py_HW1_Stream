import requests

def get_current_temperature(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()

def is_temperature_normal(city, current_temperature, historical_data):
    season = historical_data.loc[historical_data['city'] == city, 'season'].iloc[-1]
    season_stats = historical_data.groupby('season')['temperature'].agg(['mean', 'std'])
    mean = season_stats.loc[season, 'mean']
    std = season_stats.loc[season, 'std']
    return abs(current_temperature - mean) <= 2 * std
