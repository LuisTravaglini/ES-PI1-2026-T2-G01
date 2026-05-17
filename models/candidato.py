def listar_candidatos(cursor):
    cursor.execute("SELECT nome_Completo, numero_Candidato FROM candidato")
    candidatos = cursor.fetchall()
    for c in candidatos:
        print(f"Candidato: {c[0]} (Nº {c[1]})")
    input("\nPressione Enter para voltar...")