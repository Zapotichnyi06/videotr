import os
import ssl
import logging
import yt_dlp as youtube_dl
import ffmpeg
import speech_recognition as sr
import deepl
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import certifi
from pydub import AudioSegment
from pydub.silence import split_on_silence
from django.shortcuts import render
from django.conf import settings

logging.basicConfig(level=logging.INFO)

os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

ssl._create_default_https_context = ssl._create_unverified_context
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


deepl_auth_key = 'Your API'  #API key
deepl_translator = deepl.Translator(deepl_auth_key)

def download_video(url, path="video.mp4"):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': path,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    logging.info(f"Видео загружено: {path}")
    return path

def extract_audio(video_path, audio_path="audio.wav"):
    logging.info(f"Извлечение аудио из видео: {video_path}")
    ffmpeg.input(video_path).output(audio_path).run()
    logging.info(f"Аудио извлечено: {audio_path}")

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    logging.info(f"Распознанный текст: {text}")
    return text

def translate_text(text, dest_language="ru"):
    result = deepl_translator.translate_text(text, target_lang=dest_language)
    translation = result.text
    logging.info(f"Переведенный текст: {translation}")
    return translation

def text_to_speech(text, audio_path="translated_audio.mp3"):
    logging.info(f"Синтез речи: {text}")
    tts = gTTS(text=text, lang="ru")
    tts.save(audio_path)
    logging.info(f"Синтезированный аудио файл: {audio_path}")
    return audio_path

def create_new_video(original_video_path, new_audio_path, output_path):
    logging.info(f"Создание нового видео с озвучкой")
    video = VideoFileClip(original_video_path)
    audio = AudioFileClip(new_audio_path)
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    logging.info(f"Новое видео создано: {output_path}")

def process_video(url):
    video_path = download_video(url)
    audio_path = "audio.wav"
    extract_audio(video_path, audio_path)

    sound = AudioSegment.from_wav(audio_path)
    chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-40, keep_silence=250)

    translated_audio_path = os.path.join(settings.MEDIA_ROOT, "translated_audio.mp3")
    full_translated_text = ""

    for i, chunk in enumerate(chunks):
        chunk_path = f"chunk{i}.wav"
        chunk.export(chunk_path, format="wav")
        recognizer = sr.Recognizer()
        with sr.AudioFile(chunk_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                if text.strip():  # Проверяем, что текст не пустой
                    logging.info(f"Распознанный текст из {chunk_path}: {text}")
                    translated_text = translate_text(text)
                    full_translated_text += translated_text + " "
                else:
                    logging.warning(f"Пустой текст из {chunk_path}")
            except sr.UnknownValueError:
                logging.warning(f"Не удалось распознать текст из {chunk_path}")
            except sr.RequestError as e:
                logging.error(f"Ошибка сервиса Google Speech Recognition; {e}")

        os.remove(chunk_path)

    text_to_speech(full_translated_text, translated_audio_path)

    output_video_path = os.path.join(settings.MEDIA_ROOT, "new_video.mp4")
    create_new_video(video_path, translated_audio_path, output_video_path)
    return output_video_path

def index(request):
    default_url = "https://www.youtube.com/watch?v=AKJfakEsgy0&t=4s"
    return render(request, 'translate/form.html', {'default_url': default_url})

def process_video_view(request):
    url = request.GET.get('url', 'https://www.youtube.com/watch?v=AKJfakEsgy0&t=4s')
    if url:
        try:
            output_path = process_video(url)
            relative_output_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
            output_url = settings.MEDIA_URL + relative_output_path
            logging.info(f"Видео обработано успешно: {output_url}")
            return render(request, 'translate/form.html', {'output': output_url, 'default_url': url})
        except Exception as e:
            logging.error(f"Ошибка при обработке видео: {str(e)}", exc_info=True)
            return render(request, 'translate/form.html', {'error': str(e), 'default_url': url})
    else:
        return render(request, 'translate/form.html', {'error': 'No URL provided', 'default_url': url})