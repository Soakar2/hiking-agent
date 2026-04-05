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
    # Construct the prompt
    prompt = f"""
    You are an expert outdoor guide and personalized hiking assistant. Your job is to analyze 
    a provided list of trails, the current regional weather forecasts, and the user's preferred 
    difficulty level to recommend the absolute best trail for them to hike today.

    Rules:
    1. Never recommend a trail if the weather conditions in its specific location are dangerous.
    2. Always try to match the difficulty level requested by the user.
    3. Format your response exactly as requested.

    Here is the data for today's hike:
    
    User Preferences:
    - Desired Difficulty: {preferences['difficulty']}
    - Max Drive Time: {preferences['max_drive_mins']} minutes
    
    Regional Weather Forecasts:
    {weather}
    
    Available Trails Data:
    {trails}
    
    Based on this data, please recommend the single best trail for today.
    
    Output Format:
    ### Recommended Trail: [Name]
    **Why this trail today:** [Explain why it fits the difficulty and the specific weather for its location]
    **Weather Prep:** [Specific gear or timing advice]
    """

    try:
        # We are using gemini-2.5-pro since you are on the Pro trial!
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {e}"