import os
import requests

def get_forecast(location):
    """Fetches the daily forecast for the specified location."""
    
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {"error": "WEATHER_API_KEY not found in environment variables."}

    # We call the forecast endpoint (days=1 gets today's forecast)
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1&aqi=no&alerts=no"

    try:
        response = requests.get(url)
        response.raise_for_status() # Raises an error for bad status codes
        data = response.json()
        # Extract just the useful bits for the LLM
        forecast = data['forecast']['forecastday'][0]['day']
        
        parsed_weather = {
            "conditions": forecast['condition']['text'],
            "temp_high": f"{forecast['maxtemp_f']}°F",
            "temp_low": f"{forecast['mintemp_f']}°F",
            "chance_of_rain": f"{forecast['daily_chance_of_rain']}%",
            "max_wind": f"{forecast['maxwind_mph']} mph"
        }
        return parsed_weather

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather: {e}"}