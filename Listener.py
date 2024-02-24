import speech_recognition as sr
from SpeechToText import stt_google
from main import AudioAssistant

# global vars
things_said = ""
everything_said = ""
recent_things_said = ""
previous_things_said = ""


def read_from_file(file_name):
    with open(file_name, "r") as file:
        return file.read()


def your_mic_function(my_mic_work_memo):
    global things_said, recent_things_said, \
        previous_things_said, everything_said
    while True:
        print("listening")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # r.pause_threshold = 1

            # make the cutoff more aggressive, meaning as soon as someone stops talking end the recording
            # r.energy_threshold = 4000
            # r.dynamic_energy_threshold = False
            # r.pause_threshold = 0.5
            # r.adjust_for_ambient_noise(source, duration=1)

            audio = r.listen(source)
            # write audio to a WAV file
            with open("output_2.wav", "wb") as file:
                file.write(audio.get_wav_data())

        temp_things = stt_google("output_2.wav")

        things_said += "\n" + temp_things
        everything_said += "\n" + temp_things

        # recent_things_said = things_said[-10000:]  # last 200 characters

        # this involves both users and assistant speech
        recent_things_said = everything_said[-10000:]  # last 200 characters
        # print(recent_things_said)
        print(temp_things)

        if not previous_things_said == things_said and 'Lens' in temp_things or 'lens' in temp_things:
            assistant = AudioAssistant()

            # cut_in = assistant.run("Should I cut into conversation here? cut "
            #                        "in if people ask questions or are stuck, but not if it is directed at someone "
            #                        "specific. If directed at 'Lenz' or 'Lenzbot', then cut in."
            #                        "Please say YES! or NO, and then respond. Make sure your response is less "
            #                        "than 3 sentences, you don't want to hog up the conversation. If you respond NO!, "
            #                        "respond with one sentence maximum. If the conversation seems too "
            #                        "similar to the previous thing said, don't respond"
            #                        "Conversation below:\n\n" + recent_things_said +
            #                        "\n\nPrevious thing said: " + previous_things_said)

            cut_in = assistant.run("You are an active participant in this meeting. "
                                   "Please provide your thoughts/insights based on the memo "
                                   "and the recent things said in the meeting. Keep your responses brief.\n\n"
                                   "Conversation below:\n\n" + recent_things_said, my_mic_work_memo)

            print("cut_in: " + str(cut_in))

            previous_things_said = things_said

            # join cut_in into a string, but eliminate the 0th element
            cut_in_str = " ".join(cut_in)

            everything_said += "\n" + cut_in_str


if __name__ == "__main__":
    my_work_memo = read_from_file("memo.txt")
    your_mic_function(my_work_memo)

    # print("stopped listening, now transcribing to text...")

    # call wav to text
    # print(stt_google("output_2.wav"))
