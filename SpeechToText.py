from google.cloud import speech
import os

credential_path = "spry-sensor-353919-74cb50cc75e3.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def speech_to_text(
        config: speech.RecognitionConfig,
        audio: speech.RecognitionAudio,
) -> speech.RecognizeResponse:
    client = speech.SpeechClient()

    # Synchronous speech recognition request
    response = client.recognize(config=config, audio=audio)

    return response


def print_response(response: speech.RecognizeResponse):
    for result in response.results:
        print_result(result)


def print_result(result: speech.SpeechRecognitionResult):
    best_alternative = result.alternatives[0]
    print("-" * 80)
    print(f"language_code: {result.language_code}")
    print(f"transcript:    {best_alternative.transcript}")
    print(f"confidence:    {best_alternative.confidence:.0%}")


def stt_google(wav_file):
    config = speech.RecognitionConfig(language_code="en", )

    with open(wav_file, 'rb') as audio_file:
        audio_data = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_data)

    try:
        response = speech_to_text(config, audio)
        out = response.results[0].alternatives[0].transcript
    except Exception:
        out = ""
    return out

