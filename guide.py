# pip install requests gtts pygame SpeechRecognition
 
import requests  # To handle HTTP requests
from gtts import gTTS  # Google Text-to-Speech module
import pygame  # Pygame for handling audio playback
import time  # Time module to handle delays
import re  # Regular expressions for text cleaning
import speech_recognition as sr  # SpeechRecognition for capturing voice input

# Step 1: Get the current location using Google Cloud Geolocation API

# Function to get destination from voice input
def get_voice_input():
    """
    Prompts the user to say the destination and captures it as text using SpeechRecognition.
    
    Returns:
        str: The destination spoken by the user.
    """
    # Prompt user with TTS
    tts = gTTS("Please say your destination.", lang='en')
    tts.save("prompt.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("prompt.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    
    # Capture voice input
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for destination...")
        audio = recognizer.listen(source)
        try:
            # Convert voice input to text
            destination = recognizer.recognize_google(audio)
            print(f"Destination captured: {destination}")
            return destination
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        

def get_current_location(api_key):
    """
    Fetches the user's current location (latitude and longitude) using Google Cloud Geolocation API.
    
    Args:
        api_key (str): Your Google Cloud API key.

    Returns:
        tuple: A tuple containing latitude and longitude as strings or None if an error occurs.
    """
    try:
        # Prepare the request payload
        payload = {
            "considerIp": "true"  # Use IP address to get location
        }
        
        # Send request to Google Geolocation API
        response = requests.post(f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}", json=payload)
        
        # Print the entire response for debugging
        print("Response from Geolocation API:", response.json())

        data = response.json()
        
        # Extract latitude and longitude
        lat = data['location']['lat']
        lon = data['location']['lng']
        
        return str(lat), str(lon)
    except Exception as e:
        print(f"Error fetching current location: {e}")
        return None, None

# Step 2: Get directions from Google Maps API
def get_directions(api_key, origin_lat, origin_lon, destination):
    """
    Fetches directions from Google Maps API using current location as the origin.

    Args:
        api_key (str): Your Google Maps API key.
        origin_lat (str): Latitude of the origin.
        origin_lon (str): Longitude of the origin.
        destination (str): Destination location.

    Returns:
        list: A list of cleaned direction steps, or None if the API call fails.
    """
    # Construct the origin as "latitude,longitude"
    origin = f"{origin_lat},{origin_lon}"
    
    
    # Construct the Google Maps API URL
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    
    # Send the request to Google Maps API and store the response
    response = requests.get(url)
    directions = response.json()

    # Check if the API request was successful (status 'OK')
    if directions['status'] == 'OK':
        steps = directions['routes'][0]['legs'][0]['steps']
        directions_list = []
        for step in steps:
            clean_instruction = clean_html(step['html_instructions'])
            directions_list.append(clean_instruction)
        return directions_list
    else:
        print(f"Error fetching directions: {directions['status']}")
        return None

# Step 3: Clean HTML from instructions
def clean_html(raw_html):
    """
    Removes HTML tags from a given string.

    Args:
        raw_html (str): The raw string with HTML tags.

    Returns:
        str: Cleaned string without HTML tags.
    """
    cleanr = re.compile('<.*?>')  # Regular expression to match HTML tags
    cleantext = re.sub(cleanr, '', raw_html)  # Replace HTML tags with empty strings
    return cleantext

# Step 4: Convert text directions to speech
def speak_directions(directions):
    """
    Converts text directions to speech and plays the audio.

    Args:
        directions (list): A list of text directions to be spoken.
    """
    text = ' '.join(directions)  # Combine the list of directions into a single string
    tts = gTTS(text, lang='en')  # Convert the text to speech
    tts.save("directions.mp3")  # Save the generated speech as an MP3 file

    # Initialize Pygame mixer to play audio
    pygame.mixer.init()
    pygame.mixer.music.load("directions.mp3")
    pygame.mixer.music.play()

    # Wait for the audio file to finish playing
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Example Usage
google_api_key = 'api_key'  # Replace with your actual Google Cloud API key

# Get the current location (latitude, longitude) using Google Cloud Geolocation API
origin_lat, origin_lon = get_current_location(google_api_key)

if origin_lat and origin_lon:
    # Capture the destination using voice input
    destination = get_voice_input()
    
    if destination:
        # Fetch the directions using the Google Maps API
        directions = get_directions(google_api_key, origin_lat, origin_lon, destination)

        if directions:
            # If directions are available, convert them to speech and play them
            speak_directions(directions)
        else:
            print("Error fetching directions")
    else:
        print("No valid destination provided.")
else:
    print("Error fetching current location")











