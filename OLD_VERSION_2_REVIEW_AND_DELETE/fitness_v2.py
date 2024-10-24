import os
import streamlit as st
from groq import Groq
import pandas as pd
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("fitness")

def generate_plans_with_groq(api_key, age, weight, height, gender, diet_pref, fitness_goal, exercise_time):
    """
    Generate a personalized fitness and meal plan using Groq API.
    
    Parameters:
    - api_key (str): API key for Groq.
    - age (int): Age of the user.
    - weight (float): Weight of the user.
    - height (float): Height of the user.
    - gender (str): Gender of the user.
    - diet_pref (str): Dietary preferences of the user.
    - fitness_goal (str): Fitness goal of the user.
    - exercise_time (int): Available exercise time per day in minutes.
    
    Returns:
    - dict: Generated fitness and meal plan.
    """
    try:
        client = Groq(api_key=api_key)  # Initialize Groq client with the provided API key

        workout_prompt = f"""
        Generate a detailed week-long workout plan for a {age}-year-old {gender} who wants to achieve {fitness_goal} and has {exercise_time} minutes daily for exercise. Focus on exercises that build shoulders, chest, and back muscles.
        Please format the plan as follows:
        Day 1: Workout Description
        Day 2: Workout Description
        Day 3: Workout Description
        Day 4: Workout Description
        Day 5: Workout Description
        Day 6: Workout Description
        Day 7: Workout Description
        """

        meal_prompt = f"""
        Generate a detailed week-long meal plan for a {age}-year-old {gender} who weighs {weight} kg, is {height} cm tall, and prefers a {diet_pref} diet. The goal is to support {fitness_goal}.
        Please format the plan as follows:
        Day 1: Meal Description
        Day 2: Meal Description
        Day 3: Meal Description
        Day 4: Meal Description
        Day 5: Meal Description
        Day 6: Meal Description
        Day 7: Meal Description
        """

        workout_plan = client.generate(workout_prompt)
        meal_plan = client.generate(meal_prompt)
        return workout_plan, meal_plan
    except Exception as e:
        st.error(f"Error generating plans: {e}")
        return None, None

def chatbot_response(api_key, user_input):
    """
    Generate a chatbot response using Groq API.
    
    Parameters:
    - api_key (str): API key for Groq.
    - user_input (str): User input for the chatbot.
    
    Returns:
    - str: Chatbot response.
    """
    try:
        client = Groq(api_key=api_key)  # Initialize Groq client with the provided API key

        chatbot_prompt = f"""
        You are a fitness and nutrition expert. Answer the following question:
        {user_input}
        """

        response = client.generate(chatbot_prompt)
        return response
    except Exception as e:
        return f"Error generating chatbot response: {e}"

# Streamlit app
def main():
    st.title("AI Fitness Coach")

    st.subheader("Generate Personalized Fitness and Meal Plans")
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    diet_pref = st.selectbox("Diet Preference", ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"])
    fitness_goal = st.text_input("Fitness Goal", "Increase upper body strength")
    exercise_time = st.number_input("Available Exercise Time (minutes per day)", min_value=1, max_value=300, value=60)

    if st.button("Generate Plans"):
        workout_plan, meal_plan = generate_plans_with_groq(api_key, age, weight, height, gender, diet_pref, fitness_goal, exercise_time)
        if workout_plan and meal_plan:
            st.subheader("Generated Workout Plan:")
            st.text(workout_plan)

            st.subheader("Generated Meal Plan:")
            st.text(meal_plan)

    st.subheader("Chat with the AI Coach")
    user_input = st.text_area("If you have any questions or need further customization, ask here:")
    if st.button("Send"):
        if user_input:
            response = chatbot_response(api_key, user_input)
            st.markdown(f"*AI Coach:* {response}")
        else:
            st.error("Please enter a message to send to the AI Coach.")

if __name__ == "__main__":
    main()