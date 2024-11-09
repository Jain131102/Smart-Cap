#!/usr/bin/env python3

import os
import subprocess
import requests
import re
from pathlib import Path
import speech_recognition as sr
from gtts import gTTS
import tempfile

class MusicPlayer:
    def __init__(self):
        # Configuration
        self.home = str(Path.home())
        self.invidious_instance = "https://vid.puffyan.us"
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        
        # Create temp directory for speech files
        self.temp_dir = tempfile.mkdtemp()

    def recognize_speech(self):
        """Record and recognize speech"""
        print("Listening for your song request...")
        self.speak("Listening for your song request")
        with sr.Microphone() as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source)
            
            try:
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                try:
                    # Use Google Speech Recognition
                    text = self.recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    return text.lower()
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                    return None
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    return None
                    
            except sr.WaitTimeoutError:
                print("No speech detected within timeout period")
                return None

    def speak(self, text):
        """Speak text using gTTS and mpg123"""
        try:
            # Create a temporary file for the speech
            temp_speech = os.path.join(self.temp_dir, 'speech.mp3')
            
            # Generate speech audio file
            tts = gTTS(text=text, lang='en')
            tts.save(temp_speech)
            
            # Play the speech
            subprocess.run(['mpg123', '-q', temp_speech], check=True)
            
            # Clean up
            os.remove(temp_speech)
        except Exception as e:
            print(f"Speech error: {str(e)}")

    def get_video_id(self, query):
        """Search for video on invidious instance"""
        search_query = f"song audio {query}".replace(' ', '+')
        url = f"{self.invidious_instance}/search?q={search_query}"
        response = requests.get(url)
        
        # Find first video ID using regex
        match = re.search(r'watch\?v=([a-zA-Z0-9_-]{11})', response.text)
        return match.group(0) if match else None

    def get_audio_url(self, youtube_url):
        """Get best audio stream URL using yt-dlp"""
        cmd = ['yt-dlp', '-f', 'bestaudio', '--get-url', youtube_url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def get_video_title(self, youtube_url):
        """Get video title using yt-dlp"""
        cmd = ['yt-dlp', '--get-title', youtube_url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def play_audio(self, audio_url):
        """Play audio using mpv"""
        subprocess.run(['mpv', audio_url], check=True)

    def send_notification(self, title):
        """Send system notification"""
        subprocess.run(['notify-send', 'Playing: ', title], check=True)

    def stop_current_playback(self):
        """Stop current playback using mpc"""
        subprocess.run(['mpc', 'stop'], check=True)
        subprocess.run(['mpc', 'clear'], check=True)

    def cleanup(self):
        """Clean up temporary directory"""
        try:
            os.rmdir(self.temp_dir)
        except:
            pass

    def run(self):
        """Main execution flow"""
        try:
            # Stop any current playback
            #self.stop_current_playback()

            # Get speech input
            audio_input = self.recognize_speech()
            if not audio_input:
                raise Exception("No speech detected or could not understand")

            # Confirm what was heard
            self.speak(f"Playing {audio_input}")

            # Get video details and play
            video_id = self.get_video_id(audio_input)
            if not video_id:
                raise Exception("No video found")

            youtube_url = f"https://youtube.com/{video_id}"
            audio_url = self.get_audio_url(youtube_url)
            title = self.get_video_title(youtube_url)

            # Play audio and notify
            self.play_audio(audio_url)
            self.send_notification(title)

        except Exception as e:
            print(f"Error: {str(e)}")
            self.speak("Sorry, there was an error")
            subprocess.run(['notify-send', 'Error', str(e)])
        finally:
            self.cleanup()

if __name__ == "__main__":
    player = MusicPlayer()
    player.run()
