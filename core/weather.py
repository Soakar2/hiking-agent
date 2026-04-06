import os
import requests

def get_forecast(location):
    """Fetches the expanded daily forecast for the specified location."""
    
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {"error": "WEATHER_API_KEY not found in environment variables."}

    # Notice we changed aqi=yes to grab Air Quality Index as well!
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1&aqi=yes&alerts=no"

    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        current = data['current']
        forecast = data['forecast']['forecastday'][0]['day']
        astro = data['forecast']['forecastday'][0]['astro']
        
        parsed_weather = {
            "conditions": forecast['condition']['text'],
            "temp_high": f"{forecast['maxtemp_f']}°F",
            "temp_low": f"{forecast['mintemp_f']}°F",
            "feels_like": f"{current['feelslike_f']}°F",
            "chance_of_rain": f"{forecast['daily_chance_of_rain']}%",
            "max_wind": f"{forecast['maxwind_mph']} mph",
            "uv_index": forecast['uv'],
            "humidity": f"{current['humidity']}%",
            "sunrise": astro['sunrise'],
            "sunset": astro['sunset']
        }
        return parsed_weather

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather: {e}"}