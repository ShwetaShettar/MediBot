import logging

from flask import Flask, render_template
from flask_ask import Ask, question, session, statement

import responses
import term_search_aylien as sz
import pregnancy_scrape as ps

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def begin_session():
    start_msg = "Hi! Do you want to search for Medical Terminology?"
    session.attributes['answers'] = ""
    return question(start_msg)



def pregnant_case():
    return question("What Trimester?")


@ask.intent("Trimester", convert={'answer': str})
def trimester(answer):
    session.attributes['answers'] = answer.lower()
    output = "hey! YOU ARE NOT EVEN PREGNANT THOUGH"
    if session.attributes['answers'] == "first":
    	output = responses.first.encode("utf-8")
    	ps.first_trimester_todo()
    elif session.attributes['answers'] == "second":
    	output = responses.second.encode("utf-8")
    	ps.second_trimester_todo()
    elif session.attributes['answers'] == "third":
        output = responses.third.encode("utf-8")
        ps.third_trimester_todo()
    else:
    	output = output
    return statement(output)


@ask.intent("MedicalQueryIntent", convert={'answer': str})
def start_query(answer):
    session.attributes['answers'] = answer
    if answer.lower() == "pregnant":
    	return pregnant_case()
    print answer
    if session.attributes['answers'] == "Can You Please Repeat That":
        return question("I didn't quite get that, can you please repeat?")
    else:
        eliza_response = sz.search_medical_term(session.attributes['answers'])
        curr_response_msg = str(eliza_response)
        return statement(curr_response_msg)


if __name__ == '__main__':
    app.run(debug=True)
