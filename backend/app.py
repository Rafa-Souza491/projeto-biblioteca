from flask import Flask, render_template, request, redirect
from database import conectar


app = Flask(
    __name__,
    template_folder="../frontend/templates"
)


@app.route("/")
def inicio():

    conexao = conectar()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM livros")

    livros = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template(
        "index.html",
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

    return redirect("/")

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

    return "Livro atualizado com sucesso!"

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

    return "Livro cadastrado com sucesso!"


if __name__ == "__main__":
    app.run(debug=True)