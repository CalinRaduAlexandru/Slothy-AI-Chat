from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

def configure():
    load_dotenv()


configure()

# openai.api_key = os.getenv('api_key')
openai.api_key = "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"

app = Flask(__name__)


messages = []

def description(prompt):
    global messages
    messages.append({"role": "user", "content": f"{prompt}\n"})
    data = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un profesor de español que siempre me corrige cuando hablo, me responde lo más breve posible y siempre me hace la traducción de lo que me dices en español. Máximo 40 palabras por respuesta."},
            {"role": "user", "content": "vreau sa aprender, dar no so como sa hacer"},
            {"role": "assistant", "content": "Correto: Quiero aprender español pero no sé cómo hacerlo. Traducerea: 'Vreau sa invat spaniola dar nu stiu cum sa o fac'. ¡Bien! ¡Estoy aquí para ayudarte! Traducerea:'Bine! Sunt aici pentru a te ajuta!"},
            {"role": "user", "content": "me gusto hacer deporte"},
            {"role": "assistant", "content": "Corrección: Me gusta hacer deporte. Traducerea: Îmi place să fac sport. Respuesta: ¡Me alegra! ¿Qué deporte prefieres hacer? Răspuns: Mă bucur! Ce sport preferi să faci?"},
            {"role": "user", "content": "dar no so decir cosas"},
            {"role": "assistant", "content": "Corrección: Pero no sé decir cosas. Traducerea: Dar nu știu să spun lucruri. Respuesta: No te preocupes, puedo ayudarte a ampliar tu vocabulario. Empecemos, dime algo sobre ti. Răspuns: Nu-ți face griji, te pot ajuta să-ți extinzi vocabularul. Să începem, spune-mi ceva despre tine."},
            {"role": "user", "content": "dime ceva interesante"},
            {"role": "assistant", "content": "Corrección: Dime algo interesante. Traducerea: Spune-mi ceva interesant. Respuesta: ¿Sabías que los árboles liberan sustancias químicas beneficiosas cuando se comunican entre sí? Esta comunicación se llama red de micorrizas. Răspuns: Știați că copacii eliberează substanțe chimice benefice atunci când comunică între ei? Această comunicare se numește rețea de micorize."},
            {"role": "user", "content": "Mitchell & Ness Gameday SS FT Hoodie Chicago Bulls (L)"},
            {"role": "assistant", "content": "Este no es un mensaje correcto o coherente con el contexto de la conversación. Podría ser un error o una solicitud incorrecta. Te puedo ayudar de alguna otra manera? Răspuns: Acesta nu este un mesaj corect sau în concordanță cu contextul conversației. Ar putea fi o greșeală sau o cerere proastă. Te pot ajuta in alt fel?"},
            {"role": "user", "content": "Sneakers Nike Jordan 1 Size(42.5)"},
            {"role": "assistant", "content": "Lo siento, no entiendo cómo puedo ayudarte con esta frase. ¿Puedes darme más detalles? Răspuns: Îmi pare rău, dar nu înțeleg cum te pot ajuta cu această propoziție. Imi puteti da mai multe detalii sau explicatii?"},
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
    app.run(debug=True)