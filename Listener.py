import speech_recognition as sr
from SpeechToText import stt_google
from main import AudioAssistant

things_said = ""
recent_things_said = ""
previous_things_said = ""


def your_mic_function():
    global things_said, recent_things_said, previous_things_said
    while True:
        print("listening")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # r.pause_threshold = 1

            # make the cutoff more aggressive, meaning as soon as someone stops talking end the recording
            r.energy_threshold = 4000
            r.dynamic_energy_threshold = False
            r.pause_threshold = 0.5
            r.adjust_for_ambient_noise(source, duration=1)

            audio = r.listen(source)
            # write audio to a WAV file
            with open("output_2.wav", "wb") as file:
                file.write(audio.get_wav_data())

        things_said += "\n" + stt_google("output_2.wav")

        recent_things_said = things_said[-200:]  # last 200 characters
        print(recent_things_said)

        if not previous_things_said == things_said:
            print("one")
            assistant = AudioAssistant()
            print("two")

            cut_in = assistant.run("Should I cut into conversation here? cut "
                                   "in if people ask questions or are stuck, but not if it is directed at someone "
                                   "specific."
                                   "Please say YES! or NO, and then respond. Make sure your response is less "
                                   "than 3 sentences, you don't want to hog up the conversation. If you respond NO!, "
                                   "respond with one sentence maximum. If the conversation seems too "
                                   "similar to the previous thing said, don't respond"
                                   "Conversation below:\n\n" + recent_things_said +
                                   "\n\nPrevious thing said: " + previous_things_said)

            print("cut_in: " + str(cut_in))

            previous_things_said = things_said


your_mic_function()

# print("stopped listening, now transcribing to text...")

# call wav to text
# print(stt_google("output_2.wav"))
