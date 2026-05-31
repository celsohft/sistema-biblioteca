import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()

# Criar tabela de livros
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL
    )
''')
conn.commit()

# ========== FUNÇÕES DO SISTEMA ==========

def adicionar_livro():
    """Adicionar um novo livro"""
    print("\n--- ADICIONAR LIVRO ---")
    titulo = input("Título do livro: ")
    autor = input("Autor: ")
    
    cursor.execute("INSERT INTO livros (titulo, autor) VALUES (?, ?)", (titulo, autor))
    conn.commit()
    print(f"\n✅ Livro '{titulo}' adicionado com sucesso!")

def listar_livros():
    """Listar todos os livros"""
    print("\n--- LISTA DE LIVROS ---")
    cursor.execute("SELECT id, titulo, autor FROM livros ORDER BY titulo")
    livros = cursor.fetchall()
    
    if not livros:
        print("📭 Nenhum livro cadastrado na biblioteca.")
    else:
        print(f"\n📚 Total de livros: {len(livros)}\n")
        for id_, titulo, autor in livros:
            print(f"ID: {id_} | 📖 {titulo} | ✍️ Autor: {autor}")

def buscar_livro():
    """Buscar livro por título ou autor"""
    print("\n--- BUSCAR LIVRO ---")
    termo = input("Digite o título ou autor para buscar: ")
    
    cursor.execute("""
        SELECT id, titulo, autor FROM livros 
        WHERE titulo LIKE ? OR autor LIKE ?
        ORDER BY titulo
    """, (f'%{termo}%', f'%{termo}%'))
    
    resultados = cursor.fetchall()
    
    if resultados:
        print(f"\n🔍 Encontrados {len(resultados)} livro(s):\n")
        for id_, titulo, autor in resultados:
            print(f"ID: {id_} | 📖 {titulo} | ✍️ {autor}")
    else:
        print("❌ Nenhum livro encontrado.")

def excluir_livro():
    """Excluir um livro pelo ID"""
    print("\n--- EXCLUIR LIVRO ---")
    listar_livros()
    
    try:
        id_livro = int(input("\nDigite o ID do livro que deseja excluir: "))
        
        # Verificar se o livro existe
        cursor.execute("SELECT titulo FROM livros WHERE id = ?", (id_livro,))
        livro = cursor.fetchone()
        
        if livro:
            confirmar = input(f"Tem certeza que quer excluir '{livro[0]}'? (s/n): ")
            if confirmar.lower() == 's':
                cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
                conn.commit()
                print(f"✅ Livro excluído com sucesso!")
            else:
                print("❌ Exclusão cancelada.")
        else:
            print("❌ ID inválido! Livro não encontrado.")
    except ValueError:
        print("❌ Por favor, digite um número válido!")

def estatisticas():
    """Mostrar estatísticas da biblioteca"""
    cursor.execute("SELECT COUNT(*) FROM livros")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT autor) FROM livros")
    total_autores = cursor.fetchone()[0]
    
    print("\n--- ESTATÍSTICAS DA BIBLIOTECA ---")
    print(f"📚 Total de livros: {total}")
    print(f"✍️ Total de autores: {total_autores}")
    
    if total > 0:
        cursor.execute("SELECT autor, COUNT(*) FROM livros GROUP BY autor ORDER BY COUNT(*) DESC LIMIT 3")
        top_autores = cursor.fetchall()
        
        print("\n🏆 Top autores (mais livros):")
        for autor, quantidade in top_autores:
            print(f"   • {autor}: {quantidade} livro(s)")

# ========== MENU PRINCIPAL ==========

def menu():
    print("\n" + "="*50)
    print("          📚 SISTEMA DE BIBLIOTECA")
    print("="*50)
    print("1️⃣  - Adicionar livro")
    print("2️⃣  - Listar todos os livros")
    print("3️⃣  - Buscar livro")
    print("4️⃣  - Excluir livro")
    print("5️⃣  - Estatísticas")
    print("6️⃣  - Sair")
    print("="*50)

# ========== PROGRAMA PRINCIPAL ==========

print("\n🎉 Bem-vindo ao Sistema de Biblioteca!")

while True:
    menu()
    opcao = input("\n👉 Escolha uma opção (1-6): ")
    
    if opcao == "1":
        adicionar_livro()
    elif opcao == "2":
        listar_livros()
    elif opcao == "3":
        buscar_livro()
    elif opcao == "4":
        excluir_livro()
    elif opcao == "5":
        estatisticas()
    elif opcao == "6":
        print("\n👋 Obrigado por usar o Sistema de Biblioteca!")
        break
    else:
        print("❌ Opção inválida! Tente novamente.")
    
    input("\n⏎ Pressione Enter para continuar...")

# Fechar conexão
conn.close()
