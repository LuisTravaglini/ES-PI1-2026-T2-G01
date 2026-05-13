from conexao import get_conexao
conexao = get_conexao()
cursor = conexao.cursor()

query = """
        SELECT tipo_mesario
        LEFT(CPF,4) AS primeiros_digitos
        FROM eleitor
        WHERE titulo = %s
        AND CPF = %s
        AND chave_Acesso = %s"""
                        

cursor.execute(query, (titulo, CPF, chave_Acesso))

eleitor = cursor.fetchone()

if tipo_mesario == 1:
    print("Mesário")
else:
    print("Não é possivel acessar")