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

1. **User Input Handling Node**  
   Captures the user’s query and determines intent (chat, plan creation, or event search).

2. **Exercise Plan Node**  
   Generates a personalized exercise plan based on user input and stores it in the agent state.

3. **Nearby Event Node**  
   - Extracts structured information from user queries (game type, location, skill level).  
   - Searches for matching events.  
   - Presents options to the user and stores them in the agent state.

4. **Book Event Node**  
   Processes the user’s event selection, confirms the booking, and updates the agent state with a booking confirmation.

The workflow ensures smooth transitions between general chat, personalized plan creation, and event booking.

---

## 4. Getting Started
