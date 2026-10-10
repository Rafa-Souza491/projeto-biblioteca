from flask import Flask, render_template, request, redirect, url_for, flash
from database import conectar
import os

app = Flask(__name__, template_folder="../frontend/templates")

# Chave usada pelo Flask para exibir mensagens temporárias.
# Para desenvolvimento local, configure FLASK_SECRET_KEY no .env.
app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "chave-temporaria-biblioteca"
)


# =========================================
# PÁGINA INICIAL
# =========================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================
# LIVROS
# =========================================

@app.route("/livros", methods=["GET", "POST"])
def livros():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        if request.method == "POST":
            titulo = request.form["titulo"].strip()
            autor = request.form["autor"].strip()
            isbn = request.form.get("isbn", "").strip() or None
            categoria = request.form.get("categoria", "").strip() or None
            ano_publicacao = request.form.get("ano_publicacao") or None
            quantidade = request.form.get("quantidade", type=int)

            if not titulo or not autor or quantidade is None or quantidade < 0:
                flash("Preencha os campos corretamente.", "erro")
                return redirect(url_for("livros"))

            cursor.execute(
                """
                INSERT INTO livros
                    (titulo, autor, isbn, categoria,
                     ano_publicacao, quantidade, ativo)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
                """,
                (
                    titulo,
                    autor,
                    isbn,
                    categoria,
                    ano_publicacao,
                    quantidade
                )
            )

            conexao.commit()
            flash("Livro cadastrado com sucesso!", "sucesso")
            return redirect(url_for("livros"))

        cursor.execute("""
            SELECT *
            FROM livros
            ORDER BY ativo DESC, titulo ASC
        """)
        lista_livros = cursor.fetchall()

        return render_template(
            "livros.html",
            livros=lista_livros
        )

    finally:
        cursor.close()
        conexao.close()


# =========================================
# EDITAR LIVRO
# =========================================

@app.route("/livros/<int:id>/editar", methods=["GET", "POST"])
def editar_livro(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        if request.method == "POST":
            titulo = request.form["titulo"].strip()
            autor = request.form["autor"].strip()
            isbn = request.form.get("isbn", "").strip() or None
            categoria = request.form.get("categoria", "").strip() or None
            ano_publicacao = request.form.get("ano_publicacao") or None
            quantidade = request.form.get("quantidade", type=int)

            if not titulo or not autor or quantidade is None or quantidade < 0:
                flash("Preencha os campos corretamente.", "erro")
                return redirect(url_for("editar_livro", id=id))

            cursor.execute("""
                UPDATE livros
                SET titulo = %s,
                    autor = %s,
                    isbn = %s,
                    categoria = %s,
                    ano_publicacao = %s,
                    quantidade = %s
                WHERE id = %s
            """, (
                titulo,
                autor,
                isbn,
                categoria,
                ano_publicacao,
                quantidade,
                id
            ))

            conexao.commit()
            flash("Livro atualizado com sucesso!", "sucesso")
            return redirect(url_for("livros"))

        cursor.execute(
            "SELECT * FROM livros WHERE id = %s",
            (id,)
        )
        livro = cursor.fetchone()

        if not livro:
            flash("Livro não encontrado.", "erro")
            return redirect(url_for("livros"))

        return render_template("editar_livro.html", livro=livro)

    finally:
        cursor.close()
        conexao.close()


# =========================================
# DESATIVAR LIVRO
# =========================================

@app.route("/livros/<int:id>/excluir", methods=["POST"])
def excluir_livro(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, ativo
            FROM livros
            WHERE id = %s
        """, (id,))
        livro = cursor.fetchone()

        if not livro:
            flash("Livro não encontrado.", "erro")
            return redirect(url_for("livros"))

        if not livro["ativo"]:
            flash("Este livro já está desativado.", "erro")
            return redirect(url_for("livros"))

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM emprestimos
            WHERE livro_id = %s
              AND data_devolucao IS NULL
        """, (id,))

        resultado = cursor.fetchone()

        if resultado["total"] > 0:
            flash(
                "Não é possível desativar este livro: "
                "há empréstimo(s) ainda não devolvido(s).",
                "erro"
            )
            return redirect(url_for("livros"))

        cursor.execute("""
            UPDATE livros
            SET ativo = 0
            WHERE id = %s
        """, (id,))

        conexao.commit()
        flash(
            "Livro desativado. O histórico de empréstimos foi preservado.",
            "sucesso"
        )
        return redirect(url_for("livros"))

    finally:
        cursor.close()
        conexao.close()


# =========================================
# REATIVAR LIVRO
# =========================================

@app.route("/livros/<int:id>/reativar", methods=["POST"])
def reativar_livro(id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE livros
            SET ativo = 1
            WHERE id = %s
        """, (id,))

        if cursor.rowcount == 0:
            conexao.rollback()
            flash("Livro não encontrado.", "erro")
        else:
            conexao.commit()
            flash("Livro reativado com sucesso!", "sucesso")

        return redirect(url_for("livros"))

    finally:
        cursor.close()
        conexao.close()


# =========================================
# USUÁRIOS
# =========================================

@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        if request.method == "POST":
            nome = request.form["nome"].strip()
            email = request.form["email"].strip()
            telefone = request.form.get("telefone", "").strip() or None
            data_cadastro = request.form["data_cadastro"]

            if not nome or not email or not data_cadastro:
                flash("Preencha os campos obrigatórios.", "erro")
                return redirect(url_for("usuarios"))

            cursor.execute("""
                INSERT INTO usuarios
                    (nome, email, telefone, data_cadastro, ativo)
                VALUES (%s, %s, %s, %s, 1)
            """, (
                nome,
                email,
                telefone,
                data_cadastro
            ))

            conexao.commit()
            flash("Usuário cadastrado com sucesso!", "sucesso")
            return redirect(url_for("usuarios"))

        cursor.execute("""
            SELECT *
            FROM usuarios
            ORDER BY ativo DESC, nome ASC
        """)
        lista_usuarios = cursor.fetchall()

        return render_template(
            "usuario.html",
            usuarios=lista_usuarios
        )

    finally:
        cursor.close()
        conexao.close()


# =========================================
# EDITAR USUÁRIO
# =========================================

@app.route("/usuarios/<int:id>/editar", methods=["GET", "POST"])
def editar_usuario(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        if request.method == "POST":
            nome = request.form["nome"].strip()
            email = request.form["email"].strip()
            telefone = request.form.get("telefone", "").strip() or None

            if not nome or not email:
                flash("Preencha os campos obrigatórios.", "erro")
                return redirect(url_for("editar_usuario", id=id))

            cursor.execute("""
                UPDATE usuarios
                SET nome = %s,
                    email = %s,
                    telefone = %s
                WHERE id = %s
            """, (nome, email, telefone, id))

            conexao.commit()
            flash("Usuário atualizado com sucesso!", "sucesso")
            return redirect(url_for("usuarios"))

        cursor.execute(
            "SELECT * FROM usuarios WHERE id = %s",
            (id,)
        )
        usuario = cursor.fetchone()

        if not usuario:
            flash("Usuário não encontrado.", "erro")
            return redirect(url_for("usuarios"))

        return render_template(
            "editar_usuario.html",
            usuario=usuario
        )

    finally:
        cursor.close()
        conexao.close()


# =========================================
# DESATIVAR USUÁRIO
# =========================================

@app.route("/usuarios/<int:id>/excluir", methods=["POST"])
def excluir_usuario(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, ativo
            FROM usuarios
            WHERE id = %s
        """, (id,))
        usuario = cursor.fetchone()

        if not usuario:
            flash("Usuário não encontrado.", "erro")
            return redirect(url_for("usuarios"))

        if not usuario["ativo"]:
            flash("Este usuário já está desativado.", "erro")
            return redirect(url_for("usuarios"))

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM emprestimos
            WHERE usuario_id = %s
              AND data_devolucao IS NULL
        """, (id,))

        resultado = cursor.fetchone()

        if resultado["total"] > 0:
            flash(
                "Não é possível desativar este usuário: "
                "há empréstimo(s) ainda não devolvido(s).",
                "erro"
            )
            return redirect(url_for("usuarios"))

        cursor.execute("""
            UPDATE usuarios
            SET ativo = 0
            WHERE id = %s
        """, (id,))

        conexao.commit()
        flash(
            "Usuário desativado. O histórico de empréstimos foi preservado.",
            "sucesso"
        )
        return redirect(url_for("usuarios"))

    finally:
        cursor.close()
        conexao.close()


# =========================================
# REATIVAR USUÁRIO
# =========================================

@app.route("/usuarios/<int:id>/reativar", methods=["POST"])
def reativar_usuario(id):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            UPDATE usuarios
            SET ativo = 1
            WHERE id = %s
        """, (id,))

        if cursor.rowcount == 0:
            conexao.rollback()
            flash("Usuário não encontrado.", "erro")
        else:
            conexao.commit()
            flash("Usuário reativado com sucesso!", "sucesso")

        return redirect(url_for("usuarios"))

    finally:
        cursor.close()
        conexao.close()


# =========================================
# EMPRÉSTIMOS
# =========================================

@app.route("/emprestimos", methods=["GET", "POST"])
def emprestimos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        if request.method == "POST":
            usuario_id = request.form.get("usuario_id", type=int)
            livro_id = request.form.get("livro_id", type=int)
            data_emprestimo = request.form.get("data_emprestimo")
            data_prevista = request.form.get("data_devolucao_prevista")

            if not all([
                usuario_id,
                livro_id,
                data_emprestimo,
                data_prevista
            ]):
                flash("Preencha todos os campos do empréstimo.", "erro")
                return redirect(url_for("emprestimos"))

            if data_prevista < data_emprestimo:
                flash(
                    "A data prevista de devolução não pode ser anterior "
                    "à data do empréstimo.",
                    "erro"
                )
                return redirect(url_for("emprestimos"))

            # Confere se o usuário está ativo.
            cursor.execute("""
                SELECT id
                FROM usuarios
                WHERE id = %s AND ativo = 1
            """, (usuario_id,))

            if not cursor.fetchone():
                flash("Selecione um usuário ativo.", "erro")
                return redirect(url_for("emprestimos"))

            # Confere se o livro está ativo e tem exemplares disponíveis.
            cursor.execute("""
                SELECT id, quantidade
                FROM livros
                WHERE id = %s
                  AND ativo = 1
                  AND quantidade > 0
                FOR UPDATE
            """, (livro_id,))

            livro = cursor.fetchone()

            if not livro:
                flash(
                    "Livro indisponível, desativado ou sem exemplares.",
                    "erro"
                )
                return redirect(url_for("emprestimos"))

            # Registra o empréstimo.
            cursor.execute("""
                INSERT INTO emprestimos
                    (usuario_id, livro_id, data_emprestimo,
                     data_devolucao_prevista)
                VALUES (%s, %s, %s, %s)
            """, (
                usuario_id,
                livro_id,
                data_emprestimo,
                data_prevista
            ))

            # Atualiza o estoque disponível.
            cursor.execute("""
                UPDATE livros
                SET quantidade = quantidade - 1
                WHERE id = %s
                  AND quantidade > 0
            """, (livro_id,))

            if cursor.rowcount != 1:
                conexao.rollback()
                flash("Não foi possível atualizar o estoque.", "erro")
                return redirect(url_for("emprestimos"))

            conexao.commit()
            flash("Empréstimo registrado com sucesso!", "sucesso")
            return redirect(url_for("emprestimos"))

        # Histórico completo: inclui registros antigos e devolvidos.
        cursor.execute("""
            SELECT
                e.id,
                e.usuario_id,
                e.livro_id,
                u.nome AS usuario,
                l.titulo AS livro,
                e.data_emprestimo,
                e.data_devolucao_prevista,
                e.data_devolucao
            FROM emprestimos e
            INNER JOIN usuarios u ON e.usuario_id = u.id
            INNER JOIN livros l ON e.livro_id = l.id
            ORDER BY e.id DESC
        """)
        lista_emprestimos = cursor.fetchall()

        # Somente usuários ativos aparecem no formulário.
        cursor.execute("""
            SELECT id, nome
            FROM usuarios
            WHERE ativo = 1
            ORDER BY nome ASC
        """)
        lista_usuarios = cursor.fetchall()

        # Somente livros ativos e com estoque disponível.
        cursor.execute("""
            SELECT id, titulo, quantidade
            FROM livros
            WHERE ativo = 1
              AND quantidade > 0
            ORDER BY titulo ASC
        """)
        lista_livros = cursor.fetchall()

        return render_template(
            "emprestimos.html",
            emprestimos=lista_emprestimos,
            usuarios=lista_usuarios,
            livros=lista_livros
        )

    finally:
        cursor.close()
        conexao.close()


# =========================================
# DEVOLVER LIVRO
# =========================================

@app.route("/emprestimos/<int:id>/devolver", methods=["POST"])
def devolver_emprestimo(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, livro_id, data_devolucao
            FROM emprestimos
            WHERE id = %s
            FOR UPDATE
        """, (id,))

        emprestimo = cursor.fetchone()

        if not emprestimo:
            flash("Empréstimo não encontrado.", "erro")
            return redirect(url_for("emprestimos"))

        if emprestimo["data_devolucao"] is not None:
            flash("Este empréstimo já foi devolvido.", "erro")
            return redirect(url_for("emprestimos"))

        cursor.execute("""
            UPDATE emprestimos
            SET data_devolucao = CURDATE()
            WHERE id = %s
              AND data_devolucao IS NULL
        """, (id,))

        if cursor.rowcount != 1:
            conexao.rollback()
            flash("Não foi possível registrar a devolução.", "erro")
            return redirect(url_for("emprestimos"))

        cursor.execute("""
            UPDATE livros
            SET quantidade = quantidade + 1
            WHERE id = %s
        """, (emprestimo["livro_id"],))

        conexao.commit()
        flash("Devolução registrada com sucesso!", "sucesso")
        return redirect(url_for("emprestimos"))

    finally:
        cursor.close()
        conexao.close()


# =========================================
# EXECUTAR A APLICAÇÃO
# =========================================

if __name__ == "__main__":
    app.run(debug=True)
