import requests


def get_current_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 401:
        return None, "Invalid API key"
    elif response.status_code == 200:
        return data['main']['temp'], None
    else:
        return None, data.get('message', 'Unknown error')
