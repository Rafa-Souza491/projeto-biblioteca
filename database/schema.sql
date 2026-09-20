SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS biblioteca
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE biblioteca;

-- =========================================
-- TABELA DE LIVROS
-- =========================================

CREATE TABLE IF NOT EXISTS livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    isbn VARCHAR(20),
    categoria VARCHAR(50),
    ano_publicacao INT,
    quantidade INT NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- =========================================
-- DADOS INICIAIS DOS LIVROS
-- =========================================

INSERT INTO livros
    (titulo, autor, isbn, categoria, ano_publicacao, quantidade)
SELECT * FROM (
    SELECT
        '1984' AS titulo,
        'George Orwell' AS autor,
        '9780451524935' AS isbn,
        'Ficção' AS categoria,
        1949 AS ano_publicacao,
        5 AS quantidade

    UNION ALL

    SELECT
        'A Revolução dos Bichos',
        'George Orwell',
        '9780451526342',
        'Ficção',
        1945,
        4

    UNION ALL

    SELECT
        'Dom Casmurro',
        'Machado de Assis',
        '9788535911665',
        'Romance',
        1899,
        3

    UNION ALL

    SELECT
        'Harry Potter e a Pedra Filosofal',
        'J. K. Rowling',
        '9788532511010',
        'Fantasia',
        1997,
        6

    UNION ALL

    SELECT
        'O Hobbit',
        'J. R. R. Tolkien',
        '9788595084742',
        'Fantasia',
        1937,
        5

    UNION ALL

    SELECT
        'O Pequeno Príncipe',
        'Antoine de Saint-Exupéry',
        '9788522031447',
        'Infantil',
        1943,
        7

    UNION ALL

    SELECT
        'Orgulho e Preconceito',
        'Jane Austen',
        '9788544001820',
        'Romance',
        1813,
        4

    UNION ALL

    SELECT
        'Sherlock Holmes',
        'Arthur Conan Doyle',
        '9788537801815',
        'Mistério',
        1887,
        3

    UNION ALL

    SELECT
        'O Senhor dos Anéis',
        'J. R. R. Tolkien',
        '9788595086357',
        'Fantasia',
        1954,
        5

    UNION ALL

    SELECT
        'Vinte Mil Léguas Submarinas',
        'Júlio Verne',
        '9788520929395',
        'Aventura',
        1870,
        2
) AS livros_iniciais
WHERE NOT EXISTS (
    SELECT 1
    FROM livros
);

-- =========================================
-- TABELA DE USUÁRIOS - AC2
-- =========================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefone VARCHAR(20),
    data_cadastro DATE NOT NULL
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- =========================================
-- DADOS INICIAIS DOS USUÁRIOS
-- =========================================

INSERT INTO usuarios
    (nome, email, telefone, data_cadastro)
SELECT * FROM (
    SELECT
        'Ana Souza' AS nome,
        'ana.souza@email.com' AS email,
        '11987654321' AS telefone,
        '2026-09-01' AS data_cadastro

    UNION ALL

    SELECT
        'Bruno Oliveira',
        'bruno.oliveira@email.com',
        '11987654322',
        '2026-09-02'

    UNION ALL

    SELECT
        'Carlos Santos',
        'carlos.santos@email.com',
        '11987654323',
        '2026-09-03'

    UNION ALL

    SELECT
        'Mariana Costa',
        'mariana.costa@email.com',
        '11987654324',
        '2026-09-04'

    UNION ALL

    SELECT
        'Rafael Almeida',
        'rafael.almeida@email.com',
        '11987654325',
        '2026-09-05'
) AS usuarios_iniciais
WHERE NOT EXISTS (
    SELECT 1
    FROM usuarios
);

-- =========================================
-- TABELA DE EMPRESTIMOS - AC2
-- =========================================

CREATE TABLE IF NOT EXISTS emprestimos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    livro_id INT NOT NULL,
    data_emprestimo DATE NOT NULL,
    data_devolucao_prevista DATE NOT NULL,
    data_devolucao DATE NULL,

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id),

    FOREIGN KEY (livro_id)
        REFERENCES livros(id)
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;