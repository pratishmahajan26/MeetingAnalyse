import os
import speech_recognition as sr
#from tqdm import tqdm
import argparse
import io
from google.cloud import speech_v1p1beta1 as speech
from multiprocessing.dummy import Pool
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Pratish/Documents/api-key.json"

pool = Pool(8)  # Number of concurrent threads


with open("C:/Users/Pratish/Documents/api-key.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

print(GOOGLE_CLOUD_SPEECH_CREDENTIALS)
r = sr.Recognizer()
files = os.listdir('C:/Users/Pratish/Documents/Free Sound Recorder/parts/')

def transcribe_file_with_auto_punctuation(path):
    """Transcribe the given audio file with auto punctuation enabled."""
    client = speech.SpeechClient()

    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Enable automatic punctuation
        enable_automatic_punctuation=True)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print('Transcript: {}'.format(alternative.transcript))
# [END speech_transcribe_file_with_auto_punctuation]

def transcribe(data):

    idx, file = data
    name = "C:/Users/Pratish/Documents/Free Sound Recorder/parts/" + file
    #print(name + " started")
    # Load audio file
    #with sr.AudioFile(name) as source:
        #audio = r.record(source)

    client = speech.SpeechClient()
    with io.open(name, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code='en-US',
        # Enable automatic punctuation
        enable_automatic_punctuation=True)


    # [END speech_transcribe_file_with_auto_punctuation]

    try:
        response = client.recognize(config, audio)

        for i, result in enumerate(response.results):
            alternative = result.alternatives[0]
            print('-' * 20)
            print('First alternative of result {}'.format(i))
            print('Transcript: {}'.format(alternative.transcript))
        # Transcribe audio file
        #text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print(name + " done")
        return {
            "idx": idx,
            "text": text
        }
    except sr.UnknownValueError:
        return {
            "idx": idx,
            "text": ""
        }


all_text = pool.map(transcribe, enumerate(files))
pool.close()
pool.join()


transcript = ""
only_text = []
for t in sorted(all_text, key=lambda x: x['idx']):
    total_seconds = t['idx'] * 30
    # Cool shortcut from:
    # https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
    # to get hours, minutes and seconds
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)
    only_text.append(t['text'])
    # Format time as h:m:s - 30 seconds of text
    transcript = transcript + "{:0>2d}:{:0>2d}:{:0>2d} {}\n".format(h, m, s, t['text'])

print(transcript)
text = ""
for t in only_text:
    text = str(text) + " " + str(t)
print("=============>"+text)
with open("transcript.txt", "w") as f:
    f.write(transcript)
