import os
import time
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import pygame
from google import genai

# --- CONFIGURATION ---

# Securely loading the API key from environment variables
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable is not set!")
    exit(1)

client = genai.Client(api_key=API_KEY)

# Local voice recognition via Vosk
if not os.path.exists("model"):
    print("Error: 'model' folder not found! Please download an English Vosk model.")
    exit(1)

vosk_model = Model("model")
samplerate = 16000
q = queue.Queue()

# Trigger names for Yumi
YUMI_NAMES = ["yumi"]

# List of apps and games
MY_APPS = {
    "cs": "730",
    "dota": "570",
    "albion": "761890",
    "guild": "311260",
    "black desert": "582660",
    "steam": "open/main",
    "music": "https://music.youtube.com", 
    "minecraft": "C:/Games/Minecraft/TLauncher.exe" 
}

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def yumi_talk(text):
    print(f"Yumi: {text}")
    filename = f"yumi_voice_{int(time.time())}.mp3"
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
        pygame.mixer.quit()
    finally:
        if os.path.exists(filename):
            os.remove(filename)

def ask_yumi_ai(user_text):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"You are Yumi, an AI assistant for Quanti. Answer briefly and amicably. Request: {user_text}"
        )
        return response.text
    except Exception as e:
        return f"Sir, there was a glitch in my system: {e}"

def listen():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=None, 
                           dtype='int16', channels=1, callback=callback):
        rec = KaldiRecognizer(vosk_model, samplerate)
        print(">>> Yumi is listening...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                query = result.get('text', '')
                if query:
                    print(f"You: {query}")
                    return query.lower()

# --- MAIN LOOP ---

if __name__ == "__main__":
    yumi_talk("Quanti, I have updated my core. We are ready to go.")
    
    while True:
        command = listen()
        if any(name in command for name in YUMI_NAMES):
            clean_command = command
            for name in YUMI_NAMES:
                clean_command = clean_command.replace(name, "").strip()

            if not clean_command:
                yumi_talk("Listening, Quanti.")
                continue

            # Execution commands
            if "launch" in clean_command or "open" in clean_command:
                found = False
                for name, target in MY_APPS.items():
                    if name in clean_command:
                        yumi_talk(f"Opening {name}.")
                        if target.isdigit() or target.startswith("open"):
                            os.startfile(f"steam://run/{target}")
                        else:
                            os.startfile(target)
                        found = True
                        break
                if not found:
                    yumi_talk(ask_yumi_ai(clean_command))
            elif "shut down" in clean_command or "turn off" in clean_command:
                yumi_talk("See you later, Quanti!")
                break
            else:
                yumi_talk("Just a second...")
                yumi_talk(ask_yumi_ai(clean_command))
