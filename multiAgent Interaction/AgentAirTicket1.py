import json
import re
import os
import subprocess
import sys

# Attempt to install python-dotenv if missing
try:
    import dotenv
    from dotenv import load_dotenv
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
        import dotenv
        from dotenv import load_dotenv
    except Exception as e:
        print(f"Error installing python-dotenv module: {e}")
        dotenv = None

# Ensure api_keys.env exists before loading
if dotenv and os.path.exists("api_keys.env"):
    load_dotenv("api_keys.env")
else:
    print("Warning: api_keys.env file not found or dotenv module is unavailable.")

# Retrieve API key from environment
TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
if not TOGETHER_AI_API_KEY:
    print("Warning: TOGETHER_AI_API_KEY is not set. AI functionality will be disabled.")

# Attempt to install Together AI module if missing
try:
    import together
    TOGETHER_AVAILABLE = True
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "together"])
        import together
        TOGETHER_AVAILABLE = True
    except Exception as e:
        print(f"Error installing together module: {e}")
        TOGETHER_AVAILABLE = False

if TOGETHER_AVAILABLE and TOGETHER_AI_API_KEY:
    # Initialize Together AI client
    client = together.Together(api_key=TOGETHER_AI_API_KEY)
else:
    client = None

MOCK_FLIGHT_DATA = {
    "AI123": {"flight_number": "AI123", "departure_time": "08:00 AM", "destination": "Delhi", "status": "Delayed"},
    "AI456": {"flight_number": "AI456", "departure_time": "02:30 PM", "destination": "Mumbai", "status": "On Time"},
    "AI789": {"flight_number": "AI789", "departure_time": "06:45 AM", "destination": "Chennai", "status": "Cancelled"},
    "AI101": {"flight_number": "AI101", "departure_time": "10:15 AM", "destination": "Bangalore", "status": "On Time"},
    "AI202": {"flight_number": "AI202", "departure_time": "01:00 PM", "destination": "Kolkata", "status": "Delayed"},
    "AI303": {"flight_number": "AI303", "departure_time": "03:45 PM", "destination": "Hyderabad", "status": "On Time"},
    "AI404": {"flight_number": "AI404", "departure_time": "06:00 PM", "destination": "Pune", "status": "Cancelled"},
    "AI505": {"flight_number": "AI505", "departure_time": "09:30 PM", "destination": "Ahmedabad", "status": "On Time"},
    "AI606": {"flight_number": "AI606", "departure_time": "11:45 PM", "destination": "Jaipur", "status": "Delayed"},
    "AI707": {"flight_number": "AI707", "departure_time": "05:30 AM", "destination": "Lucknow", "status": "On Time"},
}

def get_flight_info(flight_number: str) -> dict:
    """Simulates flight data retrieval."""
    return MOCK_FLIGHT_DATA.get(flight_number, {"error": "Flight not found"})

def info_agent_request(flight_number: str) -> str:
    """Info Agent: Fetches flight data and returns structured JSON."""
    flight_info = get_flight_info(flight_number)
    return json.dumps({"info_agent_response": flight_info})

def qa_agent_respond(user_query: str) -> str:
    """QA Agent: Extracts flight number, calls Info Agent, and refines response using Together AI."""
    match = re.search(r'Flight\s*(AI\d+)', user_query, re.IGNORECASE)
    if not match:
        return json.dumps({"answer": "Invalid query format. Please mention a flight number."})
    
    flight_number = match.group(1).upper()
    response = json.loads(info_agent_request(flight_number))
    flight_info = response.get("info_agent_response", {})
    
    if "error" in flight_info:
        return json.dumps({"answer": f"Flight {flight_number} not found in database."})
    
    if not TOGETHER_AVAILABLE or not TOGETHER_AI_API_KEY:
        return json.dumps({"answer": "AI functionality is disabled due to missing Together module or API key."})
    
    prompt = f"Provide a structured response for the user query in the format: 'Flight {flight_number} departs at {flight_info['departure_time']} to {flight_info['destination']}. Current status: {flight_info['status']}.'"
    try:
        ai_response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        formatted_answer = ai_response.choices[0].message.content.strip()
        return json.dumps({"answer": formatted_answer})
    except Exception as e:
        return json.dumps({"answer": f"Error communicating with Together AI: {str(e)}"})

if __name__ == "__main__":
    try:
        while True:
            print("Enter your flight query (or type 'exit' to quit):")
            user_query = input()
            if user_query.lower() == 'exit':
                print("Goodbye!")
                break
            print("Response:", qa_agent_respond(user_query))
            print("-" * 50)
    except ValueError:
        print("Error: Interactive input is not supported in this environment.")
