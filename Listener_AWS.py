import asyncio
import time

# This example uses the sounddevice library to get an audio stream from the
# microphone. It's not a dependency of the project but can be installed with
# `python -m pip install amazon-transcribe aiofile`
# `pip install sounddevice`.

import sounddevice
from dotenv import load_dotenv
from main import AudioAssistant
from threading import Thread

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

"""
Here's an example of a custom event handler you can extend to
process the returned transcription results as needed. This
handler will simply print the text out to your interpreter.
"""

# global vars
things_said = ""
recent_things_said = ""
previous_things_said = ""
everything_said_aws = ""
temp_things = ""


def read_from_file(file_name):
    with open(file_name, "r") as file:
        return file.read()


my_work_memo = read_from_file("memo.txt")
load_dotenv()


def callback():  # this is called from the background thread
    global recent_things_said, everything_said_aws, my_work_memo, temp_things
    try:
        recent_things_said = everything_said_aws[-10000:]  # last 200 characters

        # trigger word
        if any(word.lower() in temp_things.lower() for word in ['Bender', 'bender']):
            assistant = AudioAssistant()

            # Wait for the previous audio to finish playing
            #assistant.audio_playback_thread.join()

            cut_in = assistant.run("You are a participant in this meeting, your name is Lenz or Lens. "
                                   "It is vital that you keep your responses relevant to the conversation and the memo"
                                   "speak as concisely as possible. Seriously, keep your responses to a minimum"
                                   "Do not say your name in your responses\n\n"
                                   "Conversation below:\n\n" + recent_things_said, my_work_memo)

            # print("cut_in: " + str(cut_in))
    except:
        pass


class MyEventHandler(TranscriptResultStreamHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_transcript = ""
        self.stt_start_time = None

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        global everything_said_aws, temp_things
        for result in results:
            if not result.is_partial:
                for alt in result.alternatives:
                    transcript = alt.transcript
                    print("\n" + transcript)
                    everything_said_aws += "\n\n" + transcript
                    temp_things = transcript
                    mythread = Thread(target=callback)
                    mythread.start()


async def mic_stream():
    # This function wraps the raw input stream from the microphone forwarding
    # the blocks to an asyncio.Queue.
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def callback_thread(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))

    # Be sure to use the correct parameters for the audio stream that matches
    # the audio formats described for the source language you'll be using:
    # https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html
    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=16000,
        callback=callback_thread,
        blocksize=1024 * 2,
        dtype="int16",
    )
    # Initiate the audio stream and asynchronously yield the audio chunks
    # as they become available.
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status


async def write_chunks(stream):
    # This connects the raw audio chunks generator coming from the microphone
    # and passes them along to the transcription stream.
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()


async def basic_transcribe():
    # Setup up our client with our chosen AWS region
    client = TranscribeStreamingClient(region="us-east-1")

    # Start transcription to generate our async stream
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm"
    )

    # Instantiate our handler and start processing events
    handler = MyEventHandler(stream.output_stream)
    print("Listening...")
    await asyncio.gather(write_chunks(stream), handler.handle_events())


loop = asyncio.get_event_loop()
loop.run_until_complete(basic_transcribe())
loop.close()
