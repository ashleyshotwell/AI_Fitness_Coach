import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment variables
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
    - tuple: Generated workout plan and meal plan.
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

        workout_plan_response = client.chat.completions.create(
            messages=[{"role": "user", "content": workout_prompt}],
            model="llama3-8b-8192",
        )

        meal_plan_response = client.chat.completions.create(
            messages=[{"role": "user", "content": meal_prompt}],
            model="llama3-8b-8192",
        )

        workout_plan = workout_plan_response.choices[0].message.content
        meal_plan = meal_plan_response.choices[0].message.content

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

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": chatbot_prompt}],
            model="llama3-8b-8192",
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating chatbot response: {e}"

# Streamlit app
def main():
    st.title("AI Fitness Coach")

    # Add the title image with the width parameter to scale it down by 25%
    st.image("titlepage.jpeg", width=int(0.75 * 800), caption="AI-Powered Fitness & Nutrition Coach", output_format="JPEG")

    st.markdown(
        """
        <div class="main-title">AI-Powered Fitness & Nutrition Coach</div>
        <div class="description">
           Welcome to the AI-Powered Fitness & Nutrition Coach, your personalized guide to achieving your fitness goals. This innovative application leverages advanced AI technology to deliver customized workout and meal plans tailored to your unique needs.
        </div>
        """, unsafe_allow_html=True
    )

    st.sidebar.subheader("Generate Personalized Fitness and Meal Plans")
    age = st.sidebar.number_input("Age", min_value=1, max_value=120, value=25)
    weight = st.sidebar.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
    height = st.sidebar.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
    diet_pref = st.sidebar.selectbox("Diet Preferences", ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"])
    fitness_goal = st.sidebar.selectbox("Fitness Goal", ["Increase Upper Body Width", "Weight Loss", "Muscle Gain", "Maintenance", "Endurance", "Flexibility"])
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