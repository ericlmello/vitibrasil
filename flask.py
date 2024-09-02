from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup




# Função para realizar o scraping de uma tabela específica em uma página
def scrape_table(url, table_class):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar a tabela baseada na classe identificada
    table = soup.find('table', {'class': table_class})

    if not table:
        print(f"Tabela não encontrada na URL: {url}")
        return []

    # Processar as linhas da tabela
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = []
    for row in table.find_all('tr')[1:]:  # Pular o cabeçalho
        cols = [col.text.strip() for col in row.find_all('td')]
        rows.append(cols)

    return headers, rows

# URLs das abas
urls = {
    "Produção": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02",
    "Processamento": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03",
    "Comercialização": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04",
    "Importação": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05",
    "Exportação": "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06",
}

# Classe CSS usada para identificar a tabela com os dados
table_class = "tb_base tb_dados"

# Scraping de cada aba
for nome, url in urls.items():
    print(f"Scraping dados de {nome}...")
    headers, rows = scrape_table(url, table_class)

    if headers and rows:
        print(f"Headers: {headers}")
        print("Rows:")
        for row in rows:
            print(row)
    else:
        print(f"Nenhum dado encontrado para {nome}.")
    print("\n")


app = Flask(__name__)

# Função para realizar o scraping de uma tabela específica em uma página
def scrape_table(url, table_class):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': table_class})

    if not table:
        return {"error": "Table not found"}, 404

    headers = [header.text.strip() for header in table.find_all('th')]
    rows = []
    for row in table.find_all('tr')[1:]:  # Pular o cabeçalho
        cols = [col.text.strip() for col in row.find_all('td')]
        rows.append(dict(zip(headers, cols)))

    return rows

# Rota para produção
@app.route('/producao', methods=['GET'])
def producao():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"
    data = scrape_table(url, 'tb_base tb_dados')
    return jsonify(data)

# Rota para processamento
@app.route('/processamento', methods=['GET'])
def processamento():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03"
    data = scrape_table(url, 'tb_base tb_dados')
    return jsonify(data)

# Rota para comercialização
@app.route('/comercializacao', methods=['GET'])
def comercializacao():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04"
    data = scrape_table(url, 'tb_base tb_dados')
    return jsonify(data)

# Rota para importação
@app.route('/importacao', methods=['GET'])
def importacao():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05"
    data = scrape_table(url, 'tb_base tb_dados')
    return jsonify(data)

# Rota para exportação
@app.route('/exportacao', methods=['GET'])
def exportacao():
    url = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06"
    data = scrape_table(url, 'tb_base tb_dados')
    return jsonify(data)

# Iniciar o servidor
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
