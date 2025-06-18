import speech_recognition as sr
from pytgpt.phind import PHIND # Or choose another provider like LEO or WIZARD
import edge_tts
import asyncio
import sys
import pyaudio # Import PyAudio for direct audio playback
from pydub import AudioSegment # Import pydub for audio decoding
import io # For in-memory byte stream handling

# --- Configuration ---
# You can list available voices by running `edge-tts --list-voices` in your terminal
# and choosing a ShortName, e.g., "en-US-AriaNeural", "en-GB-RyanNeural", "en-IN-NeerjaNeural"
VOICE = "en-US-JennyNeural" # Default voice, change as desired
# These parameters are for PyAudio's output stream, expecting raw PCM.
# Edge TTS typically provides 24kHz, 16-bit, mono audio (often compressed, which pydub will handle).
AUDIO_RATE = 24000 # Sample rate (Hz)
AUDIO_CHANNELS = 1 # Mono
AUDIO_FORMAT = pyaudio.paInt16 # 16-bit PCM format

# --- Initialize AI Assistant ---
# Initialize the TGPT model. PHIND is a good default as it doesn't require an API key.
# You can explore other providers in python-tgpt if you wish.
try:
    bot = PHIND()
    print("AI assistant (PHIND) initialized successfully.")
except Exception as e:
    print(f"Error initializing PHIND: {e}")
    print("Please ensure 'python-tgpt' is installed correctly and has access to the internet.")
    sys.exit(1)

# --- Speech Recognition Setup ---
r = sr.Recognizer()
# Adjust for ambient noise before listening to improve accuracy.
# This step is crucial and might take a moment.
with sr.Microphone() as source:
    print("Adjusting for ambient noise... Please wait.")
    r.adjust_for_ambient_noise(source, duration=1) # Listen for 1 second to calibrate noise
    print("Adjustment complete. You can now speak.")

# --- Text-to-Speech Function (Edge TTS with PyAudio and pydub for decoding) ---
async def speak_text(text: str, p: pyaudio.PyAudio):
    """
    Converts text to speech using Edge TTS, decodes the audio with pydub,
    and plays it directly via PyAudio.
    """
    print(f"Synthesizing speech for: '{text[:min(50, len(text))]}...'") # Log first 50 chars of text

    communicate = edge_tts.Communicate(text, VOICE)

    stream = None
    try:
        # Collect all audio data chunks from Edge TTS stream
        audio_data_chunks = []
        async for chunk in communicate.stream():
            # Chunks are expected to be dictionaries.
            if isinstance(chunk, dict) and 'type' in chunk and 'data' in chunk:
                if chunk['type'] == "audio" and chunk['data']:
                    audio_data_chunks.append(chunk['data'])
                elif chunk['type'] == "WordBoundary":
                    # WordBoundary chunks are for timing information, not audio data. Ignore for playback.
                    pass
                else:
                    # Log unexpected chunk types that are not audio or word boundary.
                    print(f"Warning: Received unexpected chunk type from Edge TTS: {chunk.get('type', 'N/A')}")
                    print(f"Chunk content: {chunk}")
                    # If it's an error message from the service, it might contain a 'message' key.
                    if 'message' in chunk:
                        print(f"Edge TTS service error message: {chunk['message']}")
                        raise RuntimeError(f"Edge TTS service error: {chunk['message']}")
            else:
                # Log malformed chunks (not dictionaries or missing keys).
                print(f"Warning: Received a malformed chunk from Edge TTS. Type: {type(chunk)}")
                print(f"Chunk content: {chunk}")
                if isinstance(chunk, dict) and 'message' in chunk:
                    print(f"Edge TTS service error message: {chunk['message']}")
                    raise RuntimeError(f"Edge TTS service error: {chunk['message']}")

        if not audio_data_chunks:
            print("No audio data received from Edge TTS to play.")
            return

        # Combine all audio data chunks into a single byte string.
        # This combined data is likely compressed (e.g., MP3 or Opus) as provided by Edge TTS.
        full_compressed_audio = b"".join(audio_data_chunks)

        # Use io.BytesIO to treat the byte string as a file-like object for pydub.
        # pydub will automatically detect the format (e.g., MP3) from the byte stream.
        try:
            audio_segment = AudioSegment.from_file(io.BytesIO(full_compressed_audio))
        except Exception as e:
            print(f"Error decoding audio with pydub. Ensure FFmpeg is installed and in your system's PATH. Error: {e}")
            raise # Re-raise the exception to be caught by the main loop.

        # Convert the audio segment to the raw PCM format required by PyAudio.
        # We ensure the sample rate, number of channels, and sample width match our PyAudio configuration.
        audio_segment = audio_segment.set_frame_rate(AUDIO_RATE).set_channels(AUDIO_CHANNELS).set_sample_width(p.get_sample_size(AUDIO_FORMAT))

        # Open an audio stream for playback with PyAudio.
        stream = p.open(format=AUDIO_FORMAT,
                        channels=AUDIO_CHANNELS,
                        rate=AUDIO_RATE,
                        output=True)

        # Write the raw PCM data from the decoded audio segment to the PyAudio stream.
        stream.write(audio_segment.raw_data)

        print("Speech synthesis and playback complete.")

    except Exception as e:
        print(f"Error speaking text: {e}")
        # Provide more context if it's an Edge TTS specific error or FFmpeg issue.
        if "Edge TTS service error" in str(e):
            print("This indicates a problem with the Edge TTS service itself (e.g., rate limits, invalid voice, or temporary server issues).")
            print("Try a different VOICE or wait a bit before trying again.")
        elif "Error decoding audio with pydub" in str(e) or "ffmpeg" in str(e).lower():
            print("This usually means FFmpeg is not installed or not found in your system's PATH.")
            print("Please ensure FFmpeg is correctly installed and its 'bin' directory is added to your PATH environment variable.")
        print("Please ensure your microphone and speakers are working correctly, PyAudio is installed, AND FFmpeg is installed and in your system's PATH.")
    finally:
        # Always ensure the PyAudio stream is properly stopped and closed
        if stream:
            stream.stop_stream()
            stream.close()

# --- Main Assistant Loop ---
async def main_assistant_loop():
    # Initialize PyAudio once at the beginning of the application.
    # This instance will be used for all subsequent audio playback.
    p = pyaudio.PyAudio()

    print("\nSay 'exit' or 'quit' or 'goodbye' to end the conversation.")
    print("I'm listening...")

    try:
        while True:
            try:
                with sr.Microphone() as source:
                    # Listen for spoken input from the microphone.
                    audio = r.listen(source)

                # Recognize speech using Google Speech Recognition service.
                print("Recognizing your speech...")
                user_input = r.recognize_google(audio)
                print(f"You said: \"{user_input}\"")

                # Check if the user wants to exit the assistant.
                if user_input.lower() in ["exit", "quit", "goodbye"]:
                    await speak_text("Goodbye!", p) # Speak a farewell message
                    print("Exiting assistant. Goodbye!")
                    break # Exit the loop

                # Get a response from the AI assistant (pytgpt).
                print("Thinking...")
                ai_response = bot.chat(user_input)
                print(f"AI: {ai_response}")

                # Speak the AI's response using the direct streaming method.
                await speak_text(ai_response, p)

            except sr.UnknownValueError:
                # Handle cases where speech recognition couldn't understand the audio.
                print("Sorry, I could not understand audio. Please try again.")
                await speak_text("Sorry, I could not understand what you said. Please try again.", p)
            except sr.RequestError as e:
                # Handle errors related to connecting to the speech recognition service.
                print(f"Could not request results from Google Speech Recognition service; {e}")
                await speak_text("I'm having trouble connecting to the speech recognition service. Please check your internet connection.", p)
            except Exception as e:
                # Catch any other unexpected errors during the process.
                print(f"An unexpected error occurred: {e}")
                await speak_text("An unexpected error occurred. Please try again.", p)
            finally:
                # Prompt the user that the assistant is ready for the next input.
                print("\nI'm listening...")

    finally:
        # Ensure PyAudio is terminated gracefully when the application exits.
        if p:
            p.terminate()
            print("PyAudio terminated.")

# This block ensures the main asynchronous loop runs when the script is executed.
if __name__ == "__main__":
    try:
        asyncio.run(main_assistant_loop())
    except KeyboardInterrupt:
        print("\nAssistant stopped by user (Ctrl+C).")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error in main loop: {e}")
        sys.exit(1)
