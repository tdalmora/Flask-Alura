from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inicialização do servidor e banco.
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Instanciando o objeto que vai se comunicar com o banco. Conecta ele com a aplicação.
db = SQLAlchemy(app)

from views import *

# Dá run no app e db. O __name__ é pra só iniciar se o run for feito neste arquivo aqui.
if __name__ == "__main__":
  app.run(debug=True)
