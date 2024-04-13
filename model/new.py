import threading
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
import time
import os

thrnamelist=[]


def aud_text(path,s):
    r = sr.Recognizer()
    file = sr.AudioFile(path)
    with file as source:
        audio = r.record(source)
    dest = r.recognize_google(audio,lang=s)
    return dest

def extract_audio(subclip_path):
    audio_path = subclip_path + ".wav"
    subclip = VideoFileClip(subclip_path)
    subclip.audio.write_audiofile(audio_path)
    return audio_path

# Initialize a lock to ensure thread safety
#lock = threading.Lock() 

def add_text(audio_path, recognized_texts,s,t):
    """
    Recognize speech from the extracted audio and add it to the list of recognized texts.
    """
    # not using locks as my program do not use any internal variables everything used are from stack so my code is thread safe
    # Acquire the lock to ensure thread safety
    #print("going to aqu lock")
    #lock.acquire()
    #print("got locl")
    try:
        # Recognize speech from the extracted audio
        # Append the recognized text to the list

        print("sending data to google...")
        recognized_texts.append(aud_text(audio_path,s))

        # Cleanup: remove the extracted audio file after use
        os.remove(audio_path)
    except Exception as e:
        print("exception", e)
        exit()
    finally:
        # Release the lock
      #  print("release of lock")
        #lock.release()
        print("google is done, removeing ", threading.current_thread().name)
        thrnamelist.remove(threading.current_thread().name)
        
    

def split_video_into_chunks_with_audio(video_path, chunk_duration,s,t):
    print("before loading")
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    print("clip loaded")
    # Subdivide the video into chunks
    num_chunks = int(video_clip.duration / chunk_duration)
    
    # Initialize an empty list to store recognized texts
    recognized_texts = []

    # Create the output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    # Iterate over each chunk
    for i in range(num_chunks):
        start_time = i * chunk_duration
        end_time = min((i + 1) * chunk_duration, video_clip.duration)

        # Extract the subclip
        subclip = video_clip.subclip(start_time, end_time)
        subclip_path = os.path.join(output_dir, f"chunk_{i}.mp4")

        # Export the subclip
        subclip.write_videofile(subclip_path, codec="libx264", audio_codec="aac")

        # Extract audio from the subclip
        audio_path = extract_audio(subclip_path)
        print("extract audio done for itr",i)
        
        # Create a new thread to recognize speech from the extracted audio
        thread = threading.Thread(target=add_text, name="crazy"+str(i),args=(audio_path, recognized_texts,s,t))
        print("starting thread",thread.name)
        thrnamelist.append(thread.name)
        thread.start()
    
    numberofthreads=num_chunks
    # Wait for all threads to finish
    print("goint to wait for threads")
      # Wait for all threads to finish
   # Wait for all tasks to finish
    print("goint to wait for tasks")

    while(len(thrnamelist)!=0):
        time.sleep(1)      
        print("waiting")
    print("done waiting")
    # Join all recognized texts into one
    combined_text = ' '.join(recognized_texts)
    print(combined_text)


    return combined_text

def main(vid_path, source_language, target_language):
    start = time.time()
    LANGUAGE_CODES = {
    "eng_Latn": "en",
    "tam_Taml": "ta",
    "hin_Deva": "hi",
    "mal_Mlym": "ml",
    "marathi": "mr",
    "tel_Telu": "te",
    "kan_Knda": "kn"
}   
    print(time.time())
    src=source_language
    tgt=target_language
    s = LANGUAGE_CODES.get(src.lower())
    t=LANGUAGE_CODES.get(tgt.lower())
    print("before split_video_into_chunks_with_audio")
    mid=time.time()
    src=source_language
    tgt=target_language
# Example usage:
    # video_path = "1.mp4"
    chunk_duration = 5  # seconds
    print(time.time()-mid)
    combined_text = split_video_into_chunks_with_audio(vid_path, chunk_duration,s,t)
    print("after split_video_into_chunks_with_audio...",combined_text)
    print(time.time()-mid)
    mid = time.time()
    return combined_text