import speech_recognition as sr
from SpeechToText import stt_google
from main import AudioAssistant

things_said = ""
recent_things_said = ""


def your_mic_function():
    global things_said, recent_things_said
    while True:
        print("listening")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # r.pause_threshold = 1
            audio = r.listen(source
            # write audio to a WAV file
            with open("output_2.wav", "wb") as file:
                file.write(audio.get_wav_data())

        things_said += "\n" + stt_google("output_2.wav")

        print(recent_things_said)
        recent_things_said = things_said[-100:]  # last 100 characters

        assistant = AudioAssistant()
        cut_in = assistant.run("Should I cut into conversation here? Please say YES! or NO. only. "
                               "Conversation below:\n" + recent_things_said)

        print(cut_in)

        # if cut_in[0] == "YES!":
        #     print("made it")


your_mic_function()

# print("stopped listening, now transcribing to text...")

# call wav to text
# print(stt_google("output_2.wav"))
