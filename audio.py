from pydub import AudioSegment
from pydub.playback import play
import requests
import tempfile

# URL of the pronunciation audio
mp3_url = "https://audio.howtopronounce.com/indonesian/sebagai.mp3"

# Download the audio file
response = requests.get(mp3_url)
if response.status_code == 200:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(response.content)
        temp_audio_path = temp_audio.name

    # Load and play the audio file
    audio = AudioSegment.from_file(temp_audio_path, format="mp3")
    play(audio)
else:
    print("Failed to download audio.")
