import sqlite3
import bcrypt

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
        try:
            self.conexao = sqlite3.connect('estoque.db')
            self.cursor = self.conexao.cursor()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS produtos (codigo_produto INTEGER PRIMARY KEY, preco_compra REAL, preco_venda REAL, quantidade INTEGER, categoria TEXT)')
            self.conexao.commit()
            self.cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (username VARCHAR PRIMARY KEY, password VARCHAR)')
            self.conexao.commit()
        except Error as e:
            print(e)


    def adicionar_produto(self, produto, quantidade):
        if quantidade > 0:
            self.cursor.execute('INSERT INTO produtos VALUES (?, ?, ?, ?, ?)', (produto.codigo_produto, produto.preco_compra, produto.preco_venda, produto.quantidade, produto.categoria))
            self.conexao.commit()
        else:
            print("Impossível adicionar {} produtos!".format(quantidade))

    def remover_produto(self, codigo_produto, quantidade):
        self.cursor.execute('SELECT * FROM produtos WHERE codigo_produto = ?', (codigo_produto,))
        produto = self.cursor.fetchone()

        if produto:
            unidades = quantidade
            produto = Produto(*produto)
            quantidade_estoque = produto.quantidade

            if (quantidade > 0 and quantidade <= quantidade_estoque):

                while (quantidade > 0 and quantidade <= quantidade_estoque):
                    self.cursor.execute('UPDATE produtos SET quantidade = quantidade - ? WHERE codigo_produto = ?', (1, produto.codigo_produto))
                    self.conexao.commit()
                    quantidade = quantidade - 1

                print("{} unidade(s) do produto de código {} da categoria {} foram removidas do estoque\n".format(unidades, produto.codigo_produto, produto.categoria))
                
                self.cursor.execute('SELECT * FROM produtos WHERE codigo_produto = ?', (codigo_produto,))
                produto = self.cursor.fetchone()

                if produto:
                    produto = Produto(*produto)

                    if (produto.quantidade == 0):
                        self.cursor.execute('DELETE FROM produtos WHERE codigo_produto = ?', (produto.codigo_produto,))
                        self.conexao.commit()

            elif quantidade > quantidade_estoque:
                print("Existem apenas {} produtos em estoque!".format(quantidade_estoque))

            elif quantidade < 0:
                print("Não é possível remover {} produtos do estoque!".format(quantidade))

        else:
            print("Produto não encontrado no estoque!\n")

    def consultar_produto(self, codigo_produto):
        self.cursor.execute('SELECT * FROM produtos WHERE codigo_produto = ?', (codigo_produto,))
        produto = self.cursor.fetchone()

        if produto:
            produto = Produto(*produto)
            
            print("codigo: {}\n preço de compra: {}\n preco de venda: {}\n quantidade: {}\n categoria: {}\n".format(produto.codigo_produto, produto.preco_compra, produto.preco_venda, produto.quantidade, produto.categoria))
        else:
            print("Produto indisponível!\n")

    def listar_produtos(self):
        self.cursor.execute('SELECT * FROM produtos')
        produtos = []
        for produto in self.cursor.fetchall():
            produtos.append(Produto(*produto))
        for produto in produtos:
            print(produto.codigo_produto, produto.preco_compra, produto.preco_venda, produto.quantidade, produto.categoria)
        if len(produtos) < 1:
            print("Não há produtos cadastrados\n")

    def sair(self):
        self.conexao.close()
        exit()

def login(estoque):
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    estoque.cursor.execute('SELECT password FROM usuarios WHERE username = ?', (username,))
    hash_password = estoque.cursor.fetchone()[0]

    if bcrypt.checkpw(password.encode('utf-8'), hash_password):
        menu(estoque)
    else:
        print("Credenciais incorretas!\n")
        estoque.sair()

def cadastrar(estoque):
    username = input("Digite seu novo nome de usuario: ")
    password = input("Digite sua nova senha: ")
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    estoque.cursor.execute('INSERT INTO usuarios VALUES (?, ?)', (username, hashed))
    estoque.conexao.commit()
    login(estoque)

def menu(estoque):
    while True:
        while True:
            try:
                resposta = int(input("""O que você gostaria de fazer?\n
                1 - Adicionar produto\n
                2 - Remover produto\n
                3 - Consultar produto\n
                4 - Listar produtos\n
                5 - sair\n"""))

                if resposta not in [1, 2, 3, 4, 5]:
                    raise ValueError("Resposta inválida! Por favor, informe uma das opções!\n")
                break

            except ValueError:
                print("Entrada inválida, selecione uma das opções!\n")
                
        if resposta == 1:
            codigo_produto = int(input("Digite o código do produto: "))
            preco_compra = float(input("Digite o preço de compra: ")) 
            preco_venda = float(input("Digite o preço de venda: ")) 
            quantidade = int(input("Digite a quantidade: ")) 
            categoria = input("Digite a categoria: ")

            produto = Produto(codigo_produto, preco_compra, preco_venda, quantidade, categoria)
            estoque.adicionar_produto(produto, quantidade)


        elif resposta == 2:
            codigo_produto = input("Digite o código do produto: ")
            quantidade = int(input("Digite a quantidade a ser removida: "))
            estoque.remover_produto(codigo_produto, quantidade)

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
            print("Resposta inválida!\n")

estoque = Estoque()

while True:
    try:
        cadastro = int(input("Possui cadastro no sistema?\n1 - SIM\n2 - NÃO\n"))
        if cadastro not in [1,2]:
            raise ValueError("Resposta inválida! Por favor, informe uma das opções!\n")
        break
    except ValueError:
        print("Entrada inválida, selecione uma das opções!\n")

if cadastro == 1:
    login(estoque)
elif cadastro == 2:
    cadastrar(estoque)
else:
    print("Resposta invàlida!\n")
