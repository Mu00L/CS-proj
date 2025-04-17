import requests

# Hardcoding the API key for simplicity in this project.
# For better security in production, store this in a secrets file or an environment variable.
API_KEY = "4901baf270cf624a710273a0ee3f91ce"

def get_city_coordinates(city):
    """
    Convert a city name to geographic coordinates (latitude and longitude)
    using the OpenWeatherMap Geocoding API.
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    return None, None

def get_current_weather(lat, lon):
    """
    Fetch current weather and forecast data using the OpenWeatherMap One Call API.
    """
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def get_current_weather(lat, lon):
    """
    Fetch current weather and forecast data using the OpenWeatherMap One Call API.
    """
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_historical_weather(lat, lon, dt):
    """
    Fetch historical weather data using the Time Machine endpoint.
    dt should be a Unix timestamp.
    """
    url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_daily_summary(lat, lon, date):
    """
    Fetch historical daily aggregation data.
    The date parameter should be in the format YYYY-MM-DD.
    """
    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_weather_overview(lat, lon):
    """
    Fetch a human-readable weather overview.
    """
    url = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
