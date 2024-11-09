import speech_recognition as sr
import google.generativeai as genai
import pyttsx3  # Using pyttsx3 for TTS
import os
import subprocess
import re
import time
from gtts import gTTS
from io import BytesIO
import pygame
class JarvisAssistant:  
    def __init__(self):
        genai.configure(api_key='AIzaSyAa4ygLGWZJaUKSubVdiQGhWS66Oc3sjQg')  # Replace with your actual API key
        self.model = genai.GenerativeModel('gemini-1.5-pro-002')
        self.recognizer = sr.Recognizer()

    def clean_text(self, text):
        # Remove asterisks
        text = text.replace('*', '')
        # Remove any markdown-style links
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove any remaining special characters or markdown syntax
        text = re.sub(r'[#_~`>]', '', text)
        # Replace multiple newlines with a single one
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

    def speak_fast(self, text, language='en'):
        cleaned_text = self.clean_text(text)
        """
        Speaks the given text using gTTS in the fastest way possible.

        Args:
            text: The text to be spoken.
            language: The language of the text (default: 'en').
        """
        tts = gTTS(text=cleaned_text, lang=language)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        pygame.mixer.init()
        pygame.mixer.music.load(fp)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    """def speak(self, text):
        cleaned_text = self.clean_text(text)
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say("hello I am the voice from your PC")

        #engine.say(cleaned_text)
        engine.runAndWait()"""

    def take_command(self):
        with sr.Microphone(device_index=2) as source:
            print("Listening...")
            self.speak_fast("Listening")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust duration if needed
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "None"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "None"

    def gemini_query(self, query):
        response = self.model.generate_content(query)
        return response.text

    def run(self):
        #self.speak("Hello! How may I assist you?")
        self.speak_fast("Hello! How may I assist you?")

        while True:
            query = self.take_command()

            if 'exit' in query:
                #self.speak("Goodbye!")
                self.speak_fast("Goodbye!")
                exit()
            elif query != "None":
                response = self.gemini_query(query)
                print(response)
                #self.speak(response)
                self.speak_fast(response)

if __name__ == "__main__":
    assistant = JarvisAssistant()
    assistant.run()






