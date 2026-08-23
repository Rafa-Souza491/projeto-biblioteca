import sqlite3

DATABASE = "database/biblioteca.db"


def conectar():
    return sqlite3.connect(DATABASE)