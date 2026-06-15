from groq import Groq

client = Groq(
)

with open(r"D:\screemer\master\data\tara_friendly_hindi.mp3", "rb") as file:
    transcription = client.audio.translations.create(
        file=file,
        model="whisper-large-v3",
    )

print(transcription.text)

