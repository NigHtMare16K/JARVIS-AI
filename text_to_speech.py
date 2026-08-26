from piper import PiperVoice
import wave

voice = PiperVoice.load("en_US-lessac-medium.onnx")

text = "Hello, I am Jarvis. I am an Ai assistant, I can do your daily tasks. How can I help you?"

with wave.open("output.wav", "wb") as wav_file:
    voice.synthesize_wav(text, wav_file)

print("Audio generated successfully!")