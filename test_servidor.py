import pytest
import json
from servidor import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_listar_imoveis(client):
    resp = client.get('/imoveis')
    assert resp.status_code == 200

def test_obter_imovel(client):
    resp = client.get('/imoveis/1')
    assert resp.status_code in [200, 404]

def test_adicionar_imovel(client):
    novo_imovel = {
        'logradouro': 'Rua Exemplo',
        'tipo_logradouro': 'Rua',
        'bairro': 'Bairro Teste',
        'cidade': 'Cidade Teste',
        'cep': '00000-000',
        'tipo': 'teste',
        'valor': 1000.0,
        'data_aquisicao': '2025-01-01'
    }
    resp = client.post(
        '/imoveis',
        data=json.dumps(novo_imovel),
        content_type='application/json'
    )
    assert resp.status_code in [201, 400]

def test_atualizar_imovel(client):
    imovel_atualizado = {
        'logradouro': 'Rua Atualizada',
        'tipo_logradouro': 'Avenida',
        'bairro': 'Bairro Atual',
        'cidade': 'Cidade Atual',
        'cep': '11111-111',
        'tipo': 'atualizado',
        'valor': 2000.0,
        'data_aquisicao': '2025-02-02'
    }
    resp = client.put(
        '/imoveis/1',
        data=json.dumps(imovel_atualizado),
        content_type='application/json'
    )
    assert resp.status_code in [204, 404]

def test_remover_imovel(client):
    resp = client.delete('/imoveis/1')
    assert resp.status_code in [204, 404]