Flight Query Chatbot
📌 Overview
The Flight Query Chatbot is a Python-based chatbot that allows users to retrieve flight details from a mock database. It processes flight-related queries, extracts flight numbers, and provides structured responses. Additionally, it integrates Together AI to enhance responses using an AI model.

🚀 Features
✅ Flight Query Processing – Extracts flight numbers from user input using regex.
✅ Mock Database Lookup – Retrieves flight information from a predefined dataset.
✅ AI-Powered Response Formatting – Uses Together AI to enhance responses (if available).
✅ Automatic Dependency Handling – Installs missing packages automatically.
✅ Error Handling – Provides fallback responses if AI API is unavailable.

🛠️ Installation
1️⃣ Install Python (3.9 or later)
Ensure you have Python installed:



▶️ Usage
Run the Chatbot
Start the chatbot by executing:

python agent_system.py
Example Interaction

Enter your flight query (or type 'exit' to quit):
Flight AI123

Response: {"answer": "Flight AI123 is scheduled to depart at 08:00 AM to Delhi. Status: Delayed."}
--------------------------------------------------
Enter your flight query (or type 'exit' to quit):
exit
Goodbye!





