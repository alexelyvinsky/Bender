# Audio Assistant with AWS Transcribe and OpenAI Integration

## Overview
This project is an audio assistant that listens to microphone input, transcribes it using AWS Transcribe, and provides responses via OpenAI's GPT model. It also generates audio responses and plays them back. The assistant is capable of handling live conversations, detecting trigger words, and providing concise responses based on a provided memo or context.

## Features
- **Real-time transcription**: Uses AWS Transcribe for converting speech to text.
- **Trigger-based response**: Activates specific responses based on keywords like "Bender" or "bender".
- **AI-generated responses**: Utilizes OpenAI's GPT model for generating conversational responses based on the provided transcription.
- **Audio playback**: Converts AI responses to speech and plays them back.
- **Supports multiple AI backends**: Can switch between OpenAI's API or a local LLaMA-based model for generating responses.

## Prerequisites
- **Python 3.7+**
- **AWS Credentials**: Set up with Transcribe permissions.
- **OpenAI API Key**: Required for interaction with OpenAI's API.
- **Required Python libraries**:
  - `sounddevice`
  - `amazon-transcribe`
  - `aiofile`
  - `requests`
  - `pyaudio`
  - `soundfile`
  - `ollama` (optional, for local LLaMA models)
  - `dotenv`
  - `keyboard` (optional for controlling speech stop)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/audio-assistant.git
   cd audio-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory of the project with the following variables:
     ```
     OPENAI_API_KEY=<your-openai-api-key>
     AWS_ACCESS_KEY_ID=<your-aws-access-key>
     AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
     ```

4. Set up AWS credentials:
   Ensure that your AWS credentials are set up to allow Transcribe access. This can be done via `~/.aws/credentials` or by setting environment variables directly.

5. Install the sounddevice library if not already installed:
   ```bash
   pip install sounddevice
   ```

## Usage

### Running the Assistant
To start the assistant and begin transcribing microphone input, run the following command:

```bash
python main.py
```

The assistant will listen for trigger words like "Bender" to activate and respond accordingly. The responses are generated based on a memo read from `memo.txt`, ensuring they stay relevant to the context.

### Adding Custom Responses
You can modify the `callback()` function to change the assistant's behavior when a trigger word is detected.

### Using the Local LLaMA Model
To switch to using the local LLaMA model for response generation, modify the following line in `AudioAssistant.run`:

```python
out = self.print_w_stream_local(user_input, memo)
```

### Stopping Audio Playback
You can optionally enable the `keyboard` module to stop the audio playback by pressing the Enter key. Uncomment the related code under `play_audio()` for this functionality.

## File Structure
- `main.py`: The core application logic, handles transcription and triggers the audio assistant.
- `AudioAssistant`: Handles the generation and playback of AI-generated responses.
- `memo.txt`: A file that contains the context or memo for the assistant to base its responses on.
- `.env`: Contains environment variables like OpenAI API key and AWS credentials.

## Contributing
Feel free to fork this repository and submit pull requests. Please ensure all major changes are tested before submission.

## License
This project is licensed under the MIT License.
