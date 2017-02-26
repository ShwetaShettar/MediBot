import pyaudio
import wave
import audioop
from collections import deque
import os
import urllib2
import urllib
import time
import math
#import sample_wave
import requests
import term_search_aylien
import uuid
import json
import microsoft_api
import settings
import sys
import time
import wave
import enchant
from termcolor import colored, cprint

url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"

payload = ""
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'content-length': "0",
    'ocp-apim-subscription-key': settings.getProperty('ocp-apim-subscription-key'),
    'cache-control': "no-cache",
    'postman-token': "955d09e1-9815-5753-38ee-97f97bf92733"
    }

response = requests.request("POST", url, data=payload, headers=headers)

ACCESS_TOKEN = response.text

LANG_CODE = 'en-US'  # Language to use

d = enchant.Dict("en_US")


# Microphone stream config.
CHUNK = 1024  # CHUNKS of bytes to read each time from mic
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 2500  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).

SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.

PREV_AUDIO = 0.7  # Previous audio (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded audio is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.

EXIT_COMMANDS = ["quit","close","exit","end","shut up","shut down","goodbye","fuck off"]



def say(word,filename):
    microsoft_api.get_tts(ACCESS_TOKEN,"output.wav",str(word))
    microsoft_api.speak()
    try:
        os.remove(filename)
    except:
        pass

def listen_for_speech(threshold=THRESHOLD, num_phrases=-1):
    """
    Listens to Microphone, extracts phrases from it and sends it to
    Google's TTS service and returns response. a "phrase" is sound
    surrounded by silence (according to threshold). num_phrases controls
    how many phrases to process before finishing the listening process
    (-1 for infinite).
    """

    #Open stream
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print "* Listening mic. " + u'\U00031F50A' + ' '
    #return

    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    slid_win = deque(maxlen=SILENCE_LIMIT * rel)
    #Prepend audio from 0.5 seconds before noise was detected
    prev_audio = deque(maxlen=PREV_AUDIO * rel)
    started = False
    n = num_phrases
    response = []

    while (num_phrases == -1 or n > 0):
        cur_data = stream.read(CHUNK)

        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))

        if(sum([x > THRESHOLD for x in slid_win]) > 0):
            if(not started):
                print "Starting record of phrase"
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            print "Finished"

            # The limit was reached, finish capture and deliver.
            filename = save_speech(list(prev_audio) + audio2send, p)

            stream.stop_stream()

            r = microsoft_api.get_stt(ACCESS_TOKEN,filename)
            cprint("You: " + r, 'green', attrs=['bold'], file=sys.stderr)



            if r in EXIT_COMMANDS:
                cprint("Bot: Bye, Have a nice day!", 'red', attrs=['bold'], file=sys.stderr)
                say("Bye, Have a nice day!",filename)
                break
            else:
                # send response here
                txt = term_search_aylien.search_medical_term(r)
                say_lst = []

                for i in range(0,len(txt),255):
                    new_say = txt[i:i+255]
                    say(new_say,filename)
                cprint("Bot: " + r, 'red', attrs=['bold'], file=sys.stderr)


            stream.start_stream()
            # if num_phrases == -1:
            #     cprint(r, 'red', attrs=['bold'], file=sys.stderr)
            # else:
            #     response.append(r)

            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT * rel)
            prev_audio = deque(maxlen=0.5 * rel)
            audio2send = []
            n -= 1
            print "Listening ..."
        else:
            prev_audio.append(cur_data)

    print "* Done recording"
    stream.close()
    p.terminate()


    return response


def save_speech(data, p):
    """ Saves mic data to temporary WAV file. Returns filename of saved
        file """

    filename = 'output_'+str(int(time.time()))
    # writes data to WAV file
    data = ''.join(data)
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)  # TODO make this value a function parameter?
    wf.writeframes(data)
    wf.close()
    return filename + '.wav'


# def stt_google_wav(audio_fname):
#     """ Sends audio file (audio_fname) to Google's text to speech
#         service and returns service's response. We need a FLAC
#         converter if audio is not FLAC (check FLAC_CONV). """
#
#     print "Sending ", audio_fname
#     # #Convert to flac first
#     filename = audio_fname
#     del_flac = False
#     if 'flac' not in filename:
#         del_flac = True
#         print "Converting to flac"
#         print FLAC_CONV + filename
#         os.system(FLAC_CONV + ' ' + filename)
#         filename = filename.split('.')[0] + '.flac'
#
#     f = open(filename, 'rb')
#     flac_cont = f.read()
#     f.close()
#
#
#
#     # Headers. A common Chromium (Linux) User-Agent
#     hrs = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7",
#            'Content-type': 'audio/x-flac; rate=16000'}
#
#     req = urllib2.Request(GOOGLE_SPEECH_URL, data=flac_cont, headers=hrs)
#     print "Sending request to Google TTS"
#     #print "response", response
#     try:
#         p = urllib2.urlopen(req)
#         response = p.read()
#         res = eval(response)['hypotheses']
#     except:
#         print "Couldn't parse service response"
#         res = None
#
#     if del_flac:
#         os.remove(filename)  # Remove temp file
#
#     return ret


if(__name__ == '__main__'):
    n  = 6 - 2
    m = 20 - 2
    a = u'\U0001F3E5' + ' '
    b = u'\U0001F916' + ' '
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*10 + a*12
    print  " "*10 + a*12
    print  " "*10 + a*12
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    print  " "*m + a*n
    #
    c = u'\U0001F489' + ' '
    d = u'\U0001F48A' + ' '
    cprint(" "*10 + b + " Hey! Welcome to MediBot " + b, 'red', file=sys.stderr)
    say("Hey!Welcome to MediBot","")
    cprint(c + d + " MediBot is everyone's go to bot for medical terminology " + c + d, 'red', file=sys.stderr)
    say("MediBot is everyone's go to bot for medical terminology","")
    say("Go ahead, Ask something we're listening","")
    listen_for_speech()  # listen to mic.
    #print stt_google_wav('hello.flac')  # translate audio file
    #audio_int()  # To measure your mic levels
