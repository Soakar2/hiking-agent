import os
import json
from dotenv import load_dotenv
from core.weather import get_forecast  # Assuming you made this file!
from core.agent import get_trail_recommendation
from core.email import send_recommendation_email  # Assuming you made this file!
def load_trails(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data.get("trails", [])
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}")
        return []

def main():
    load_dotenv()
    
    # 1. Load Trails
    trails = load_trails('trails.json')
    
    # 2. Extract unique locations and fetch weather
    print("Fetching weather data...")
    unique_locations = set(trail.get("location") for trail in trails if trail.get("location"))
    
    regional_weather = {}
    for location in unique_locations:
        # Assuming get_forecast returns a dictionary of weather stats
        regional_weather[location] = get_forecast(location) 
        print(f"Got weather for {location}")

    # 3. User Preferences (We can hardcode this or move it to a config file later)
    preferences = {
        "difficulty": "Moderate",
        "max_drive_mins": 60
    }
    
    print("-" * 20 + "\nAgent is thinking...")
    
    # 4. Pass the combined context to the agent
    recommendation = get_trail_recommendation(trails, regional_weather, preferences)
    
# --- THE NEW SAFETY CHECK ---
    if recommendation:
        print("\n" + recommendation)
        
        # 5. Send the email!
        print("-" * 20 + "\nSending email...")
        send_recommendation_email(recommendation)
    else:
        # If recommendation is None, the script will just quietly end here!
        print("\nAgent failed to generate a recommendation. Aborting email.")

if __name__ == "__main__":
    main()