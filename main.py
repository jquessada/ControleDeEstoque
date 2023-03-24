import sqlite3

class Usuario:
    def __init__(self, username, senha):
        self.username = username
        self.senha = senha

class Produto:
    def __init__(self, codigo_produto, preco_compra, preco_venda, quantidade, categoria):
        self.codigo_produto = codigo_produto
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.quantidade = quantidade
        self.categoria = categoria

class Estoque:
    def __init__(self):
        self.conexao = sqlite3.connect('estoque.db')
        self.cursor = self.conexao.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS produtos (codigo_produto INTEGER PRIMARY KEY, preco_compra REAL, preco_venda REAL, quantidade INTEGER, categoria TEXT)')
        self.conexao.commit()

    def verifica_login(self, username, senha):
        self.cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, senha,))
        usuario = self.cursor.fetchone()
        usuario = Usuario(*usuario)
        if usuario:
            menu()
        else:
            print("Credenciais incorretas!")
            self.conexao.close()
            login()


    def adicionar_produto(self, produto):
        self.cursor.execute('INSERT INTO produtos VALUES (?, ?, ?, ?, ?)', (produto.codigo_produto, produto.preco_compra, produto.preco_venda, produto.quantidade, produto.categoria))
        self.conexao.commit()

    def remover_produto(self, codigo_produto):
        self.cursor.execute('DELETE FROM produtos WHERE codigo_produto = ?', (codigo_produto,))
        self.conexao.commit()

    def consultar_produto(self, codigo_produto):
        self.cursor.execute('SELECT * FROM produtos WHERE codigo_produto = ?', (codigo_produto,))
        produto = self.cursor.fetchone()
        produto = Produto(*produto)
        if produto:
            print(produto.codigo_produto, produto.preco_compra, produto.preco_venda, produto.quantidade, produto.categoria)
        else:
            print("Produto indisponível!")

    def listar_produtos(self):
        self.cursor.execute('SELECT * FROM produtos')
        produtos = []
        for produto in self.cursor.fetchall():
            produtos.append(Produto(*produto))
        for produto in produtos:
            print(produto.codigo_produto, produto.preco_compra, produto.preco_venda, produto.quantidade, produto.categoria)

    def sair(self):
        self.conexao.close()
        exit()

def login():
    estoque = Estoque()
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")
    credenciais = [username, password]
    estoque.verifica_login(credenciais[0], credenciais[1])

def menu():
    while True:
        resposta = int(input("""Bem vindo! O que você gostaria de fazer?\n
                1 - Adicionar produto\n
                2 - Remover produto\n
                3 - Consultar produto\n
                4 - Listar produtos\n
                5 - sair\n"""))

        if resposta == 1:
            codigo_produto = input("Digite o código do produto: ")
            preco_compra = input("Digite o preço de compra: ") 
            preco_venda = input("Digite o preço de venda: ") 
            quantidade = input("Digite a quantidade: ") 
            categoria = input("Digite a categoria: ")

            produto = Produto(codigo_produto, preco_compra, preco_venda, quantidade, categoria)
            estoque.adicionar_produto(produto)


        elif resposta == 2:
            codigo_produto = input("Digite o código do produto: ")
            estoque.remover_produto(codigo_produto)

        elif resposta == 3:
            codigo_produto = input("Digite o código do produto: ")
            estoque.consultar_produto(codigo_produto)

        elif resposta == 4:
            estoque.listar_produtos()

        elif resposta == 5:
            print("Até mais!")
            estoque.sair()
            exit()

        else:
            print("Resposta inválida!")

login()