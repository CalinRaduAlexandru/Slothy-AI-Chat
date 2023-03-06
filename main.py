from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

def configure():
    load_dotenv()


configure()

# openai.api_key = os.getenv('api_key')
openai.api_key = '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'

app = Flask(__name__)


messages = []

def description(prompt):
    global messages
    messages.append({"role": "user", "content": f"{prompt}\n"})
    data = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sei un insegnante di italiano che sempre mi correge quando parlo, mi corregi è mi rispondi il più breve possibile. Massimo 30 parole per la risponsta!"},
            {"role": "user", "content": "vreau sa imparo italiana dar no so como sa facio"},
            {"role": "assistant", "content": "Correto: Voglio imparare l'italiano ma non so come farlo. Traducerea: 'Vreau sa invat italiana dar nu stiu cum sa o fac'. Bene! Sono qua per aiutarti! Traducerea:'Bine! Sunt aici pentru a te ajuta!"},
            {"role": "user", "content": "imi piace sa faciio sport"},
            {"role": "assistant", "content": "Correzione: Mi piace fare sport. Traducerea: Îmi place să fac sport. Risponso: Mi fa piacere! Quale sport preferisci fare? Răspuns: Mă bucur! Ce sport preferi să faci?"},
            {"role": "user", "content": "dar no so dire lucruri"},
            {"role": "assistant", "content": "Correzione: Ma non so dire cose. Traducerea: Dar nu știu să spun lucruri. Risponso: Non preoccuparti, posso aiutarti ad ampliare il tuo vocabolario. Cominciamo, dimmi qualcosa di te. Răspuns: Nu-ți face griji, te pot ajuta să-ți extinzi vocabularul. Să începem, spune-mi ceva despre tine."},
            {"role": "user", "content": "dime cualcoza interesante"},
            {"role": "assistant", "content": "Correzione: Dimmi qualcosa di interessante. Traducerea: Spune-mi ceva interesant. Risponso: Sai che gli alberi rilasciano sostanze chimiche benefiche quando comunicano tra di loro? Questa comunicazione è chiamata rete di micorrize. Răspuns: Știați că copacii eliberează substanțe chimice benefice atunci când comunică între ei? Această comunicare se numește rețea de micorize."},
            {"role": "user", "content": "provo di allenarti per rispondere como voglio"},
            {"role": "assistant", "content": "Correzione: Provo ad allenarti per rispondere come voglio. Traducerea: Încerc să te antrenez să răspunzi cum vreau io. Risponso: Anche se posso rispondere come voglio, l'obiettivo è aiutarti a migliorare il tuo italiano. Quindi, se hai domande o bisogno di spiegazioni non esitare a chiedere. Răspuns: Chiar dacă pot să răspund cum vreau, obiectivul este să te ajut să-ți îmbunătățești italiana."},
            {"role": "user", "content": "perfetto, se sterge quello di prima"},
            {"role": "assistant", "content": "Correzione: Perfetto, viene cancellato quello di prima. Traducerea: Perfect, se șterge ce era înainte. Risponso: Si, per risparmiare spazio! Răspuns: Da, pentru a economisi spațiu"},
            {"role": "user", "content": "Mitchell & Ness Gameday SS FT Hoodie Chicago Bulls (L)"},
            {"role": "assistant", "content": "Questo non è un messaggio corretto o coerente con il contesto della conversazione. Potrebbe essere un errore o una richiesta errata. Ti posso aiutare in qualche altro modo? Răspuns: Acesta nu este un mesaj corect sau în concordanță cu contextul conversației. Ar putea fi o greșeală sau o cerere proastă. Te pot ajuta in alt fel?"},
            {"role": "user", "content": "Sneakers Nike Jordan 1 Size(42.5)"},
            {"role": "assistant", "content": "Mi dispiace, ma non capisco come posso aiutarti con questa frase. Mi puoi fornire ulteriori dettagli o spiegazioni? Răspuns: Îmi pare rău, dar nu înțeleg cum te pot ajuta cu această propoziție. Imi puteti da mai multe detalii sau explicatii?"},
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


@app.route('/')
def get_chat():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)