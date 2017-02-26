import logging

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

import term_search_aylien as sz

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def begin_session():
	start_msg = "Hi! Do you want to search for Medical Terminology?"
	session.attributes['answers']=""
	return question(start_msg)

@ask.intent("Pregnant")
def pregnant_case():
	return statement("Listen, and listen closely. Step 1: Get off Google.")
@ask.intent("MedicalQueryIntent",convert={'answer':str})
def start_query(answer):
	session.attributes['answers'] = answer
	print answer
	if session.attributes['answers'] == "Can You Please Repeat That":
		return question("I didn't quite get that, can you please repeat?")
	else:
		eliza_response = sz.search_medical_term(session.attributes['answers'])
		curr_response_msg = str(eliza_response)
		return statement(curr_response_msg)


if __name__=='__main__':
	app.run(debug=True)

