# -*- coding: utf-8 -*-

pregeers_file = open("pregnancy.txt","r")
# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

# Find these values at https://twilio.com/user/account
account_sid = "" #TODO
auth_token = ""#TODO
client = TwilioRestClient(account_sid, auth_token)



def first_trimester_todo():
    todo = pregeers_file.readline().split(", ")
    body = "Here is a checklist to follow for your first trimester" + "\n"
    for e in todo:
        body += str(todo.index(e) + 1)+".\t" + e + "\n"
    body = body + "Happy pregnancy " + u'\U0001F6BC' + ' ' + u'\U0001F6BC' + ' ' + u'\U0001F6BC'
    message = client.messages.create(to="(650) 995-2455", from_="(504) 434-7749", body=body)

def second_trimester_todo():
    pregeers_file.readline()
    todo = pregeers_file.readline()
    todo = todo.split(", ")
    body = "Here is a checklist to follow for your second trimester" + "\n"
    for e in todo:
        body += str(todo.index(e) + 1)+".\t" + e + "\n"
    body = body + "Happy pregnancy " + u'\U0001F476' + ' ' + u'\U0001F476' + ' ' + u'\U0001F476'
    message = client.messages.create(to="(650) 995-2455", from_="(504) 434-7749", body=body)
def third_trimester_todo():
    pregeers_file.readline()
    pregeers_file.readline()
    todo = pregeers_file.readline()
    todo = todo.split(", ")
    body = "Here is a checklist to follow for your third trimester" + "\n"
    for e in todo:
        body += str(todo.index(e) + 1)+".\t" + e + "\n"
    body = body + "Happy pregnancy " + u'\U0001F37C' + ' ' + u'\U0001F37C' + ' ' + u'\U0001F37C'
    message = client.messages.create(to="(650) 995-2455", from_="(504) 434-7749", body=body)


#first_trimester_todo()
#second_trimester_todo()
#third_trimester_todo()
