from flask import Flask, render_template, request, jsonify, url_for
import os
from datetime import datetime

app = Flask(__name__)

# salva em uma pasta segura do Flask (não dá conflito com caminhos relativos)
os.makedirs(app.instance_path, exist_ok=True)
ARQUIVO_RESPOSTAS = os.path.join(app.instance_path, 'respostas_amigo_secreto.txt')

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/submit', methods=['POST'])
def submit():
    amigo = (request.form.get('amigo') or '').strip()
    if not amigo:
        return jsonify(success=False, message="Campo vazio"), 400

    linha = f"{datetime.now().isoformat(timespec='seconds')} - Pegou: {amigo}\n"
    with open(ARQUIVO_RESPOSTAS, 'a', encoding='utf-8') as f:
        f.write(linha)

    return jsonify(success=True)
    
if __name__ == '__main__':
    app.run(debug=True)

from flask import send_from_directory

@app.route('/download')
def download_file():
    try:
        return send_from_directory(app.instance_path, 'respostas_amigo_secreto.txt', as_attachment=True)
    except FileNotFoundError:
        return "Arquivo não encontrado", 404

