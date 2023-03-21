#!/usr/bin/python3
#Criado por: Argemiro Silva

import requests
import json
import argparse

# Define os argumentos de entrada
parser = argparse.ArgumentParser(description='Lista todos os scans disponíveis no Nessus.')
parser.add_argument('url', help='URL do Nessus')
parser.add_argument('username', help='Nome de usuário do Nessus')
parser.add_argument('password', help='Senha do Nessus')
args = parser.parse_args()

nessus_url = args.url + '/nessus'
username = args.username
password = args.password

# Desabilita a verificação de SSL para evitar problemas com servidores sem certificado válido
verify_ssl = False

# Obtém o token de sessão necessário para autenticar na API do Nessus
response = requests.post(nessus_url + '/session', json={'username': username, 'password': password}, verify=verify_ssl)

# Verifica se a resposta da API foi bem sucedida (código 200)
if response.status_code == 200:
    token = json.loads(response.content)['token']
    headers = {'X-Cookie': 'token=' + token}

    # Lista todos os scans disponíveis no Nessus
    response = requests.get(nessus_url + '/scans', headers=headers, verify=verify_ssl)

    # Verifica se a resposta da API foi bem sucedida (código 200)
    if response.status_code == 200:
        scans = json.loads(response.content)
        print('Lista de scans:')
        print('{:<10} {:<50} {:<20} {:<10} {:<20}'.format('ID', 'Nome', 'ID da pasta', 'Status', 'Data de criação'))
        for scan in scans['scans']:
            print('{:<10} {:<50} {:<20} {:<10} {:<20}'.format(scan['id'], scan['name'], scan['folder_id'], scan['status'], scan['creation_date']))
    else:
        print('Erro ao acessar a API do Nessus:', response.status_code)
else:
    # Tentativa de autenticação utilizando a URL da API mais antiga (Nessus v6 e anteriores)
    nessus_url = args.url + '/api'
    response = requests.post(nessus_url + '/session', json={'username': username, 'password': password}, verify=verify_ssl)

    # Verifica se a resposta da API foi bem sucedida (código 200)
    if response.status_code == 200:
        token = json.loads(response.content)['token']
        headers = {'X-Cookie': 'token=' + token}

        # Lista todos os scans disponíveis no Nessus
        response = requests.get(nessus_url + '/scans', headers=headers, verify=verify_ssl)

        # Verifica se a resposta da API foi bem sucedida (código 200)
        if response.status_code == 200:
            scans = json.loads(response.content)
            print('Lista de scans:')
            print('{:<10} {:<50} {:<20} {:<10} {:<20}'.format('ID', 'Nome', 'ID da pasta', 'Status', 'Data de criação'))
            for scan in scans['scans']:
                print('{:<10} {:<50} {:<20} {:<10} {:<20}'.format(scan['id'], scan['name'], scan['folder_id'], scan['status'], scan['creation_date']))
        else:
            print('Erro ao acessar a API do Nessus:', response.status_code)
   
