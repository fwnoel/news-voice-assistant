import pyttsx3
import speech_recognition as sr
import requests
import PySimpleGUI as sg

# Initialize the TTS engine
engine = pyttsx3.init()

# NewsAPI setup
NEWS_API_KEY = '78a8b6674c4e4ef982f165979fd43625'  # Replace with your NewsAPI Key
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, there was an error with the speech recognition service.")
            return ""

# Function to get news articles from NewsAPI
def get_news(query):
    params = {
        'q': query,  # Query for news related to the question
        'apiKey': NEWS_API_KEY,
        'pageSize': 3  # Limit to 3 news articles
    }

    try:
        response = requests.get(NEWS_ENDPOINT, params=params)
        response.raise_for_status()
        news_data = response.json()

        # Check if articles are available
        if news_data['status'] == 'ok' and news_data['totalResults'] > 0:
            articles = news_data['articles']
            news_snippet = f"Here are the top 3 news results for '{query}':\n"
            for i, article in enumerate(articles):
                news_snippet += f"{i+1}. {article['title']} - {article['description']}\n"
            return news_snippet
        else:
            return "Sorry, no news articles found for that query."
    except Exception as e:
        return f"Error: {e}"

# Define the layout for the GUI
layout = [
    [sg.Text("Voice Assistant", size=(30, 1), justification='center')],
    [sg.Button("Ask", size=(15, 2), key='ASK')],
    [sg.Text("Response will be displayed here.", size=(40, 2), key='RESPONSE')],
]

# Create the window
window = sg.Window("Voice Assistant", layout)

# Event loop for the GUI
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == 'ASK':
        # Listen for the user's question
        query = listen()
        if query:
            # Get the response from NewsAPI
            response = get_news(query)
            # Update the response in the GUI window
            window['RESPONSE'].update(response)
            # Speak the response aloud
            speak(response)

# Close the window when done
window.close()
