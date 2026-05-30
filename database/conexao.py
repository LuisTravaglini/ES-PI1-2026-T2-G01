import mysql.connector

def get_conexao():
    return mysql.connector.connect(
        host="localhost",
        database="sist_votacao",
        user="root",
        password="1234"
    )