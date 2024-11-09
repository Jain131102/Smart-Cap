import speech_recognition as sr
import pyttsx3
import time
import subprocess
import os
from gtts import gTTS
from playsound import playsound as ps
# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get the absolute path to the project directory
PROJECT_DIR = os.path.expanduser('~/project/Smart_Cap')
VENV_PYTHON = os.path.expanduser('~/project/piper/.venv/bin/python3')
DETECT_PYTHON = os.path.expanduser('~/project/DETECT/examples/tf/bin/python3')

def speak(text):
    """
    Converts the provided text to speech.
    Args:
        text (str): The text that will be spoken.
    """
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)

def run_subprocess(python_path, script_path, cwd=None, additional_args=None):
    """
    Runs a subprocess with proper error handling.
    Args:
        python_path (str): Path to Python interpreter
        script_path (str): Path to script to run
        cwd (str): Working directory for the subprocess
        additional_args (list): Additional command line arguments
    """
    try:
        cmd = [python_path, script_path]
        if additional_args:
            cmd.extend(additional_args)
            
        process = subprocess.Popen(
            cmd,
            cwd=cwd or PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            print(f"Error running {script_path}:")
            print(f"Exit code: {process.returncode}")
            if stderr:
                print(f"Error output: {stderr}")
        elif stdout:
            print(f"Output: {stdout}")
            
    except Exception as e:
        print(f"Failed to run {script_path}: {str(e)}")

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
    t="Powering on"
    tts=gTTS(text=t,lang='en')
    tts.save("xyz.mp3")
    ps("xyz.mp3")
    
    time.sleep(1)
    t="What would you like me to assist you with?"
    tts=gTTS(text=t,lang='en')
    tts.save("xyz.mp3")
    ps("xyz.mp3")
    
    while True:
        command = listen(recognizer)
        if command:
            if "play" in command:
                t="Playing Music"
                tts=gTTS(text=t,lang='en')
                tts.save("xyz.mp3")
                ps("xyz.mp3")
                run_subprocess(
                    VENV_PYTHON,
                    os.path.join(PROJECT_DIR, 'music.py')
                )
                
            elif "ai" in command:
                t="Starting AI conversation"
                tts=gTTS(text=t,lang='en')
                tts.save("xyz.mp3")
                ps("xyz.mp3")
                run_subprocess(
                    VENV_PYTHON,
                    os.path.join(PROJECT_DIR, 'assi.py')
                )
                
            elif "detect" in command:
                t="Object detection mode on"
                tts=gTTS(text=t,lang='en')
                tts.save("xyz.mp3")
                ps("xyz.mp3")
                run_subprocess(
                    DETECT_PYTHON,
                    'detect.py',
                    cwd=PROJECT_DIR,
                    additional_args=['--model', 'efficientdet_lite0.tflite']
                )
                
            elif "guide" in command:
                t="Guiding routes mode on"
                tts=gTTS(text=t,lang='en')
                tts.save("xyz.mp3")
                ps("xyz.mp3")
                run_subprocess(
                    VENV_PYTHON,
                    os.path.join(PROJECT_DIR, 'guide.py')
                )
                
            elif "bye" in command:
                t="Powering Off"
                tts=gTTS(text=t,lang='en')
                tts.save("xyz.mp3")
                ps("xyz.mp3")
                break
                
            else:
                speak("Command not recognized, please try again.")

if __name__ == "__main__":
    main()
