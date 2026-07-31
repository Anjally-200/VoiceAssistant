import os
import streamlit as st

from speak import speak
from speech import speech_to_text
from weather import get_weather
from news import get_news
from reminder import (
    add_reminder,
    get_reminders,
    delete_reminder
)
from commands import process_command

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Voice Activated Personal Assistant",
    page_icon="🎙️",
    layout="centered"
)

# ==========================================
# Create Audio Folder
# ==========================================

AUDIO_FOLDER = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ==========================================
# Title
# ==========================================

st.title(" Voice Activated Personal Assistant")
st.caption("An AI-powered assistant developed using Python and Streamlit.")

st.write("""
### Welcome!

Your AI Assistant can perform:

-  Speech Recognition
-  Text-to-Speech
-  Weather Information
-  Latest News
-  Reminder System
- Voice Command Processing
""")

st.success("Assistant is Ready!")

# ==========================================
# Text To Speech
# ==========================================

st.divider()
st.header(" Text To Speech")

if st.button("Test Voice"):

    message = "Hello, how can I help you?"

    try:
        audio_file = speak(message)

        # If speak() returns an audio file
        if audio_file:
            st.audio(audio_file, format="audio/mp3", autoplay=True)

    except Exception as e:
        st.exception(e)

# ==========================================
# Speech Recognition
# ==========================================

st.divider()
st.header(" Speech Recognition")

uploaded_audio = st.file_uploader(
    "Upload an Audio File",
    type=["wav", "mp3", "m4a", "ogg"]
)

if uploaded_audio is not None:

    file_path = os.path.join(AUDIO_FOLDER, uploaded_audio.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_audio.getbuffer())

    st.audio(uploaded_audio)

    with st.spinner("Recognizing Speech..."):

        try:

            text, language = speech_to_text(file_path)

            st.success("Speech Recognized Successfully!")

            st.subheader("Recognized Text")
            st.write(text)

            st.subheader("Detected Language")
            st.write(language)

            if text:

                result = process_command(text)

                st.divider()
                st.subheader("Assistant Response")

                st.success(result["message"])

                try:
                    audio_file = speak(result["message"])

                    if audio_file:
                        st.audio(audio_file, format="audio/mp3", autoplay=True)

                except Exception as e:
                    st.exception(e)

                if result.get("type") == "weather":

                    weather = result["data"]

                    st.write(f" Temperature : {weather['temperature']} °C")
                    st.write(f" Humidity : {weather['humidity']} %")
                    st.write(f" Wind Speed : {weather['wind']} m/s")

                elif "Reminder added" in result["message"]:

                    st.info("Reminder has been added successfully.")

        except Exception as e:
            st.exception(e)

# ==========================================
# Weather
# ==========================================

st.divider()
st.header(" Weather Information")

city = st.text_input("Enter City Name")

if st.button("Get Weather"):

    if city.strip():

        with st.spinner("Fetching Weather..."):

            weather = get_weather(city)

        if weather:

            message = (
                f"The weather in {weather['city']} is "
                f"{weather['temperature']} degree Celsius with "
                f"{weather['description']}."
            )

            st.success(message)

            st.write(f" Temperature : {weather['temperature']} °C")
            st.write(f" Humidity : {weather['humidity']} %")
            st.write(f" Wind Speed : {weather['wind']} m/s")

            try:
                audio_file = speak(message)

                if audio_file:
                    st.audio(audio_file, format="audio/mp3", autoplay=True)

            except Exception as e:
                st.exception(e)

        else:
            st.error("Unable to fetch weather information.")

    else:
        st.warning("Please enter a city name.")

# ==========================================
# Latest News
# ==========================================

st.divider()
st.header(" Latest News")

col1, col2 = st.columns([3, 1])

with col1:
    get_news_btn = st.button("Get Latest News")

with col2:
    refresh_btn = st.button("🔄 Refresh")

if get_news_btn or refresh_btn:

    with st.spinner("Fetching Latest News..."):

        try:

            headlines = get_news()

            if headlines:

                st.success("Top Headlines")

                for i, headline in enumerate(headlines, start=1):
                    st.markdown(f"**{i}. {headline}**")

                speech = "Here are today's top headlines. "

                for headline in headlines[:3]:
                    speech += headline + ". "

                try:
                    audio_file = speak(speech)

                    if audio_file:
                        st.audio(audio_file, format="audio/mp3", autoplay=True)

                except Exception as e:
                    st.exception(e)

            else:
                st.warning("No news available.")

        except Exception as e:
            st.exception(e)

# ==========================================
# Reminder
# ==========================================

st.divider()
st.header(" Reminder")

new_reminder = st.text_input(
    "Enter Reminder",
    placeholder="e.g., Buy groceries"
)

if st.button("Add Reminder"):

    if new_reminder.strip():

        add_reminder(new_reminder)

        st.success("Reminder added successfully!")

        st.rerun()

    else:
        st.warning("Please enter a reminder.")

# ==========================================
# Display Reminders
# ==========================================

st.subheader(" Saved Reminders")

reminders = get_reminders()

if reminders:

    for index, item in enumerate(reminders):

        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f"• {item}")

        with col2:

            if st.button("Delete", key=f"delete_{index}"):

                delete_reminder(index)
                st.rerun()

else:

    st.info("No reminders found.")

# ==========================================
# Footer
# ==========================================

st.divider()
st.caption(" Voice Activated Personal Assistant | Python • Streamlit")