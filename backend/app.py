from flask import Flask, render_template, request, redirect
from database import conectar


app = Flask(
    __name__,
    template_folder="../frontend/templates"
)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/livros")
def listar_livros():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM livros ORDER BY titulo ASC"
    )

    livros = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "livros.html",
        livros=livros
    )


@app.route("/livros/<int:id>/editar")
def editar_livro(id):

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM livros WHERE id = %s",
        (id,)
    )

    livro = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "editar_livro.html",
        livro=livro
    )

@app.route("/livros/<int:id>/excluir", methods=["POST"])
def excluir_livro(id):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM livros WHERE id = %s",
        (id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/livros")

@app.route("/livros/<int:id>/editar", methods=["POST"])
def atualizar_livro(id):

    titulo = request.form["titulo"]
    autor = request.form["autor"]
    isbn = request.form["isbn"]
    categoria = request.form["categoria"]
    ano_publicacao = request.form["ano_publicacao"]
    quantidade = request.form["quantidade"]

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE livros
        SET titulo = %s,
            autor = %s,
            isbn = %s,
            categoria = %s,
            ano_publicacao = %s,
            quantidade = %s
        WHERE id = %s
    """

    valores = (
        titulo,
        autor,
        isbn,
        categoria,
        ano_publicacao,
        quantidade,
        id
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/livros")

@app.route("/livros", methods=["POST"])
def cadastrar_livro():

    titulo = request.form["titulo"]
    autor = request.form["autor"]
    isbn = request.form["isbn"]
    categoria = request.form["categoria"]
    ano_publicacao = request.form["ano_publicacao"]
    quantidade = request.form["quantidade"]

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO livros
        (titulo, autor, isbn, categoria, ano_publicacao, quantidade)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    valores = (
        titulo,
        autor,
        isbn,
        categoria,
        ano_publicacao,
        quantidade
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/livros")

@app.route("/usuarios")
def listar_usuarios():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios ORDER BY nome ASC"
    )

    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "usuario.html",
        usuarios=usuarios
    )

@app.route("/usuarios", methods=["POST"])
def cadastrar_usuario():

    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    data_cadastro = request.form["data_cadastro"]

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        INSERT INTO usuarios
        (nome, email, telefone, data_cadastro)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        nome,
        email,
        telefone,
        data_cadastro
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/usuarios")

@app.route("/usuarios/<int:id>/editar")
def editar_usuario(id):

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = %s",
        (id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    return render_template(
        "editar_usuario.html",
        usuario=usuario
    )


@app.route("/usuarios/<int:id>/editar", methods=["POST"])
def atualizar_usuario(id):

    nome = request.form["nome"]
    email = request.form["email"]
    telefone = request.form["telefone"]
    data_cadastro = request.form["data_cadastro"]

    conexao = conectar()

    cursor = conexao.cursor()

    sql = """
        UPDATE usuarios
        SET nome = %s,
            email = %s,
            telefone = %s,
            data_cadastro = %s
        WHERE id = %s
    """

    valores = (
        nome,
        email,
        telefone,
        data_cadastro,
        id
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/usuarios")

@app.route("/usuarios/<int:id>/excluir", methods=["POST"])
def excluir_usuario(id):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM usuarios WHERE id = %s",
        (id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/usuarios")

@app.route("/emprestimos")
def listar_emprestimos():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    # Buscar empréstimos
    cursor.execute("""
        SELECT
            emprestimos.id,
            usuarios.nome AS usuario,
            livros.titulo AS livro,
            emprestimos.data_emprestimo,
            emprestimos.data_devolucao_prevista,
            emprestimos.data_devolucao
        FROM emprestimos
        INNER JOIN usuarios
            ON emprestimos.usuario_id = usuarios.id
        INNER JOIN livros
            ON emprestimos.livro_id = livros.id
        ORDER BY emprestimos.id DESC
    """)

    emprestimos = cursor.fetchall()

    # Buscar usuários
    cursor.execute("""
        SELECT id, nome
        FROM usuarios
        ORDER BY nome ASC
    """)

    usuarios = cursor.fetchall()

    # Buscar livros
    cursor.execute("""
        SELECT id, titulo, quantidade
        FROM livros
        WHERE quantidade > 0
        ORDER BY titulo ASC
    """)

    livros = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "emprestimos.html",
        emprestimos=emprestimos,
        usuarios=usuarios,
        livros=livros
    )

@app.route("/emprestimos", methods=["POST"])
def cadastrar_emprestimo():

    usuario_id = request.form["usuario_id"]
    livro_id = request.form["livro_id"]
    data_emprestimo = request.form["data_emprestimo"]
    data_devolucao_prevista = request.form["data_devolucao_prevista"]

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT quantidade FROM livros WHERE id = %s",
        (livro_id,)
    )

    livro = cursor.fetchone()

    if livro is None:
        cursor.close()
        conexao.close()
        return redirect("/emprestimos")

    if livro["quantidade"] <= 0:
        cursor.close()
        conexao.close()
        return redirect("/emprestimos")

    cursor.execute(
        """
        UPDATE livros
        SET quantidade = quantidade - 1
        WHERE id = %s
        """,
        (livro_id,)
    )

    sql = """
        INSERT INTO emprestimos
        (
            usuario_id,
            livro_id,
            data_emprestimo,
            data_devolucao_prevista
        )
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        usuario_id,
        livro_id,
        data_emprestimo,
        data_devolucao_prevista
    )

    cursor.execute(sql, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/emprestimos")

@app.route("/emprestimos/<int:id>/devolver", methods=["POST"])
def devolver_emprestimo(id):

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT livro_id, data_devolucao
        FROM emprestimos
        WHERE id = %s
        """,
        (id,)
    )

    emprestimo = cursor.fetchone()

    if emprestimo is None:
        cursor.close()
        conexao.close()
        return redirect("/emprestimos")

    if emprestimo["data_devolucao"] is not None:
        cursor.close()
        conexao.close()
        return redirect("/emprestimos")

    livro_id = emprestimo["livro_id"]

    cursor.execute(
        """
        UPDATE emprestimos
        SET data_devolucao = CURDATE()
        WHERE id = %s
        """,
        (id,)
    )

    cursor.execute(
        """
        UPDATE livros
        SET quantidade = quantidade + 1
        WHERE id = %s
        """,
        (livro_id,)
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect("/emprestimos")

if __name__ == "__main__":
    app.run(debug=True)