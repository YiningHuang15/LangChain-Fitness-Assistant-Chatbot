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
   - Determines the user’s intent from their query.  
   - Routes to the appropriate node based on the detected intent.

2. **General_Chat_Node**  
   - Handles casual conversation about fitness, workouts, and healthy habits.  
   - Ends the workflow after responding.

3. **Exercise_Plan_Node**  
   - Generates a personalized exercise plan tailored to the user’s fitness goals.  
   - Ends the workflow after providing the plan.

4. **Nearby_Event_Node**  
   - Extracts structured information (game type, location, level) from the user’s query.  
   - Searches for matching local sports events.  
   - Routes to **Book_Nearby_Event_Node** if events are found, or **Alternative_Approach_Node** if no matches exist.

5. **Book_Nearby_Event_Node**  
   - Confirms the booking for the selected event.  
   - Updates the agent state with a booking confirmation.  
   - Ends the workflow.

6. **Alternative_Approach_Node**  
   - Handles cases where no events are found or other fallback scenarios.  
   - Ends the workflow.

The workflow ensures smooth transitions between general chat, personalized plan creation, and event booking.

---

## 4. Getting Started
