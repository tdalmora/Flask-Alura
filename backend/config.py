import os

# Conectando sql com o banco. Configurao SGBD (Gerenciamento do DB) e senha secreta.

SECRECT_KEY = 'supersenhasecreta'
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = '127.0.0.1',
        database = 'jogoteca'
    )

# Caminho absoluto do arquivo (abspath). O dirname retorna em qual diretorio este arquivo está. Concatenando com o arquivo que queremos, é o caminho do arquivo.
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'