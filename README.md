AI Hiking Agent 🥾
An intelligent, data-driven decision agent that automates the process of selecting the perfect hiking trail based on real-time atmospheric conditions, geospatial data, and personalized user constraints.

🚀 Overview
The AI Hiking Agent eliminates "decision fatigue" for outdoor enthusiasts. By synthesizing unstructured trail data with live weather telemetry, the agent uses a Large Language Model (LLM) to recommend the optimal trail for any given day.

Originally built with a manual trail registry, the system is being evolved into a fully automated pipeline that fetches data via the Overpass API (OpenStreetMap) and serves recommendations through a Streamlit web interface.

✨ Key Features
Automated Weather Synthesis: Integrates with weather APIs to analyze temperature, precipitation probability, and wind speeds for specific trailhead coordinates.

Geospatial Data Integration: Programmatically retrieves local trail metadata (difficulty, length, elevation gain) using OpenStreetMap.

LLM-Powered Reasoning: Leverages the Google Gemini API to process multi-variable constraints (e.g., "Find a trail under 5 miles that won't be muddy after yesterday's rain").

Dynamic Filtering: Sorts and selects hikes based on a weighted preference system, ensuring recommendations align with the user's fitness goals and schedule.

🛠️ Tech Stack
Language: Python 3.12

AI/ML: Google Gemini API (LLM Orchestration)

Data Sources: OpenStreetMap (Overpass API), OpenWeatherMap API

Interface: Streamlit (in-development)

Version Control: Git (Feature-branch workflow)

📂 Project Structure
Plaintext
├── src/
│   ├── agent.py              # Core logic for the AI decision engine
│   ├── weather.py            # ETL pipeline for OSM and Weather data
│   └── email.py              # Emailer for the the response
├── data/
│   └── trails.json           # Cached geospatial trail data
├── Subscriber/
│   └── email_subscriber.py   # Cached geospatial trail data
├── requirements.txt          # Project dependencies
├── main.py                   # Main 
└── README.md
⚙️ Installation & Setup
Clone the Repository:

Bash
git clone https://github.com/Soakar23/ai-hiking-agent.git
cd ai-hiking-agent
Install Dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file and add your API keys:

Code snippet
GEMINI_API_KEY=GET YOUR OWN KEY!!!!!!!!!!
WEATHER_API_KEY=GET YOUR OWN KEY!!!!!!!!!!
Run the Agent:

Bash
python src/agent.py
🗺️ Roadmap
[ ] Automated Population: Finalize the script to auto-generate the trail list based on an X-mile radius of Decatur, AL.

[ ] Vector Search: Implement a vector database (FAISS) to allow for semantic searching of trail descriptions.

[ ] UI Deployment: Deploy the Streamlit interface to a cloud environment for mobile access.

Developed by Daniel Harrison – Software Engineer & Outdoor Enthusiast.