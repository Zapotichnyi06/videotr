# Video Translation and Dubbing Project

This project is a Django application for translating and dubbing YouTube videos using DeepL and Google Text-to-Speech (gTTS). It downloads a video, extracts the audio, translates the speech, and creates a new video with dubbed audio in a different language.

## Features

- Download YouTube videos
- Extract audio from videos
- Transcribe audio to text using Google Speech Recognition
- Translate text using DeepL API
- Synthesize speech using gTTS
- Create new video with dubbed audio

## Requirements

- Python 3.8+
- Django 5.0.6
- yt-dlp
- ffmpeg
- speechrecognition
- deepl
- gtts
- moviepy
- pydub
- python-decouple

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/videotr.git
    cd videotr
    ```

2. **Create a virtual environment and activate it**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply database migrations**:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser for the Django admin**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

7. **Open your browser and go to `http://127.0.0.1:8000/translate/` to use the application**.

## Usage

1. **Go to the Translate page**:

    Navigate to `http://127.0.0.1:8000/translate/`.

2. **Enter the YouTube video URL**:

    Enter the URL of the YouTube video you want to translate and dub.

3. **Submit the form**:

    Click the "Submit" button to start the translation and dubbing process.

4. **Download the new video**:

    After the process is complete, a link to download the new video with the dubbed audio will be provided.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

