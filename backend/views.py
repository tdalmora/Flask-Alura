from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from models import Jogos, Usuarios
from helpers import recupera_imagem, deleta_arquivo
import time


# Define uma nova rota. Essa é a home, mostra os jogos dentro da lista.
@app.route('/')
def index():
  # Vai fazer um query da tabela Jogos, enviando-a em ordem pelo id. lista vai receber isso.
  lista = Jogos.query.order_by(Jogos.id)
  return render_template('lista.html', titulo='Jogos', jogos=lista)


# Para adicionar novo jogo a lista.
@app.route('/novo')
def novo():
  # Mas so pode fazê-lo se estiver logado. Sessions explicado na route /login.
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    flash('Você não está logado!')
    # Se não estiver logado, redirect para login, enviando também em qual página é para voltar.
    return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


# Se o novo receber um post, meio que a ação vai ser recebida nessa rota aqui, intermediária.
@app.route('/criar', methods=['POST'])
def criar():
  # Pegar do request as informações. É pssível pegar sem form.
  nome = request.form['nome']
  categoria = request.form['categoria']
  console = request.form['console']

  jogo = Jogos.query.filter_by(nome=nome).first()

  if jogo:
    flash('Jogo já existente!')
    return redirect(url_for('index'))

  # Manda pro banco de dados.
  novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
  db.session.add(novo_jogo)
  db.session.commit()

  arquivo = request.files('arquivo')
  uploads_path = app.config('UPLOAD_PATH')
  timestamp = time.time()
  arquivo.save(f'{uploads_path}/capa{jogo.id}-{timestamp}.jpg') 
  
  return redirect(url_for('index'))

# Para editar novo jogo a lista.
@app.route('/editar/<int:id>')
def editar(id):
  # Mas so pode fazê-lo se estiver logado. Sessions explicado na route /login.
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    flash('Você não está logado!')
    # Se não estiver logado, redirect para login, enviando também em qual página é para voltar.
    return redirect(url_for('login', proxima=url_for('editar')))
    
  jogo = Jogos.query.filter_by(id=id).first()
  capa_jogo = recupera_imagem(id)
  return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)

# Se o editar receber um post, meio que a ação vai ser recebida nessa rota aqui, intermediária.
@app.route('/atualizar', methods=['POST'])
def atualizar():
  # Pegar do request as informações. Filtrado pelo id que eu recebi do post.
  # jogo vai ser agora esse objeto.
  jogo = Jogos.query.filter_by(id=request.form['id']).first()
  jogo.nome = request.form['nome']
  jogo.categoria = request.form['categoria']
  jogo.console = request.form['console']
  
  db.session.add(jogo)
  db.session.commit()

  arquivo = request.files('arquivo')
  uploads_path = app.config('UPLOAD_PATH')
  timestamp = time.time()
  deleta_arquivo(id)
  arquivo.save(f'{uploads_path}/capa{jogo.id}-{timestamp}.jpg') 
  
  return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
  if 'usuario_logado' not in session or session['usuario_logado'] == None:
    flash('Você não está logado!')
    return redirect(url_for('login'))

    Jogos.quer.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo excluído com sucesso!')

    return redirect(url_for('index'))
    
# Rota para efetuar login.
@app.route('/login')
def login():
  # Vai receber da URL a próxima página a seguir.
  proxima = request.args.get('proxima')
  return render_template('login.html', proxima=proxima)


# Se o login receber um post, meio que a ação vai ser recebida nessa rota aqui, intermediária. Ela vai autenticar o usuário ou ver se a senha  gral está correta.
@app.route('/autenticar', methods=['POST'])
def autenticar():
  # Recebe to primeiro usuário que possui o nickname.
  usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
  # Se quem fez login estiver no dicionário usuários.
  if usuario:
    # Se a senhar dada coincidir com a do usuário.
    if request.form['senha'] == usuario.senha:
      # Session agora possui salvo o nome logado. O seesion salva, nos cookies da página, informações por mais de um ciclo de request / response. Ele é um dicionário.
      session['usuario_logado'] = usuario.nickname
      flash(usuario.nickname + ' logado com sucesso!')
      proxima_pagina = request.form['proxima']
      return redirect(proxima_pagina)
  # Se a senha geral estiver correta.
  if 'alohomora' == request.form['senha']:
    session['usuario_logado'] = request.form['usuario']
    flash(session['usuario_logado'] + ' logado com sucesso!')
    proxima_pagina = request.form['proxima']
    return redirect(proxima_pagina)
  else:
    flash('Usuário não logado.')
    return redirect(url_for('login'))


# Desloga da sessão.
@app.route('/logout')
def logout():
  session['usuario_logado'] = None
  # Mensagem única na tela, precisa fazer a secret key e mudar no html.
  flash('Logout efetuado com sucesso!')
  return redirect(url_for('index'))

# Uma rota só pra retornar o diretório do arquivo para a template em novo.
@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
  return send_from_directory('uploads', nome_arquivo)