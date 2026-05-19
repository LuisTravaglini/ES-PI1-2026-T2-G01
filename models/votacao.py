LOG = "logs/auditoria.log"

def abrir_votacao(cursor, conexao, votacao_aberta):
    if votacao_aberta:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("\n\t ⚠️ Tentativa de abrir votação já aberta")
    else:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("\n\t ✅ Votação ABERTA! Votos podem ser registrados")

    titulo = input("Digite seu titulo: ")
    cpf = input("Digite os 4 primeiros dígitos do CPF: ")
    chave = input("Digite sua chave de acesso: ")

    query = """
    SELECT tipo_mesario,
        LEFT(CPF,4) AS primeiros_digitos
    FROM eleitor
    WHERE titulo = %s
    AND LEFT(CPF,4) = %s
    AND chave_Acesso = %s;
    """

    cursor.execute(query, (titulo, cpf, chave))
    result = cursor.fetchall()

    if result == 0:
        print("Não possui permissão, tente novamente com perfil de mesário.")
    else:
        print("É mesário, iniciando votação...")

    zerar_votos(cursor, conexao)

    print("\n=== Zerézima ===\n")
    input("\nPressione Enter para voltar...")
    return True


def encerrar_votacao(votacao_aberta):
    if not votacao_aberta:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("\n\t ⚠️ Tentativa de encerrar votação ainda não aberta!")
        print("A votação não está aberta.")
    else:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("\n\t 🔒 A votação foi ENCERRADA!")
        print("Votação encerrada.")
    input("\nPressione Enter para voltar...")
    return False
    


def auditoria(votacao_aberta):
    if not votacao_aberta:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("\n\t ⚠️ Para auditar, a votação precisa estar aberta!")
        print("A votação precisa estar aberta para auditar.")
    input("\nPressione Enter para voltar...")



def resultado(cursor):
    cursor.execute("""
    SELECT candidato.nome_Completo,
           candidato.numero_Candidato,
           COUNT(registro_voto.id) AS total_votos
    FROM candidato
    LEFT JOIN registro_voto ON candidato.numero_Candidato = registro_voto.numero_Candidato
    GROUP BY candidato.id_candidato, candidato.nome_Completo, candidato.numero_Candidato
    ORDER BY total_votos DESC
    """)
    for c in cursor.fetchall():
        print(f"{c[0]} (Nº {c[1]}) — {c[2]} votos")
    input("\nPressione Enter para voltar...")


def zerar_votos(cursor, conexao):
    cursor.execute("DELETE FROM registro_voto;")
    conexao.commit()
    input("\nPressione Enter para voltar...")