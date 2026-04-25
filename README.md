# Urna Eletrônica (Projeto Integrador I)

Backend de uma Urna eletronica ficticia.


Integrantes:
Arthur Alves Raymundi
Gabriel Souza Gonçalves
Kaiky de Mello Rosa Severino
Luís Felippe Travaglini


Tecnologias:
Python 3.14.3
MySQL
Biblioteca Python: mysql-connector-python


Pré-requisitos
Python 3.14.3 instalado
Git instalado
MySQL instalado e rodando


Clonar o repositório:
git clone https://github.com/LuisTravaglini/ES-PI1-2026-T2-G01.git
cd ES-PI1-2026-T2-G01


Ambiente virtual (venv) e dependências:

macOS / Linux

Criar o ambiente virtual (uma vez):
python3 -m venv .venv

Ativar:
source .venv/bin/activate

Instalar dependências:
pip install -r requirements.txt

Desativar quando terminar:
deactivate


Windows (PowerShell)

Criar o ambiente virtual (uma vez):
py -m venv .venv

Ativar:
.\.venv\Scripts\Activate.ps1

Instalar dependências:
pip install -r requirements.txt

Desativar:
deactivate

Se o PowerShell bloquear a ativação, execute uma vez:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


Importar/criar estrutura do banco (macOS / Linux)
mysql -u root -p < sist_votacao.sql
Importar/criar estrutura do banco (Windows PowerShell)
mysql -u root -p < sist_votacao.sql

Observação: se o comando mysql não for reconhecido no Windows, é necessário adicionar o MySQL ao PATH ou executar pelo terminal do MySQL instalado.

Como executar o sistema
Com o ambiente virtual ativado:

macOS / Linux
python3 setup.py
Windows
python setup.py
