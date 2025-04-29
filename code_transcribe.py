import whisper

model = whisper.load_model("base")
result = model.transcribe("sound.mp3")

with open("transcription.txt", "w") as F:
    f.write(result["text"])
    