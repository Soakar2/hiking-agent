import time

from google import genai

def get_trail_recommendation(trails, weather, preferences):
    """Passes the world state to Gemini to get a recommendation."""
    
    # Initialize the new Client. 
    # It automatically finds GEMINI_API_KEY from your environment variables!
    try:
        client = genai.Client()
    except Exception as e:
         return f"Error initializing client. Is GEMINI_API_KEY set? Details: {e}"

    # Construct the prompt
    prompt = f"""
    You are an expert outdoor guide and personalized hiking assistant. Your job is to analyze 
    a provided list of trails, the current regional weather forecasts, and the user's preferred 
    difficulty level to recommend the absolute best trail for them to hike today.

    Rules:
Rules:
    1. Never recommend a trail if the weather conditions in its specific location are dangerous.
    2. Always try to match the difficulty level requested by the user.
    3. YOU MUST FILL IN THE BRACKETED PLACEHOLDERS in the HTML template below with the actual data and your generated advice. 
    4. For the "Navigate to Trailhead" button, take the text from the 'location' field of the winning trail, format it for a URL (replace spaces with +), and insert it at the end of the Google Maps search link.

    Here is the data for today's hike:
    
    User Preferences:
    - Desired Difficulty: {preferences.get('difficulty')}
    - Max Elevation Gain: {preferences.get('max_elevation_gain')} feet
    
    Regional Weather Forecasts:
    {weather}
    
    Available Trails Data:
    {trails}
    
    Based on this data, please recommend the single best trail for today.
    
    Output Format:
    Return ONLY valid HTML code. Do not use markdown backticks around your response. 
    Format the email using this exact template, replacing everything in brackets with your actual analysis:

    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
        <div style="background-color: #2E7D32; color: white; padding: 20px; text-align: center;">
            <h2 style="margin: 0;">🏔️ Today's Trail: [Insert Trail Name Here]</h2>
        </div>
        
        <div style="padding: 20px; color: #333; line-height: 1.6;">
            <div style="background-color: #f1f8e9; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 14px;">
                <h4 style="margin-top: 0; color: #2E7D32;">🌤️ Trail Conditions</h4>
                <ul style="list-style-type: none; padding: 0; margin: 0;">
                    <li><strong>🌡️ Temps:</strong> High of [Insert High Temp] | Low of [Insert Low Temp]</li>
                    <li><strong>💧 Rain Chance:</strong> [Insert Rain Chance] | <strong>💦 Humidity:</strong> [Insert Humidity]</li>
                    <li><strong>🌬️ Wind:</strong> [Insert Wind Speed] | <strong>☀️ UV Index:</strong> [Insert UV Index]</li>
                    <li><strong>🌅 Sunrise:</strong> [Insert Sunrise] | <strong>🌇 Sunset:</strong> [Insert Sunset]</li>
                </ul>
            </div>

            <h3 style="color: #2E7D32; border-bottom: 2px solid #eee; padding-bottom: 5px;">🥾 Why this trail today?</h3>
            <p>[Insert your explanation of why it fits the difficulty, how the elevation gain fits the user's max limit, and cross-reference specific weather stats]</p>

            <h3 style="color: #2E7D32; border-bottom: 2px solid #eee; padding-bottom: 5px;">🦵 Leg Endurance Factor</h3>
            <p>[Insert a 1-10 score on how well this specific trail builds leg strength based on its elevation gain, and briefly explain why]</p>
            
            <h3 style="color: #2E7D32; border-bottom: 2px solid #eee; padding-bottom: 5px;">🎒 Weather & Gear Prep</h3>
            <p>[Insert specific gear or timing advice based strictly on today's expanded forecast metrics]</p>

            <div style="text-align: center; margin-top: 30px; margin-bottom: 10px;">
                <a href="https://www.google.com/maps/search/?api=1&query=[Insert 'location' text here, replacing spaces with +]" style="background-color: #2E7D32; color: white; padding: 14px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block; font-size: 16px;">🗺️ Navigate to Trailhead</a>
            </div>
        </div>
    </div>
    """

# --- THE RETRY LOGIC ---
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
            
        except Exception as e:
            # If it's a 503 traffic jam and we have retries left
            if '503' in str(e) or 'UNAVAILABLE' in str(e):
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Waits 1s, then 2s...
                    print(f"Gemini servers busy. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue # Try the loop again
                    
            # If it's a different error, or we ran out of retries, fail gracefully
            print(f"Error communicating with Gemini after {attempt + 1} attempts: {e}")
            return None # <--- Return None instead of the error string!