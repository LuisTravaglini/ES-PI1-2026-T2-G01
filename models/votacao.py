LOG = "logs/auditoria.log"

import random
import string
from datetime import datetime

def abrir_votacao(cursor, conexao, votacao_aberta):
    if votacao_aberta:
        with open(LOG, "a", encoding="utf-8") as f:
            horario = datetime.now().strftime('%D/%M/%Y %H:%M%S')
            f.write(f"\n\t ⚠️ {horario} - ALERTA: Tentativa de abrir votação já aberta")
    else:
        with open(LOG, "a", encoding="utf-8") as f:
            horario = datetime.now().strftime('%D/%M/%Y %H:%M%S')
            f.write(f"\n\t {horario} - ✅ ABERTURA: Votação iniciada com sucesso. Total de votos zerado")

    titulo = input("Digite seu titulo: ")
    cpf = input("Digite os 4 primeiros dígitos do CPF: ")
    chave = input("Digite sua chave de acesso: ")

    query = """
    SELECT tipo_mesario
    FROM eleitor
    WHERE titulo = %s
    AND LEFT(CPF,4) = %s
    AND chave_Acesso = %s;
    """
    cursor.execute(query, (titulo, cpf, chave))
    result = cursor.fetchone()

    if result:
        tipo_mesario = result[0]

        if tipo_mesario:
            print("É mesário, iniciando votação...")
        else:
            with open(LOG, "a", encoding="utf-8") as f:
                horario = datetime.now().strftime('%D/%M/%Y %H:%M%S')
                f.write(f"\n\t {horario} - ⚠️ ALERTA: Tentativa de acesso negado")
            print("Você não possui permissão de mesário.")
            input("\nPressione Enter para voltar...")
            return False

    else:
        print("Dados inválidos.")
        input("\nPressione Enter para voltar...")
        return False

    zerar_votos(cursor, conexao)

    print("\n=== Zerézima ===\n")
    input("\nPressione Enter para voltar...")
    return True


def encerrar_votacao(votacao_aberta):
    resp = input("Deseja realmente encerrar a votação?(sim/não): ")

    if resp.lower() == "sim":

        if not votacao_aberta:
            with open(LOG, "a", encoding="utf-8") as f:
                horario = datetime.now().strftime('%D/%M/%Y %H:%M%S')
                f.write(f"\n\t {horario} - ⚠️ Tentativa de encerrar votação ainda não aberta!")
            print("A votação não está aberta.")
        else:
            with open(LOG, "a", encoding="utf-8") as f:
                horario = datetime.now().strftime('%D/%M/%Y %H:%M%S')
                f.write(f"\n\t {horario} - 🔒 A votação foi ENCERRADA!")
            print("Votação encerrada.")
        input("\nPressione Enter para voltar...")
        return False

    else:
        print("\nVocê não tem permissão para encerrar a votação.")
        
        return True
    


def auditoria(votacao_aberta):
    if not votacao_aberta:
        with open(LOG, "a", encoding="utf-8") as f:
            horario = datetime.now().strftime('%D/%M/%Y %H:%M%S')
            f.write(f"\n\t {horario} - ⚠️ ALERTA: Para auditar, a votação precisa estar aberta!")
        print("A votação precisa estar aberta para auditar.")
    input("\nPressione Enter para voltar...")



def resultado(cursor):

    cursor.execute("""
    SELECT nome_Completo,
           numero_Candidato,
           partido,
           votos
    FROM candidato
    ORDER BY votos DESC
    """)

    candidatos = cursor.fetchall()

    if not candidatos:
        print("Nenhum candidato encontrado.")
        input("\nPressione Enter para voltar...")
        return

    print("=" * 40)
    print("RESULTADO DA ELEIÇÃO")
    print("=" * 40)

    # VENCEDOR
    vencedor = candidatos[0]

    print("\n🏆 VENCEDOR DA ELEIÇÃO")
    print(f"Nome: {vencedor[0]}")
    print(f"Número: {vencedor[1]}")
    print(f"Partido: {vencedor[2]}")
    print(f"Votos: {vencedor[3]}")

    print("\n" + "=" * 40)

    opcao = input("Deseja ver os demais candidatos? (s/n): ").lower()

    if opcao == "s":

        print("\n📊 TODOS OS RESULTADOS\n")

        for candidato in candidatos:

            print("=" * 30)
            print(f"Nome: {candidato[0]}")
            print(f"Número: {candidato[1]}")
            print(f"Partido: {candidato[2]}")
            print(f"Total de votos: {candidato[3]}")
            print("=" * 30)

    input("\nPressione Enter para voltar...")


def zerar_votos(cursor, conexao):

    # APAGA TODOS OS VOTOS
    cursor.execute("DELETE FROM registro_voto;")
    cursor.execute("""
                    UPDATE candidato
                    SET votos = 0
                    """)

    # RESETA STATUS DE VOTAÇÃO DOS ELEITORES
    cursor.execute("""
    UPDATE eleitor
    SET votou = FALSE
    """)

    conexao.commit()


def protocolo_votacao(numero_candidato):

    letras_aleatorias = ''.join(random.sample(string.ascii_uppercase, k=2))
    numeros_aleatorios = ''.join(map(str, random.sample(range(1, 9), k=5)))
    return f'V{letras_aleatorias}26{str(numero_candidato)}{numeros_aleatorios}'
    
    