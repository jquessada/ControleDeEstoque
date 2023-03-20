import sqlite3

Class Produto:
	def __init__(self, codigo_produto, preco_compra, preco_venda, quantidade, categoria):
		self.codigo_produto = codigo_produto
		self.preco_compra = preco_compra
		self.preco_venda = preco_venda
		self.quantidade = quantidade
		self.categoria = categoria

Class Estoque:
	sef __init__(self):
	self.conexao = sqlite3.connect('estoque.db')