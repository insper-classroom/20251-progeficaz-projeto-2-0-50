from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': os.getenv("MYSQL_HOST"),
    'port': int(os.getenv("MYSQL_PORT", 3306)),
    'user': os.getenv("MYSQL_USER"),
    'password': os.getenv("MYSQL_PASSWORD"),
    'database': os.getenv("MYSQL_DATABASE"),
}

@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    tipo = request.args.get('tipo')
    cidade = request.args.get('cidade')
    if tipo:
        query = "SELECT * FROM imoveis WHERE tipo = %s"
        cursor.execute(query, (tipo,))
    elif cidade:
        query = "SELECT * FROM imoveis WHERE cidade = %s"
        cursor.execute(query, (cidade,))
    else:
        cursor.execute("SELECT * FROM imoveis")
    imoveis = cursor.fetchall()
    conn.close()
    return jsonify(imoveis)

@app.route('/imoveis/<int:imovel_id>', methods=['GET'])
def obter_imovel(imovel_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (imovel_id,))
    imovel = cursor.fetchone()
    conn.close()
    return jsonify(imovel) if imovel else ('', 404)

@app.route('/imoveis', methods=['POST'])
def adicionar_imovel():
    data = request.json
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (data['logradouro'], data['tipo_logradouro'], data['bairro'], data['cidade'], data['cep'], data['tipo'], data['valor'], data['data_aquisicao'])
    )
    conn.commit()
    conn.close()
    return ('', 201)

@app.route('/imoveis/<int:imovel_id>', methods=['PUT'])
def atualizar_imovel(imovel_id):
    data = request.json
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        (data['logradouro'], data['tipo_logradouro'], data['bairro'], data['cidade'], data['cep'], data['tipo'], data['valor'], data['data_aquisicao'], imovel_id)
    )
    conn.commit()
    conn.close()
    return ('', 204)

@app.route('/imoveis/<int:imovel_id>', methods=['DELETE'])
def remover_imovel(imovel_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (imovel_id,))
    conn.commit()
    conn.close()
    return ('', 204)

if __name__ == '__main__':
    app.run(debug=True)