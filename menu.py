import speech_recognition as sr  # For speech recognition
import pyttsx3  # For text-to-speech
import time  # For delays

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """
    Converts the provided text to speech.

    Args:
        text (str): The text that will be spoken.
    """
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)

def listen(recognizer):
    """
    Listens for voice commands and returns the recognized command.

    Args:
        recognizer (speech_recognition.Recognizer): The Speech Recognition recognizer.

    Returns:
        str: The recognized command as text.
    """
    print("Listening...")

    with sr.Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Listen for audio input
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            try:
                # Use Google Speech Recognition to convert audio to text
                command = recognizer.recognize_google(audio)
                print("You said:", command)
                return command.lower()
            except sr.UnknownValueError:
                print("Could not understand the audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                return None

        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None

def main():
    """
    Main function to run the voice assistant.
    Initializes the recognizer and handles command processing.
    """
    recognizer = sr.Recognizer()
    speak("Powering on")
    time.sleep(1)
    speak("What would you like me to assist you with?")

    while True:
        command = listen(recognizer)

        if command:
            if "play" in command:
                speak("Playing music")
                # Placeholder for music playback logic
            elif "ai" in command:
                speak("Starting AI conversation")
                # Placeholder for AI interaction logic
            elif "detect" in command:
                speak("Object detection mode on")
                # Placeholder for object detection function
            elif "guide" in command:
                speak("Guiding routes mode on")
                # Placeholder for guiding routes function
            elif "bye" in command:
                speak("Turning off")
                break
            else:
                speak("Command not recognized, please try again.")

if __name__ == "__main__":
    main()

