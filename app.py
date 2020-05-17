from flask import Flask, render_template, request
from chatbot.chatbot import get_response

app = Flask(__name__)
conversation = []
user = {'localisation':'',
        'contexte':''
}
@app.route('/')
def home():
    if(conversation):
        for i in range(len(conversation)):
            conversation.pop()
        user.clear()
        user = {'localisation':'',
        'contexte':''}
    return render_template("home.html")

@app.route('/', methods=['POST'])
def text_box():
    text = request.form['question']
    quest_rep = get_response(text,user)
    for elt in quest_rep:
        conversation.append(elt)
    return render_template("home.html", conversation=conversation)

if __name__ == "__main__":
    app.run(debug=True)