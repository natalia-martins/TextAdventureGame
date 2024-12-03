from elevenlabs import play
from elevenlabs.client import ElevenLabs


def call_audio(text):
    client = ElevenLabs(
        api_key="api goes here",  # Defaults to ELEVEN_API_KEY
    )

    audio = client.generate(
        text=text,
        voice="Lily",
        model="eleven_multilingual_v2"
    )

    play(audio)
