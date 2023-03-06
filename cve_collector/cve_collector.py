# Nome: CVE Collector
# Versão: 2.0
# Elaborado por: Evandro Santos
# Elaborado em : 22 de fevereiro de 2023
# Descrição: Efetua a consulta à NVD e retorna os dados das CVEs Altas e Críticas publicadas
#            dentro de um dado período de tempo e as registra em um arquivo do tipo .html

import nvdlib
import datetime
import pandas as pd
import plotly.express as px
from jinja2 import Environment, FileSystemLoader

# Delimitação do Período de Coleta das Vulnerabilidades
end = datetime.datetime.now()
start = end - datetime.timedelta(days=7)

# Requisição das Vulnerabilidades de Severidades publicadas nos últimos XX dias.
results = nvdlib.searchCVE(cvssV3Severity='', pubStartDate=start, pubEndDate=end, key='', delay=50)

# Agrupa as CVEs por severidade
critical = []
high = []
medium = []
low = []
for result in results:
    if hasattr(result, 'v30score') and result.v30score >= 9.0:
        critical.append(result)
    elif hasattr(result, 'v31score') and result.v31score >= 9.0:
        critical.append(result)
    elif hasattr(result, 'v30score') and result.v30score >= 7.0 and result.v30score <= 8.9:
        high.append(result)
    elif hasattr(result, 'v31score') and result.v31score >= 7.0 and result.v31score <= 8.9:
        high.append(result)
    elif hasattr(result, 'v30score') and result.v30score >= 4.0 and result.v30score <= 6.9:
        medium.append(result)
    elif hasattr(result, 'v31score') and result.v31score >= 4.0 and result.v31score <= 6.9:
        medium.append(result)
    else:
        low.append(result)

# Criação de um DataFrame para visualização dos dados
df = pd.DataFrame({
    'Severidade': ['Crítica', 'Alta'],
    'Quantidade': [len(critical), len(high)]
})

# Criação de gráfico de barras para visualização dos dados
fig = px.bar(df, x='Severidade', y='Quantidade', title='Total de Vulnerabilidades x Severidades')

# Configuração do ambiente jinja2
env = Environment(loader=FileSystemLoader('/home/evandro/projetos/cve_collector/templates'))
template = env.get_template('dashboard.html')
output = template.render()


# Renderização do template com os dados
output = template.render(critical=critical, high=high, fig=fig.to_html(full_html=False, include_plotlyjs='cdn'))

# Criação e abertura do arquivo .html para escrita
with open("Boletim_CVE.html", "w") as file:
    file.write(output)
