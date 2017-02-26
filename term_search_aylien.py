from aylienapiclient import textapi
app_id = ""
app_key = ""
with open("aylient_key.txt","r") as f:
    app_id = f.readline().replace("\n","")
    app_key = f.readline().replace("\n","")
f.close()
app_id = "1" + app_id

client = textapi.Client(app_id, app_key)


def search_medical_term(text):
    text = text.replace(" ","%20")
    wiki = "http://en.wikipedia.org/wiki/" + text
    url = wiki
    extract = client.Extract({"url": url})

    text = extract['article']

    summarized_text = ""

    summarized_text += text[0:text.index('.')] + "."

    rest_text = text[text.index('.'):]
    lenght = rest_text.count('.')//5
    summary = client.Summarize({"title":extract["title"],'text': repr(rest_text), 'sentences_number':5})
    for sentence in summary['sentences']:
        sentence = sentence.replace("\\n","")
        summarized_text += " " + sentence

    s = ""
    for i in summarized_text:
        if ord(i) < 128:
            if (ord(i) >= 97 and ord(i) <= 122) or (ord(i) >= 65 and ord(i) <= 90):
                s = s + i
            elif i != "[" and i!="]" and i not in ['0','1','2','3','4','5','6','7','8','9']:
                s = s + i
    s=s.replace("\u","").replace("\\","").replace("\"","")
    return s