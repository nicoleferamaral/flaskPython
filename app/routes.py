from app import app
from flask import render_template
from flask import request
import requests   #para instalar pode clicar em cima e colocar para instalar, ou ir em python packages embaico e instalar
import json
link = "https://flasktintnicole-default-rtdb.firebaseio.com/"

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html',titulo="Página Inicial")

@app.route('/contato')
def contato():
    return render_template('contato.html', titulo="Contatos")


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', titulo="Cadastrar")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    #cada form precisa de um requests.
    try: #Vai tentar executar
        cpf = request.form.get("cpf")  #coletar dados
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        email = request.form.get("email")
        senha = request.form.get("senha")


        dados = {"cpf": cpf, "nome":nome, "telefone":telefone, "endereco": endereco, "email":email, "senha":senha} #formato de requisição, coleção de dados, qual é o dado e quem é o dado
        requisicao = requests.post(f'{link}/cadastro/.json', data = json.dumps(dados)) #resposta true or false, vai tentar inserir no banco de dados os dados informados
        return 'Cadastrado com sucesso!'
    except Exception as e: #caso tenha uma excessão roda o exception
        return f'Ocorreu um erro\n +{e}'


@app.route('/listar')
def listarTudo():
    try:
        requisicao = requests.get(f'{link}/cadastro/.json') #solicita os dados
        dicionario = requisicao.json()
        return dicionario

    except Exception as e:
        return f'Algo deu errado \n {e}'


@app.route('/listarIndividual', methods=['POST'])
def listarIndividual():
    try:
        requesicao = requests.get(f'{link}/cadastro/.json')
        dicionario = requesicao.json()
        procurar = request.form.get("procurar")

        for codigo in dicionario:
            chave = dicionario[codigo]['nome']
            if chave == procurar:

                return f'Nome: {dicionario[codigo]["nome"]}\n<br> CPF: {dicionario[codigo]["cpf"]}\n<br> Telefone: {dicionario[codigo]["telefone"]}\n<br> Endereco: {dicionario[codigo]["endereco"]}\n<br>'

    except Exception as e:
        return f'Algo deu errado\n {e}'

@app.route('/atualizacao')
def atualizacao():
    return render_template('atualizacao.html',titulo="Atualização")

@app.route('/atualizar', methods=['POST'])
def atualizar():
    try:
        requesicao = requests.get(f'{link}/consultar/.json')
        dicionario = requesicao.json()

        cpf      = request.form.get("cpf")
        nome     = request.form.get("nome")
        telefone = request.form.get("telefone")
        endereco = request.form.get("endereco")
        dados    = {"cpf": cpf, "nome": nome, "telefone": telefone, "endereco": endereco}

        for codigo in dicionario:
            chave = dicionario[codigo][cpf]
            if chave == cpf:
                requisicao = requests.patch(f'{link}/consultar/{codigo}/.json', data=json.dumps(dados))
                return "Atualizado com sucesso!"

    except Exception as e:
        return f'Algo deu errado\n {e}'


@app.route('/excluir')
def excluir():
    try:
        requisicao = requests.delete(f'{link}/cadastro/-O8mkk11M1SdppmuhJcc/.json')
        return f'Excluido com sucesso'

    except Exception as e:
        return f'Algo deu errado\n {e}'

@app.route('/consultar')
def consultar():
    return render_template('consultar.html', titulo="Consultar")


