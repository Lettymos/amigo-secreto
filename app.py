from flask import Flask, render_template, request, jsonify
import os, datetime

app = Flask(__name__)
ARQ = os.path.join(os.path.dirname(__file__), 'respostas_amigo_secreto.txt')

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/submit', methods=['POST'])
def submit():
    amigo = (request.form.get('amigo') or '').strip()
    if not amigo:
        return jsonify(success=False, message='Campo vazio'), 400
    with open(ARQ, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - Pegou: {amigo}\n")
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
