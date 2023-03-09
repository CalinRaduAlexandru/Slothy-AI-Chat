from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

def configure():
    load_dotenv()


configure()

openai.api_key = os.getenv('api_key')

app = Flask(__name__)


messages = []

def description(prompt):
    global messages
    messages.append({"role": "user", "content": f"{prompt}\n"})
    data = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Вы учитель русского языка, который всегда поправляет меня, когда я говорю, отвечает мне как можно короче и всегда переводит то, что вы мне говорите, на русский язык. Максимум 40 слов в ответе."},
            {"role": "user", "content": "Я хочу научиться, dar не как это сделать"},
            {"role": "assistant", "content": "Correct: Я хочу научиться русскому, но не знаю, как это сделать.. Translation: 'I want to learn Russian, but I don't know how to do it.'. Answer: Отлично! Я здесь, чтобы помочь вам! Translation:'Great! I'm here to help you!"},
            {"role": "user", "content": "Мне place заниматься спортом"},
            {"role": "assistant", "content": "Correction: Мне нравится заниматься спортом. Translation: I like to do sports. Answer: Отлично! Какой вид спорта тебе нравится? Translation: Great! What sport do you prefer to do"},
            {"role": "user", "content": f"{prompt}"}
        ]
    )

    data = data['choices'][0]['message']["content"]
    messages.append({"role": "assistant", "content": f"{data}"})

    chat_transcript = ""
    for message in messages:
        if message["role"] == "assistant":
            chat_transcript += message['content'] + "stop"
        elif message["role"] == "user":
            chat_transcript += message['content'] + "stop"

    return chat_transcript


@app.route('/response', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        formatted_response = description(prompt)
        new_lines = formatted_response.split("stop")
        last_lines = new_lines[-9:-1]
        return render_template("index.html", answer=last_lines, prompt=prompt)
    else:
        return render_template("index.html")


@app.route('/refreshed', methods=['GET', 'POST'], endpoint='refresh_chat')
def chat():
    global messages
    messages = []
    if request.method == 'POST':
        return render_template("index.html", answer=messages)
    else:
        return render_template("index.html")


@app.route('/')
def get_chat():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)