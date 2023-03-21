import sqlite3

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
		self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS produtos (codigo_produto INTEGER, preco_compra REAL, preco_venda REAL, quantidade INTEGER, categoria TEXT)')
        self.connection.commit()

	def adicionar_produto(self, produto):
		self.cursor.execute('INSERT INTO produtos VALUES (?, ?, ?, ?, ?)', (produto.codigo_produto, produto.preco_compra, produto.preco_venda, produto.quantidade, produto.categoria))
		self.connection.commit()

	def remover_produto(self, codigo_produto):
		self.cursor.execute('DELETE FROM produtos WHERE codigo_produto = ?', (codigo_produto,))
		self.connection.commit()

	def consultar_produto(self, codigo_produto):
		self.cursor.execute('SELECT * FROM produtos WHERE codigo_produto = ?', (codigo_produto))
		produto = self.cursor.fetchnone()
		if produto:
			return Produto(*produto)
		else:
			return none

	def listar_produtos(self):
		self.cursor.execute('SELECT * FROM  produtos')
		produtos = []
		for produto in self.cursor.fetchall():
			produtos.append(Produto(*produto))
		return produtos

	def sair(self):
		self.connection.close