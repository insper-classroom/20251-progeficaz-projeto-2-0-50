from flask import Flask, request, jsonify

app = Flask(__name__)
imoveis = {}

@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    return jsonify(list(imoveis.values())), 200

@app.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    if id in imoveis:
        return jsonify(imoveis[id]), 200
    return jsonify({'erro': 'Imóvel não encontrado'}), 404

@app.route('/imoveis', methods=['POST'])
def adicionar_imovel():
    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Dados inválidos'}), 400
    novo_id = len(imoveis) + 1
    imoveis[novo_id] = data
    return jsonify({'id': novo_id}), 201

@app.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    if id not in imoveis:
        return '', 404
    data = request.get_json()
    if not data:
        return jsonify({'erro': 'Dados inválidos'}), 400
    imoveis[id].update(data)
    return '', 204

@app.route('/imoveis/<int:id>', methods=['DELETE'])
def remover_imovel(id):
    if id not in imoveis:
        return '', 404
    del imoveis[id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)