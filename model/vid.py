from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
from gtts import gTTS
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
translator = pipeline('translation', model=model, tokenizer=tokenizer, max_length=400)


def extract_audio(path):
    video = VideoFileClip(path)
    audio_path = path + ".wav"
    video.audio.write_audiofile(audio_path)
    return audio_path

def split_video(input_path, chunk_duration):
    video = VideoFileClip(input_path)
    total_duration = video.duration
    chunks = []
    start_time = 0
    while start_time < total_duration:
        end_time = min(start_time + chunk_duration, total_duration)
        chunk = video.subclip(start_time, end_time)
        chunks.append(chunk)
        start_time = end_time
    return chunks

def extract_video(path):
    videoclip = VideoFileClip(path, audio=False)
    video_path = "output/Extractedvid" + ".mp4"
    videoclip.write_videofile(video_path)
    return video_path  

def merge(vid_path, audio_path):
    try:
        movie = VideoFileClip(vid_path).set_audio(AudioFileClip(audio_path))
        mergepath = "output/merged.mp4"
        movie.write_videofile(mergepath)
        print(mergepath)
        return mergepath
    except Exception as e:
        print("Error merging:", e)

def aud_text(path,s):
    r = sr.Recognizer()
    file = sr.AudioFile(path)
    with file as source:
        audio = r.record(source)
    dest = r.recognize_google(audio,language=s)
    print(dest)
    return(dest)

def text_text(text,src,tgt):
    translated = translator(text,src_lang=src, tgt_lang=tgt)
    print(translated[0]['translation_text'])
    return translated[0]['translation_text']

def text_to_speech(text, t):
    tts = gTTS(text=text, lang=t)
    tts.save("output.mp3")
    os.system("mpg123 output.mp3")  # Adjust this line according to your system's audio player
    return("output.mp3")
# Example usage


def main(vid_path, source_language, target_language):
    try:
        LANGUAGE_CODES = {
    "eng_Latn": "en",
    "tam_Taml": "ta",
    "hin_Deva": "hi",
    "mal_Mlym": "ml",
    "marathi": "mr",
    "tel_Telu": "te",
    "kan_Knda": "kn"
}   
        
        src=source_language
        tgt=target_language
        s = LANGUAGE_CODES.get(src)
        print(s)
        t=LANGUAGE_CODES.get(tgt)
        path = vid_path
        aud_path = extract_audio(path)
        recognition=aud_text(aud_path,s)
        translation=text_text(recognition,src,tgt)
        vid_path = extract_video(path)
        audio_path=text_to_speech(translation,t)
        a=merge(vid_path, audio_path)
        return a
    except Exception as e:
        print("Error:", e)
