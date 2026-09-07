CREATE DATABASE IF NOT EXISTS biblioteca;

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

);


-- =========================================
-- DADOS INICIAIS
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