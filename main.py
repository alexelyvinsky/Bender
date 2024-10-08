import requests
import pyaudio
import time
import threading
import queue
import tempfile
import soundfile as sf
from dotenv import load_dotenv
from openai import OpenAI
import os
import ollama
# import pyttsx3
import keyboard


class AudioAssistant:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()
        self.audio_generation_queue = queue.Queue()
        self.audio_playback_queue = queue.Queue()

        self.audio_generation_thread = threading.Thread(target=self.process_audio_generation_queue)
        self.audio_playback_thread = threading.Thread(target=self.process_audio_playback_queue)

        self.audio_generation_thread.start()
        self.audio_playback_thread.start()
        #self.is_speaking = False

        # self.engine = pyttsx3.init()
        # self.voices = self.engine.getProperty('voices')
        # self.engine.setProperty('voice', self.voices[1].id)

    def process_audio_generation_queue(self):
        while True:
            input_text = self.audio_generation_queue.get()
            if input_text is None:
                break
            audio_file_path = self.generate_audio(input_text)
            self.audio_playback_queue.put(audio_file_path)
            self.audio_generation_queue.task_done()

    def process_audio_playback_queue(self):
        while True:
            audio_file_path = self.audio_playback_queue.get()
            if audio_file_path is None:
                break
            self.play_audio(audio_file_path)
            self.audio_playback_queue.task_done()

    def generate_audio(self, input_text, model='tts-1', voice='alloy'):
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }
        data = {
            "model": model,
            "input": input_text,
            "voice": voice,
            "response_format": "opus",
        }
        with requests.post(url, headers=headers, json=data, stream=True) as response:
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.opus') as temp_file:
                    for chunk in response.iter_content(chunk_size=4096):
                        temp_file.write(chunk)
                    return temp_file.name
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

    def play_audio(self, audio_file_path):
        if audio_file_path:
            with sf.SoundFile(audio_file_path, 'r') as sound_file:
                self.audio = pyaudio.PyAudio()
                self.stream = self.audio.open(format=pyaudio.paInt16, channels=sound_file.channels, rate=sound_file.samplerate,
                                    output=True)
                data = sound_file.read(1024, dtype='int16')

                #self.is_speaking = True
                #while len(data) > 0 and self.is_speaking:
                while len(data) > 0:
                    self.stream.write(data.tobytes())
                    data = sound_file.read(1024, dtype='int16')

                    # Check if the Enter key is pressed
    #                 if keyboard.is_pressed('enter'):
    #                     self.stop_speaking()
    #
    #             self.stream.stop_stream()
    #             self.stream.close()
    #             self.audio.terminate()
    #
    # def stop_speaking(self):
    #     self.is_speaking = False

    def print_w_stream(self, message, memo):
        start_time = time.time()
        completion = self.client.chat.completions.create(
            model='gpt-4-turbo-preview',
            messages=[
                {"role": "system", "content": memo},
                {"role": "user", "content": message},
            ],
            stream=True,
            temperature=0,
            max_tokens=1000,
        )

        first_chunk_received = False
        sentences = []
        sentence = ''
        sentence_end_chars = {'.', '?', '!', '\n'}

        for chunk in completion:
            if not first_chunk_received:
                end_time = time.time()
                latency = end_time - start_time
                #print(f"Time taken to receive first chunk: {latency:.3f} seconds")
                first_chunk_received = True

            content = chunk.choices[0].delta.content
            if content:
                for char in content:
                    sentence += char
                    if char in sentence_end_chars:
                        sentence = sentence.strip()
                        if sentence and sentence not in sentences:
                            sentences.append(sentence)
                            # if "YES!" in sentences[0]:
                            #     if "YES!" not in sentence:
                            # print(f"Queued sentence: {sentence}")
                            self.audio_generation_queue.put(sentence)
                        sentence = ''
        return sentences

    def print_w_stream_local(self, message, memo):
        start_time = time.time()
        completion = ollama.chat(
            model='llama2-uncensored',  # mistral
            messages=[
                {"role": "system", "content": memo},
                {"role": "user", "content": message},
            ],
            stream=True,
        )
        first_chunk_received = False
        sentences = []
        sentence = ''
        sentence_end_chars = {'.', '?', '!', '\n'}

        for chunk in completion:
            if not first_chunk_received:
                end_time = time.time()
                latency = end_time - start_time
                print(f"Time taken to receive first chunk: {latency:.3f} seconds")
                first_chunk_received = True

            content = chunk['message']['content']
            if content:
                for char in content:
                    sentence += char
                    if char in sentence_end_chars:
                        sentence = sentence.strip()
                        if sentence and sentence not in sentences:
                            sentences.append(sentence)
                            # if "YES!" in sentences[0]:
                            #     if "YES!" not in sentence:
                            # print(f"Queued sentence: {sentence}")
                            self.audio_generation_queue.put(sentence)
                            # self.engine.say(sentence)
                            # self.engine.runAndWait()
                        sentence = ''
        return sentences

    def cleanup_queues(self):
        self.audio_generation_queue.join()
        self.audio_generation_queue.put(None)
        self.audio_playback_queue.join()
        self.audio_playback_queue.put(None)

    def run(self, user_input, memo="You are an assistant."):
        # start_time = time.time()
        # out = self.print_w_stream(user_input, memo)
        # change to print_w_stream_local to use local model
        out = self.print_w_stream(user_input, memo)
        self.cleanup_queues()
        self.audio_generation_thread.join()
        self.audio_playback_thread.join()
        return out

# if __name__ == "__main__":
#     assistant = AudioAssistant()
#     user_input = input("What do you want to ask the AI? ")
#     assistant.run(user_input)
