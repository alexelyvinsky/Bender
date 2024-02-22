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
            audio = r.listen(source)
            # write audio to a WAV file
            with open("output_2.wav", "wb") as file:
                file.write(audio.get_wav_data())

        things_said += "\n" + stt_google("output_2.wav")

        recent_things_said = things_said[-200:]  # last 200 characters
        print(recent_things_said)

        print("one")
        assistant = AudioAssistant()
        print("two")

        cut_in = assistant.run("Should I cut into conversation here? cut "
                               "in if people ask questions or are stuck. Please say YES! or NO. only. "
                               "Conversation below:\n" + recent_things_said)

        print(cut_in)

        # check if cut_in[0] exists and then if it is "YES!"
        if cut_in and cut_in[0] == "YES!":
            print("three")
            assistant = AudioAssistant()
            out = assistant.run("Participate in conversation:\n" + recent_things_said, play_output=True)
            print("four")
            print(out)


your_mic_function()

# print("stopped listening, now transcribing to text...")

# call wav to text
# print(stt_google("output_2.wav"))
