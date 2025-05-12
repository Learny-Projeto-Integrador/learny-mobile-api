from api import mongo
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import database
from bson import ObjectId, errors
from pymongo import DESCENDING
from datetime import datetime


def get_children_by_id(id):
    # Buscar usuário no banco
    user_data = mongo.db.criancas.find_one({'_id': id})

    if user_data:
        return user_data
    else:
        return {'error': 'Erro ao buscar os dados da criança'}
    
def get_children_by_user(new_data):
    user_data = mongo.db.criancas.find_one({'usuario': new_data.user})

    if user_data:
        return user_data
    else:
        return {'error': 'Erro ao buscar os dados da criança'}
    
def get_ranking():
    criancas = mongo.db.criancas.find().sort("pontos", DESCENDING)

    if not criancas:
        return {'error': 'Erroa ao buscar os dados das crianças'}

    ranking = []
    for c in criancas:
        ranking.append({
            "id": str(c["_id"]),
            "foto": c.get("foto", ""),
            "nome": c.get("nome", ""),
            "pontos": c.get("pontos", 0)
        })

    return ranking
   

def register_children(data):
    foto = data.foto
    usuario = data.usuario
    nome = data.nome
    senha = generate_password_hash(data.senha)
    email = data.email
    dataNasc = data.dataNasc
    responsavel = data.responsavel
    
    if responsavel != "":
        try:
            responsavel = ObjectId(data.responsavel)
        except (errors.InvalidId, TypeError):
            return {'error': 'ID do responsável inválido.'}

    # Verifica se o usuário já existe
    children_data = mongo.db.criancas.find_one({'usuario': usuario})
    parent_data = mongo.db.pais.find_one({'usuario': usuario})

    if children_data or parent_data:
        return {'error': 'Usuário já existente'}

    # Sorteia 3 missões da coleção de missões diárias predefinidas
    missoes = list(mongo.db.diarias.aggregate([{ "$sample": { "size": 3 } }]))

    # Remove o _id (opcional, se você quiser evitar duplicidade de referência)
    for m in missoes:
        m.pop('_id', None)

    dados = {
        'foto': foto,
        'avatar': "",
        'usuario': usuario,
        'senha': senha,
        'nome': nome,
        'email': email,
        'dataNasc': dataNasc,
        'pontos': 0,
        'fasesConcluidas': 0,
        'medalhas': [],
        'medalhaSelecionada': {},
        'rankingAtual': 0,
        'missoesDiarias': missoes,
        'audio': True,
        'mundos': [{
            "mundo": 1,
            "faseAtual": "",
            "fases": [
                {
                    "fase": 1,
                    "concluida": False
                },
                {
                    "fase": 2,
                    "concluida": False
                },
                {
                    "fase": 3,
                    "concluida": False
                },
                {
                    "boss": 4,
                    "concluida": False
                }
            ]
        }],
        'responsavel': responsavel,
    }

    result = mongo.db.criancas.insert_one(dados)
    return {
    'message': 'Usuário cadastrado com sucesso!',
    'dados': {
        '_id': str(result.inserted_id),  # Convertemos para string para facilitar o uso em JSON
        'usuario': usuario,
        'nome': nome,
        # outros campos que quiser retornar
    }
}
    
def edit_children(id, new_data):
    try:
        # Certificar que o ID é do tipo ObjectId
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}
    
    if new_data.get('senha'):
        new_data['senha'] = generate_password_hash(new_data['senha'])
    else:
        # Se não houver nova senha, remove o campo para manter a antiga
        new_data.pop('senha', None)

    result = mongo.db.criancas.update_one(
        {'_id': obj_id},
        {'$set': new_data}
    )

    if result.matched_count > 0:
        return {'message': 'Dados atualizados com sucesso'}
    else:
        return {'error': 'Nenhuma alteração realizada'}
    
def edit_rankings():
     # Busca todas as crianças, ordenadas por pontos (maior para menor)
    criancas = list(mongo.db.criancas.find().sort('pontos', -1))

    # Atualiza o campo 'ranking' com a posição na lista
    for index, crianca in enumerate(criancas):
        mongo.db.criancas.update_one(
            {'_id': crianca['_id']},
            {'$set': {'rankingAtual': index + 1}}  # ranking começa em 1
        )
    
def edit_children_score(id, new_data, tipo_fase=None):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    existing_data = mongo.db.criancas.find_one({'_id': obj_id})
    if not existing_data:
        return {'error': 'Criança não encontrada'}

    updated_data = {}
    campos_somaveis = ['pontos', 'fasesConcluidas']
    pontos_bonus = 0
    missao_concluida_info = None
    medalhas_adicionadas = []

    for campo in campos_somaveis:
        valor_atual = existing_data.get(campo, 0)
        valor_novo = new_data.get(campo, 0)
        if isinstance(valor_atual, (int, float)) and isinstance(valor_novo, (int, float)):
            updated_data[campo] = valor_atual + valor_novo

    # Atualização das fases com base na sequência
    fase_sequencia = ['connect', 'memory', 'feeling', 'listening']

    mundos = existing_data.get('mundos', [])
    boss_concluido = False
    if tipo_fase in fase_sequencia:
        index_fase = fase_sequencia.index(tipo_fase)
        if mundos:
            fases = mundos[0].get('fases', [])
            if index_fase < len(fases):
                fase_info = fases[index_fase]
                if not fase_info.get('concluida', False):
                    fases[index_fase]['concluida'] = True
                    fase_atual = index_fase + 1  # faseAtual será 1 a 4

                    mongo.db.criancas.update_one(
                        {'_id': obj_id},
                        {
                            '$set': {
                                'mundos.0.fases': fases,
                                'mundos.0.faseAtual': fase_atual
                            }
                        }
                    )
                    # Marcar boss como concluído se for a fase listening
                    if tipo_fase == "listening":
                        boss_concluido = True

    # Checar por medalhas a serem atribuídas
    fases_concluidas = sum(1 for f in existing_data['mundos'][0]['fases'][:3] if f.get('concluida'))
    medalhas_existentes = existing_data.get('medalhas', [])

    def adicionar_medalha(nome_medalha):
        if nome_medalha not in [m.get("nome") for m in medalhas_existentes]:
            medalha = mongo.db.medalhas.find_one({'nome': nome_medalha})
            if medalha:
                medalha_com_data = dict(medalha)
                medalha_com_data['dataConquista'] = datetime.now().isoformat()
                mongo.db.criancas.update_one(
                    {'_id': obj_id},
                    {'$push': {'medalhas': medalha_com_data}}
                )
                medalhas_adicionadas.append(medalha_com_data)

    if fases_concluidas == 1:
        adicionar_medalha("Iniciando!")
    if fases_concluidas == 3:
        adicionar_medalha("A todo o vapor!")
    if boss_concluido:
        adicionar_medalha("Desvendando")

    # Missões diárias
    missoes = existing_data.get('missoesDiarias', [])
    missao_removida = None

    if tipo_fase and isinstance(missoes, list):
        for missao in missoes:
            if tipo_fase.lower() in missao.get("nome", "").lower():
                missao_removida = missao
                break

        if missao_removida:
            pendentes = len(missoes)

            if pendentes == 3:
                pontos_bonus = 50
            elif pendentes == 2:
                pontos_bonus = 100
            elif pendentes == 1:
                pontos_bonus = 150

            updated_data['pontos'] = updated_data.get('pontos', 0) + pontos_bonus

            mongo.db.criancas.update_one(
                {'_id': obj_id},
                {'$pull': {'missoesDiarias': {'nome': missao_removida["nome"]}}}
            )

            missao_concluida_info = {
                'nomeMissao': missao_removida["nome"],
                'descricao': missao_removida.get("descricao", ""),
                'bonus': pontos_bonus,
                'missaoAntesDeConcluir': pendentes
            }

    result = mongo.db.criancas.update_one(
        {'_id': obj_id},
        {'$set': updated_data}
    )

    edit_rankings()

    response = {
        'message': 'Dados atualizados com sucesso' if result.modified_count > 0 or missao_removida else 'Nenhuma alteração realizada',
        'bonus': pontos_bonus,
        'missaoConcluida': missao_concluida_info,
        'medalhasGanhas': medalhas_adicionadas
    }

    return response

def delete_children(id):
    # Buscar usuário no banco
    user_data = mongo.db.criancas.find_one({'_id': id})

    if user_data:
        mongo.db.criancas.deleteMany({'_id': id})
        return {'message': 'Conta excluida com sucesso'}
    else:
        return {'error': 'Erro ao buscar os dados da criança'}
