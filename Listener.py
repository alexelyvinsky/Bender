import speech_recognition as sr
from main import AudioAssistant
import time

# global vars
things_said = ""
everything_said = ""
recent_things_said = ""
previous_things_said = ""


def read_from_file(file_name):
    with open(file_name, "r") as file:
        return file.read()


def callback(recognizer, audio):  # this is called from the background thread
    try:
        global things_said, recent_things_said, \
            previous_things_said, everything_said, my_work_memo

        try:
            # temp_things = stt_google(audio_data)  # Process the audio chunk directly
            temp_things = r.recognize_google(audio)

            things_said += "\n" + temp_things
            everything_said += "\n" + temp_things

            # recent_things_said = things_said[-10000:]  # last 200 characters

            # this involves both users and assistant speech
            recent_things_said = everything_said[-10000:]  # last 200 characters
            # print(recent_things_said)
            print(temp_things)

            if not previous_things_said == things_said and 'Lens' in temp_things or 'lens' in temp_things:
                assistant = AudioAssistant()

                cut_in = assistant.run("You are an active participant in this meeting. "
                                       "Please provide your thoughts/insights based on the memo "
                                       "and the recent things said in the meeting. Keep your responses brief, "
                                       "less than 3 sentences.\n\n"
                                       "Conversation below:\n\n" + recent_things_said, my_work_memo)

                print("cut_in: " + str(cut_in))

                previous_things_said = things_said

                # join cut_in into a string, but eliminate the 0th element
                cut_in_str = " ".join(cut_in)

                everything_said += "\n" + cut_in_str

        except sr.UnknownValueError:
            print("Audio could not be understood")
        except sr.RequestError as e:
            print("Error from STT service; {0}".format(e))

    except LookupError:
        print("Oops! Didn't catch that")


my_work_memo = read_from_file("memo.txt")

r = sr.Recognizer()
print("Listening...")
r.listen_in_background(sr.Microphone(), callback)

while True: time.sleep(0.1)  # we're still listening even though the main thread is blocked
