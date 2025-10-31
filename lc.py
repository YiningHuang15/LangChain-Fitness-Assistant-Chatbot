#!/usr/bin/env python
# coding: utf-8

# ## Your AI Fitness Chatbot
# ### Plan smarter. Play together.

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")


from prompts import INTENT_DETECTION_SYSTEM_PROMPT, EXERCISE_PLANNING_SYSTEM_PROMPT, ALTERNATIVE_APPROACH_SYSTEM_PROMPT
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json
import pandas as pd
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
import logging
import graphviz
import re
from langgraph.types import interrupt, Command


logging.getLogger("httpx").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)


class FitnessAgentState(TypedDict):
    user_input: str
    intent: Optional[str]
    exercise_plan: Optional[dict]
    matched_event: Optional[dict]
    booking_confirmation: Optional[str]
    assistant_reply: Optional[str]



def detect_intent(user_query: str, model_name: str = "gpt-4o-mini", temperature: float = 0.3) -> str:
    """
    Detent the user query into one of the defined intents:
    GeneralChat, ExercisePlan, NearbyEvents, Fallback, or Other.
    
    Returns:
        str: The detected intent label.
    """
    prompt = ChatPromptTemplate.from_messages([
    ("system", INTENT_DETECTION_SYSTEM_PROMPT),
    ("human", "{user_query}")
    ])
    
    messages = prompt.format_messages(user_query=user_query)
    
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    
    response = llm.invoke(messages)
    
    intent = json.loads(response.content)["intent"]
    
    return intent

def Intent_Node(state: FitnessAgentState) -> FitnessAgentState:
    """
    LangGraph node that determines user intent using detect_intent().
    """
    user_query = state["user_input"]
    detected_intent = detect_intent(user_query)
    return {"intent": detected_intent}

def get_general_chat(user_query: str, model_name: str = "gpt-4o-mini", temperature: float = 0.3):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a friendly AI fitness coach. Answer general fitness and health questions."),
        ("human", "{user_query}")
    ])
    llm = ChatOpenAI(model=model_name, temperature=temperature)

    messages = prompt.format_messages(user_query=user_query)

    response = llm.invoke(messages)

    return response


def General_Chat_Node(state: FitnessAgentState) -> FitnessAgentState:
    """
    Node for handling general chat or casual fitness conversation.
    """
    user_query = state["user_input"]
    
    response = get_general_chat(user_query)
    
    assistant_reply = response.content.strip()
    
    return {"assistant_reply": assistant_reply}


class ExerciseItem(BaseModel):
    """Defines one workout exercise."""
    exercise: str = Field(description="Name of the exercise")
    setsxreps: str = Field(description="Number of sets and reps, e.g., '3 x 15'")
    focus: str = Field(description="Muscle group or area targeted")
    notes: str = Field(description="Form tips or execution notes")

class WorkoutPlan(BaseModel):
    """Structured output for a workout plan."""
    title: str = Field(description="Title of the workout section")
    exercises: List[ExerciseItem] = Field(description="List of exercises in this workout circuit")


def get_exercise_plan(user_query: str, model_name: str = "gpt-4o-mini", temperature: float = 0.3):
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXERCISE_PLANNING_SYSTEM_PROMPT),
        ("human", "{user_query}")
    ])

    messages = prompt.format_messages(user_query=user_query)

    llm = ChatOpenAI(model=model_name, temperature=temperature).with_structured_output(WorkoutPlan)
    
    response = llm.invoke(messages)
    return response


def Exercise_Plan_Node(state: FitnessAgentState) -> FitnessAgentState:
    """
    LangGraph node for generating a personalized exercise plan.
    """
    user_query = state["user_input"]
    
    response = get_exercise_plan(user_query)
    
    return {"exercise_plan": response}


def find_matching_event(sport, city, zip_cd, level):
    df = pd.read_csv("nearby_events.csv")   
    filtered = df[(df['game_type'] == sport) & (df['game_city'] == city) & (df["game_zip_code"] == zip_cd) & 
                  ((df['game_level'] == level) | (df['game_level'] == 'all')  )]
    if filtered.empty:
        return None
    
    return filtered




def parse_event_keyword(user_query: str, model_name: str = "gpt-4o-mini", temperature: float = 0):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that extracts structured information from user queries."),
        ("human", "Extract sports_name, city, and zip_code and level from this query: '{user_query}' in JSON format.")
    ])

    llm = ChatOpenAI(model=model_name, temperature=temperature)

    messages = prompt.format_messages(user_query=user_query)

    response = llm.invoke(messages)

    return response




def Nearby_Event_Node(state: FitnessAgentState) -> FitnessAgentState:
    """
    LangGraph node to return a static matched event for demo purposes.
    """
    print("Nearby_Event_Node invoked.")

    user_query = state["user_input"]

    print(f"user_query is {user_query}")
    
    parse_response = parse_event_keyword(user_query).content
    cleaned = re.sub(r"```(?:json)?", "", parse_response).strip()

    print(f"parse_response is {cleaned}")

    matched_event = None
    try:
        print("Attempting to parse JSON from LLM response...")
        parsed_json = json.loads(cleaned)  
        sports_name = parsed_json.get("sports_name")
        city = parsed_json.get("city")
        zip_cd = int(parsed_json.get("zip_code"))
        level = parsed_json.get("level")

        matched_event = find_matching_event(sports_name, city, zip_cd, level)
        print(f"Matched event: {matched_event}")
    
    except Exception:
        matched_event = None
        print("something is wrong in the parsing process and matched_event assignement")
    
    if matched_event is None:
        print("No matching event found for testing.")

    event_list = matched_event.to_dict(orient="records")

    # Build a friendly list for the user
    event_summary = "\n".join([
        f"{i+1}. {row['game_type']} - {row['game_date']} at {row['game_time']} in {row['game_location']} ({row['game_level']})"
        for i, row in enumerate(event_list)
    ])
    question = f"I found the following events from meetup:\n\n{event_summary}\n\nWhich one would you like to book? (Please enter the number.)"

    state['assistant_reply'] = question
    state['matched_event'] = event_list

    print("📍 Nearby_Event_Node executed")

    return state


def Book_Nearby_Event_Node(state: FitnessAgentState) -> FitnessAgentState:
    """
    LangGraph node to return a static booking confirmation for demo purposes.
    """
    print("Book_Nearby_Event_Node invoked.")

    events = state.get("matched_event", [])
    print(f"the matching events are {events}")
    
    try:
        choice = 0
        print(f"user selected choice index: {choice}")
        event = events[choice]
        
        print(f"the selected event is {event}")
        
    except (IndexError, ValueError):
        state["assitant_reply"] = "Sorry, I couldn’t understand your selection. Please reply with a valid number."
        state["booking_confirmation"] = None
        print(f"something is wrong in the event selection process")
        return state

    booking_confirmation = (
        f"✅ Your {event['game_type']} event on {event['game_date']} "
        f"at {event['game_time']} in {event['game_location']} is booked!"
    )
    print(f"booking_confirmation message is {booking_confirmation}")
    
    # Explicitly assign it to the state
    state["booking_confirmation"] = booking_confirmation
    state["assistant_reply"] = booking_confirmation
    
    print("📍 Book_Nearby_Event_Node executed")
    
    return state



def Alternative_Approach_Node(state: FitnessAgentState) -> FitnessAgentState:
    """
    Node that uses a system prompt to provide alternative guidance when no matching event is found.
    Updates:
        - assistant_reply: string with ChatGPT-generated suggestions
    """
    user_query = state["user_input"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", ALTERNATIVE_APPROACH_SYSTEM_PROMPT),
        ("human", "{user_query}")
    ])

    messages = prompt.format_messages(user_query=user_query)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)
    response = llm.invoke(messages)

    assistant_reply = response.content.strip()
    return {"assistant_reply": assistant_reply}




# test run
workflow = StateGraph(FitnessAgentState)
workflow.add_node("Intent_Node", Intent_Node)
workflow.add_node("General_Chat_Node", General_Chat_Node)
workflow.add_node("Exercise_Plan_Node", Exercise_Plan_Node)
workflow.add_node("Nearby_Event_Node", Nearby_Event_Node)
workflow.add_node("Book_Nearby_Event_Node", Book_Nearby_Event_Node)
workflow.add_node("Alternative_Approach_Node", Alternative_Approach_Node)

workflow.add_edge(START, "Intent_Node")
def router(state: FitnessAgentState) -> str:
    if state["intent"] == "GeneralChat":
        return "General_Chat_Node"
    elif state["intent"] == "ExercisePlan":
        return "Exercise_Plan_Node"
    elif state["intent"] == "NearbyEvents":
        return "Nearby_Event_Node"
    else:
        return 'END'


workflow.add_conditional_edges(
    "Intent_Node",
    router, 
    {   "END": END,
        "General_Chat_Node": "General_Chat_Node",
        "Exercise_Plan_Node": "Exercise_Plan_Node",
        "Nearby_Event_Node": "Nearby_Event_Node"
    }
)

def router2(state: FitnessAgentState) -> str:
    if state.get("matched_event"):
        return "Book_Nearby_Event_Node"
    else:
        return "Alternative_Approach_Node" 

workflow.add_conditional_edges(
    "Nearby_Event_Node",
    router2, 
    {   "END": END,
        "Book_Nearby_Event_Node": "Book_Nearby_Event_Node",
        "Alternative_Approach_Node": "Alternative_Approach_Node"
    }
)


workflow.add_edge("General_Chat_Node", END)
workflow.add_edge("Exercise_Plan_Node", END)
workflow.add_edge("Book_Nearby_Event_Node", END)
workflow.add_edge("Alternative_Approach_Node", END)


FITNESS_ASSISTANT_GRAPH = workflow.compile()


FITNESS_ASSISTANT_GRAPH





if __name__ == "__main__":

    config = {"configurable": {"thread_id": "session_001"}}


    # 1️⃣ Define initial state
    initial_state: FitnessAgentState = {
        # Try any of these
        # "user_input": "What is hatha yoga?",
        # "user_input": "Suggest an exercise plan for training core in the gym for 30 minutes",
        "user_input": "Find and book a beginner tennis meetup near Menlo Park 94025",
        # "user_input": "Find an intermediate volleyball meetup near Menlo Park 94025 in the morning",

        "intent": None,
        "exercise_plan": None,
        "matched_event": None,
        "booking_confirmation": None,
        "assistant_reply": None
    }

    # 2️⃣ Run the full workflow (detect intent → find event)
    state = FITNESS_ASSISTANT_GRAPH.invoke(initial_state, config=config)

    print(state)

  