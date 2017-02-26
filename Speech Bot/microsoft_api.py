import requests
import uuid
import json
import wave
import io
import pyaudio
import settings
from urllib2 import Request, urlopen, URLError, HTTPError


def get_stt(accessToken,filename):
    f = open(filename, 'rb')
    flac_cont = f.read()
    f.close()


    sampleRate = "44100"
    url = "https://speech.platform.bing.com/recognize"
    qs = {
    'scenarios': 'ulm',
    'appid': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5', # This magic value is required
    'locale': 'en-US',
    'device.os': 'wp7',
    'version': '3.0',
    'format': 'json',
    'requestid': uuid.uuid4(),
    'instanceid': 'f7370be0-c9b3-46a6-bf6e-a7f6049a1aba'
    }
    payload = flac_cont

    headers = {
    'Authorization': 'Bearer ' + accessToken,
    'content-type': 'audio/wav; samplerate='+sampleRate + '; sourcerate='+sampleRate,
    'content-length' : str(len(flac_cont)),
    'cache-control': "no-cache",
    'postman-token': "955d09e1-9815-5753-38ee-97f97bf92733"
    }

    response = requests.request("POST", url, params=qs, data=payload, headers=headers)

    resp = json.loads(response.text)
    try:
        return resp['results'][0]['lexical']
    except KeyError:
        return "Sorry I could not process that"

def get_tts(accessToken,filename,text):
    ssmlPayload = "<speak version='1.0' xml:lang='en-us'><voice xml:lang='en-US' xml:gender='Male' name='Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)'>" + text + "</voice></speak>"

    url = 'https://speech.platform.bing.com/synthesize'
    body = ssmlPayload
    headers = {
      'Authorization': 'Bearer ' + accessToken,
      'content-type' : 'application/ssml+xml',
    #   // 'X-Microsoft-OutputFormat' : 'riff-8khz-8bit-mono-mulaw', uses mulaw encoding format
	  'X-Microsoft-OutputFormat' : 'raw-16khz-16bit-mono-pcm',
      'X-Search-AppId': settings.getProperty('X-Search-AppId'),
      'X-Search-ClientID': settings.getProperty('X-Search-ClientID'),
	  'User-Agent': 'Chat Robot',
      'cache-control': "no-cache",
      'postman-token': "955d09e1-9815-5753-38ee-97f97bf92733"
    }

    #response = requests.request("POST", url, data=payload,headers=headers)
    request = Request(url, data=body, headers=headers)
    response = urlopen(request)
    wav_data = response.read()

    #wav_data = response.text
    with io.BytesIO() as myfile:
        wav_writer = wave.open(filename, "wb")
        try:
            wav_writer.setframerate(16000)
            wav_writer.setsampwidth(2)
            wav_writer.setnchannels(1)
            wav_writer.writeframes(wav_data)
            #wav_data = filename.getvalue()
        finally:
            wav_writer.close()
    #print wav_data
    return



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

accessToken = response.text

def speak():
    #define stream chunk
    chunk = 1024

    #open a wav format music
    f = wave.open("output.wav","rb")
    #instantiate PyAudio
    p = pyaudio.PyAudio()
    #open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
    channels = f.getnchannels(),
    rate = f.getframerate(),
    output = True)
    #read data
    data = f.readframes(chunk)

    #play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

        #stop stream
    stream.stop_stream()
    stream.close()

        #close PyAudio
    p.terminate()

#get_tts(accessToken,'output.wav',"Hackillinois is the best hactkhon ever!!")

#print speak("sdfgdfg")
