from database import conectar


try:
    conexao = conectar()

    if conexao.is_connected():
        print("Conexão com MySQL realizada com sucesso!")

        cursor = conexao.cursor()
        cursor.execute("SELECT DATABASE();")

        banco = cursor.fetchone()

        print(f"Banco conectado: {banco[0]}")

        cursor.close()
        conexao.close()

except Exception as erro:
    print("Erro ao conectar ao MySQL:")
    print(erro)