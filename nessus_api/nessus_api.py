#!/usr/bin/python3
#Criado por: Argemiro Silva

import argparse
import requests
import json
from prettytable import PrettyTable

# Criar argumentos de linha de comando para URL, nome de usuário e senha
parser = argparse.ArgumentParser(description="Listar todos os scans da API do Nessus.")
parser.add_argument("-u", "--url", type=str, required=True, help="URL da API do Nessus.")
parser.add_argument("-n", "--username", type=str, required=True, help="Nome de usuário para a API do Nessus.")
parser.add_argument("-p", "--password", type=str, required=True, help="Senha para a API do Nessus.")
args = parser.parse_args()

url = args.url
username = args.username
password = args.password

# Desativar verificação de SSL, se necessário
verify_ssl = False
if not verify_ssl:
    requests.packages.urllib3.disable_warnings()
    print("Verificação SSL desativada. Isso não é recomendado em ambientes de produção.")

# Fazer login na API do Nessus e obter token de autenticação
login_url = f"{url}/session"
login_data = {"username": username, "password": password}
response = requests.post(login_url, json=login_data, verify=verify_ssl)
token = response.json()["token"]

# Definir cabeçalhos da requisição com token de autenticação
headers = {
    "X-Cookie": f"token={token}",
    "Content-Type": "application/json"
}

# Fazer uma solicitação GET para obter uma lista de todos os scans disponíveis na API do Nessus
scans_url = f"{url}/scans"
response = requests.get(scans_url, headers=headers, verify=verify_ssl)
scans = response.json()

# Criar uma tabela para exibir os resultados e definir as colunas da tabela
table = PrettyTable()
table.field_names = ["ID", "Nome", "ID da pasta", "Status", "Data de criação"]

# Iterar sobre todos os scans e adicionar uma nova linha à tabela para cada um
for scan in scans["scans"]:
    table.add_row([
        scan['id'],
        scan['name'],
        scan['folder_id'],
        scan['status'],
        scan['creation_date']
    ])

# Exibir a tabela com os resultados
print(table)

# Fazer download em formato Nessus do scan pelo ID
scan_id = input("Digite o ID do scan para download: ")
download_url = f"{url}/scans/{scan_id}/export"
download_payload = {
    "format": "nessus"
}
download_response = requests.post(download_url, headers=headers, json=download_payload, verify=verify_ssl)

# Salvar o arquivo Nessus no disco
file_name = f"{scan_id}.nessus"
with open(file_name, "wb") as f:
    f.write(download_response.content)

print(f"O arquivo {file_name} foi salvo com sucesso!")
