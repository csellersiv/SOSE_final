import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

st.title("🌴 Ideal Vacation Spot Finder 🌍")
st.write("Take this short survey, and we'll suggest the perfect vacation spot for you!")

st.sidebar.header("📝 Vacation Preferences Survey")

climate = st.sidebar.selectbox(
    "What type of climate do you prefer?",
    ["Tropical", "Temperate", "Cold", "Desert", "Varied"]
)

activity_level = st.sidebar.radio(
    "How active do you want your vacation to be?",
    ["Relaxed", "Moderate", "Adventurous"]
)

activities = st.sidebar.multiselect(
    "Select your favorite vacation activities:",
    ["Beach lounging", "Hiking", "Cultural tours", "Shopping", "Water sports", "Skiing", "Nightlife"]
)

companions = st.sidebar.selectbox(
    "Who are you traveling with?",
    ["Solo", "Family", "Friends", "Partner", "Group"]
)

budget = st.sidebar.slider(
    "What is your budget for this trip (in USD)?",
    min_value=500,
    max_value=20000,
    step=500
)

if st.sidebar.button("🌟 Find My Vacation Spot"):
    if not activities:
        st.error("Please select at least one activity.")
    else:
        user_input = (
            f"Climate: {climate}\n"
            f"Activity Level: {activity_level}\n"
            f"Activities: {', '.join(activities)}\n"
            f"Travel Companions: {companions}\n"
            f"Budget: ${budget}"
        )

        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are a travel expert recommending vacation spots based on user preferences."},
                    {"role": "user", "content": f"Based on the following survey responses, suggest an ideal vacation spot:\n{user_input}"}
                ]
            )

            suggestion = completion.choices[0].message.content.strip()
            st.subheader("✨ Your Ideal Vacation Spot ✨")
            st.markdown(suggestion)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.write("\nThis app uses OpenAI to generate personalized travel recommendations based on your preferences.")
