#Usando como base o último código de CRUD desenvolvido em aula
import sqlite3

# =========================
# Função de Conexão com DB
# =========================
def conectar():
    conexao = sqlite3.connect("Inventario.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    """)
    conexao.commit()
    return conexao, cursor

# =========================
# Funções CRUD
# =========================
def criar_produto(cursor, conexao):
    nome = input("Nome do produto: ").strip()
    quantidade = input("Quantidade: ").strip()
    preco = input("Preço: ").strip()
    
    if not quantidade.isdigit() or not preco.replace('.','',1).isdigit():
        print("Quantidade ou preço inválidos!")
        return

    try:
        cursor.execute(
            "INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
            (nome, int(quantidade), float(preco))
        )
        conexao.commit()
        print(f"Produto '{nome}' criado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Produto com esse nome já existe.")

def listar_produtos(cursor):
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
    print("\n=== Produtos no Estoque ===")
    for prod in produtos:
        print(f"ID: {prod[0]} | Nome: {prod[1]} | Quantidade: {prod[2]} | Preço: R${prod[3]:.2f}")
    print("===========================\n")

def atualizar_produto(cursor, conexao):
    id_prod = input("ID do produto a atualizar: ").strip()
    if not id_prod.isdigit():
        print("ID inválido!")
        return
    cursor.execute("SELECT * FROM produtos WHERE id=?", (int(id_prod),))
    produto = cursor.fetchone()
    if not produto:
        print("Produto não encontrado.")
        return
    quantidade = input(f"Nova quantidade (atual: {produto[2]}): ").strip()
    preco = input(f"Novo preço (atual: R${produto[3]:.2f}): ").strip()
    if not quantidade.isdigit() or not preco.replace('.','',1).isdigit():
        print("Quantidade ou preço inválidos!")
        return
    cursor.execute(
        "UPDATE produtos SET quantidade=?, preco=? WHERE id=?",
        (int(quantidade), float(preco), int(id_prod))
    )
    conexao.commit()
    print("Produto atualizado com sucesso!")

def deletar_produto(cursor, conexao):
    id_prod = input("ID do produto a deletar: ").strip()
    if not id_prod.isdigit():
        print("ID inválido!")
        return
    cursor.execute("SELECT * FROM produtos WHERE id=?", (int(id_prod),))
    produto = cursor.fetchone()
    if not produto:
        print("Produto não encontrado.")
        return
    cursor.execute("DELETE FROM produtos WHERE id=?", (int(id_prod),))
    conexao.commit()
    print("Produto deletado com sucesso!")

# =========================
# Menu Interativo
# =========================
def menu():
    conexao, cursor = conectar()
    while True:
        print("\n=== Sistema de Estoque ===")
        print("1. Criar produto")
        print("2. Listar produtos")
        print("3. Atualizar produto")
        print("4. Deletar produto")
        print("5. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            criar_produto(cursor, conexao)
        elif escolha == "2":
            listar_produtos(cursor)
        elif escolha == "3":
            atualizar_produto(cursor, conexao)
        elif escolha == "4":
            deletar_produto(cursor, conexao)
        elif escolha == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

    conexao.close()

# =========================
# Execução do Programa
# =========================
if __name__ == "__main__":
    menu()
