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
parser.add_argument("-i", "--id", type=int, help="ID do scan para baixar relatório em formato Nessus.")
args = parser.parse_args()

url = args.url
username = args.username
password = args.password
scan_id = args.id

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

# Baixar um relatório em formato Nessus pelo ID do scan fornecido
if scan_id:
    download_url = f"{url}/scans/{scan_id}/export"
    download_data = {"format": "nessus"}
    response = requests.post(download_url, headers=headers, json=download_data, verify=verify_ssl)
    file_id = response.json()["file"]

    # Aguardar a geração do relatório
    while True:
        status_url = f"{url}/scans/{scan_id}/export/{file_id}/status"
        response = requests.get(status_url, headers=headers, verify=verify_ssl)
        status = response.json()["status"]
        if status == "ready":
            break
        print("Aguardando a geração do relatório...")
        time.sleep(10)

    # Fazer o download do relatório em formato Nessus
    download_url = f"{url}/scans/{scan_id}/export/{file_id}/download"
    response = requests.get(download_url, headers=headers, verify=verify_ssl)

    # Salvar o arquivo Nessus localmente
    with open(f"nessus_scan_{scan_id}.nessus", "wb") as f:
        f.write(response.content)

    print(f"Relatório Nessus salvo como nessus_scan_{scan_id}.nessus")
