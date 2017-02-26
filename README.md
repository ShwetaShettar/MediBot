# MediBot
##What It Does
MediBot has 2 components:
*  Alexa Skill with Twilio-SMS-Pregnancy
*  A based-Terminal text-to-speech and speech-to-text bot (was originally supposed to be on the pi)
Explanation for medical terminology was enabled in both

##Build
```python
pip install requirements.txt
```
You will require the following API keys

| API Name      | Purpose       
| ------------- |:-------------:| 
| Aylien SDK    | Text summarization and NLP |
| Twilio SDK    | To send SMS      |
| Microsoft Cognitive services| For TTS and STT |

##Usage
The following command will start the terminal chat-bot 
```python
python fml-ms.py
```
The following command will start the Alexa flask app
```python
python Quireir.py
```
Use ngrok and put the http link in Amazon Developer Program
For pregnancy_scraper.py, alyien.py use them like normal python classes

##What's next for MediBot
Expand the chatbot to support more medical advice for things like cancer, hernia etc
