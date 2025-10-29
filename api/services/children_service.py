from api import mongo
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import database
from bson import ObjectId, errors
from pymongo import DESCENDING
from datetime import datetime

def get_child_by_id(id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    crianca = mongo.db.criancas.find_one({'_id': child_oid})
    if crianca:
        crianca = mongo_to_dict(crianca)
        return crianca, 200
    else:
        return {"error": "Nenhum filho selecionado"}, 404
    
def edit_child(id, new_data):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    result = mongo.db.criancas.update_one(
        {'_id': child_oid},
        {'$set': new_data}
    )

    if result.modified_count > 0:
        return {'message': 'Dados alterados com sucesso'}, 200
    else:
        return {'error': 'Erro ao alterar os dados'}, 500
    
def get_ranking():
    criancas = mongo.db.criancas.find().sort("pontos", DESCENDING)

    if not criancas:
        return {'error': 'Dados das crianças não encontrados'}, 404

    ranking = []
    for c in criancas:
        ranking.append({
            "id": str(c["_id"]),
            "foto": c.get("foto", ""),
            "nome": c.get("nome", ""),
            "pontos": c.get("pontos", 0)
        })

    return ranking
    
def edit_rankings():
    criancas = list(mongo.db.criancas.find().sort('pontos', -1))

    for index, crianca in enumerate(criancas):
        mongo.db.criancas.update_one(
            {'_id': crianca['_id']},
            {'$set': {'rankingAtual': index + 1}}
        )
   
def edit_children_score(id, new_data, tipo_fase=None):
    obj_id = convert_id(id)
    if not  obj_id:
        return {'error': 'ID inválido'}, 400

    existing_data = mongo.db.criancas.find_one({'_id': obj_id})
    if not existing_data:
        return {'error': 'Criança não encontrada'}, 404

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
    fase_sequencia = ['connect', 'memory', 'feeling', 'boss']

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
                    if tipo_fase == "boss":
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

                update_fields = {'$push': {'medalhas': medalha_com_data}}

                # Verifica se a criança ainda não possui uma medalha selecionada
                if existing_data.get("medalhaSelecionada") == {}:
                    update_fields['$set'] = {'medalhaSelecionada': medalha_com_data}

                mongo.db.criancas.update_one(
                    {'_id': obj_id},
                    update_fields
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

    return response, 200

def convert_id(id_str):
    try:
        return ObjectId(id_str)
    except Exception:
        return None
    
def mongo_to_dict(doc):
    if isinstance(doc, list):
        return [mongo_to_dict(item) for item in doc]
    elif isinstance(doc, dict):
        new_doc = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                new_doc[key] = str(value)
            elif isinstance(value, (dict, list)):
                new_doc[key] = mongo_to_dict(value)
            else:
                new_doc[key] = value
        return new_doc
    else:
        return doc
