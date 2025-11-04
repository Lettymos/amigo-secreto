from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração para PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://username:password@hostname:port/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita o uso de memória desnecessária
db = SQLAlchemy(app)

# Modelo para a resposta do amigo secreto
class Resposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amigo = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Resposta {self.amigo}>'

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('formulario.html')

# Rota para o envio do formulário
@app.route('/submit', methods=['POST'])
def submit():
    amigo = request.form['amigo']
    
    # Adiciona a resposta no banco de dados
    nova_resposta = Resposta(amigo=amigo)
    db.session.add(nova_resposta)
    db.session.commit()  # Salva a resposta no banco

    return redirect('/')

# Criação do banco de dados (se não existir)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

