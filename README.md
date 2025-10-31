# AI Fitness Assistant Chatbot
*Plan Smarter. Play Together*

## 1. Project Overview & Description
The **AI Fitness Assistant Chatbot** is an intelligent virtual assistant designed to help users with their fitness and workout goals. Powered by OpenAI chatgpt and built using LangChain, the chatbot provides three core functionalities:

1. **General Fitness/Workout Chat**  
   Users can engage in casual conversation about fitness, exercise tips, and healthy habits.

2. **Personalized Exercise Plan Design**  
   The chatbot can generate a customized exercise plan tailored to a user’s goals, preferences, and fitness level.

3. **Find and Book Nearby Sports Events**  
   Users can search for nearby sports events based on the game type, location, and skill level. The chatbot can automatically identify matching events and confirm bookings for the user.

This AI agent provides a seamless experience combining conversational interaction, personalized recommendations, and automated event booking.


## 2. Programming Languages & Tools
The project is built using the following technologies:

- **Python** – Core programming language for building the AI agent.
- **LangChain** – Framework for constructing the AI agent and orchestrating workflows.
- **LangGraph** – Used to define the nodes and workflow for different chatbot functionalities.
- **Streamlit** – Web interface for interacting with the chatbot and displaying event tables, personalized plans, and booking confirmations.


## 3. LangGraph Workflow
The chatbot's LangGraph workflow consists of multiple nodes that handle different tasks:
![LangGraph Workflow](https://github.com/YiningHuang15/LangChain-Fitness-Assistant-Chatbot/blob/main/langgraph-workflow.png)

1. **Intent_Node**  
   - Determines the user’s intent from their query (General Chat, Exercise Plan, or Nearby Events) and routes to the appropriate node.

2. **General_Chat_Node**  
   - Handles casual conversation about fitness, workouts, and healthy habits.

3. **Exercise_Plan_Node**  
   - Generates a personalized exercise plan based on the user’s goals and preferences.

4. **Nearby_Event_Node**  
   - Extracts structured information from user queries (game type, location, skill level).  
   - Searches for matching local sports events and routes to the appropriate next node.

5. **Book_Nearby_Event_Node**  
   - Confirms the booking for the selected event and updates the agent state with a confirmation.

6. **Alternative_Approach_Node**  
   - Handles cases where no events are found or other fallback scenarios.

The workflow ensures smooth transitions between general chat, personalized plan creation, and event booking.


## 4. Getting Started

#### Prerequisites
- Python 3.9 or higher
- Install required packages in the requirements.txt

#### Clone the repository:
```
git clone https://github.com/YiningHuang15/LangChain-Fitness-Assistant-Chatbot
cd ai-fitness-chatbot
```

#### Start the Streamlit app:
```
streamlit run 💬AI_Fitness_Chatbot.py
```

#### Interact with the AI Fitness Assistant Chatbot:
1. Ask general fitness questions. e.g. "What is hatha yoga?"
2. Generate personalized workout plans. e.g. "Suggest an exercise plan for training core in the gym for 30 minutes"
3. Search and book nearby sports events automatically. e.g. "Find and book a beginner tennis meetup near Menlo Park 94025"

#### Notes
Ensure you have valid API credentials for any LLMs used (e.g., OpenAI API key).
Event search functionality currently uses demo or static data; it can be extended to real event APIs.
