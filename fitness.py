import os
import streamlit as st
from groq import Groq
import pandas as pd

api_key = st.secrets["fitnessapi"]

# Function to generate a personalized fitness and meal plan using Groq API
def generate_plans_with_groq(api_key, age, weight, height, gender, diet_pref, fitness_goal, exercise_time):
    client = Groq(api_key=api_key)  # Initialize Groq client with the provided API key

    workout_prompt = f"""
    Generate a detailed week-long workout plan for a {age}-year-old {gender} who wants to {fitness_goal} and has {exercise_time} minutes daily for exercise.
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
    Generate a detailed week-long meal plan for a {diet_pref} diet to help a {age}-year-old {gender} achieve {fitness_goal}.
    Please format the plan as follows:
    Day 1: Breakfast, Lunch, Dinner, Snacks
    Day 2: Breakfast, Lunch, Dinner, Snacks
    Day 3: Breakfast, Lunch, Dinner, Snacks
    Day 4: Breakfast, Lunch, Dinner, Snacks
    Day 5: Breakfast, Lunch, Dinner, Snacks
    Day 6: Breakfast, Lunch, Dinner, Snacks
    Day 7: Breakfast, Lunch, Dinner, Snacks
    """

    workout_plan = client.chat.completions.create(
        messages=[{"role": "user", "content": workout_prompt}],
        model="llama3-8b-8192",
    )

    meal_plan = client.chat.completions.create(
        messages=[{"role": "user", "content": meal_prompt}],
        model="llama3-8b-8192",
    )

    return workout_plan.choices[0].message.content, meal_plan.choices[0].message.content

# Function to handle chatbot responses
def chatbot_response(api_key, user_input):
    client = Groq(api_key=api_key)  # Initialize Groq client with the provided API key

    chat_prompt = f"""
    User: {user_input}
    AI: 
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": chat_prompt}],
        model="llama3-8b-8192",
    )

    return response.choices[0].message.content

# Streamlit app
def main():
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 3em;
            color: #FF6347;
            text-align: center;
            margin-bottom: 0.5em;
        }
        .description {
            font-size: 1.2em;
            color: #2E8B57;
            text-align: center;
            margin-bottom: 2em;
        }
        .css-1d391kg {
            background-color: #2E8B57 !important;
        }
        .css-1cpxqw2 {
            color: #FFFFFF !important;
        }
        .css-1n76uvr, .css-7jyd01, .css-vfskoc, .css-1ktcvv5 { 
            color: #2E8B57 !important;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Add the title image
    st.image("titlepage.jpeg", use_column_width=True)

    st.markdown(
        """
        <div class="main-title">AI-Powered Fitness & Nutrition Coach</div>
        <div class="description">
           Welcome to the AI-Powered Fitness & Nutrition Coach, your personalized guide to achieving your fitness goals. This innovative application leverages advanced AI technology to deliver customized workout and meal plans tailored to your unique needs.
        </div>
        """, unsafe_allow_html=True
    )

    st.sidebar.header("Enter Your Details")
    
    age = st.sidebar.number_input("Age", min_value=1, max_value=100, value=25)
    weight = st.sidebar.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    height = st.sidebar.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
    diet_pref = st.sidebar.selectbox("Diet Preferences", ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"])
    fitness_goal = st.sidebar.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance", "Endurance", "Flexibility"])
    exercise_time = st.sidebar.slider("Exercise Time (minutes per day)", min_value=10, max_value=120, value=60)

    if st.sidebar.button("Generate Plan"):
        if api_key:
            with st.spinner('Generating your personalized fitness and meal plan...'):
                workout_plan, meal_plan = generate_plans_with_groq(api_key, age, weight, height, gender, diet_pref, fitness_goal, exercise_time)
                
                # Display the raw outputs
                st.subheader("Generated Workout Plan:")
                st.text(workout_plan)

                st.subheader("Generated Meal Plan:")
                st.text(meal_plan)

    # Chatbot section
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
