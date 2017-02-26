# MediBot
##What It Does
MediBot has 2 components:
1.  Alexa Skill with Twilio-SMS-Pregnancy
2.  A based-Terminal text-to-speech and speech-to-text bot (was originally supposed to be on the pi)
Explanation for medical terminology was enabled in both

##How We Built It
We first worked on making a wrapper for the Microsoft Cognitive services TTS and STT API. We then worked with text analysis API like Aylien to summarize the ton of text we got from scraping Wikipedia and DBpedia. Then we added the Alexa skill and finally the pregnancy advice and Twilio SMS.

##Challenges We Ran Into
Microsoft did not have wrappers or SDKs or proper (python) docs for calling their API. So we spent the good portion of an 8hrs building and implementation our own TTS and STT for the bot. Thanks to the Facebook and Microsoft mentors for helping us out with this

##Accomplishments that we're proud of
A working Microsoft Conversation wrapper for python :). Also making our extremely rudimentary terminal Chatbot

##What we learned
Open-source projects with poor documentation are a pain-in-the-a**. Also, using new Text Analysis APIs like Aylien.

##What's next for MediBot
Expand the chatbot to support more medical advice for things like cancer, hernia etc

##All Dependencies Listed under Requirements.txt
