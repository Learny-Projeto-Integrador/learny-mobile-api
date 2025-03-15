from flask import request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash, generate_password_hash

def init_app(app):

    app.config['MONGO_URI'] = 'mongodb://localhost:27017/learny-bd'

    mongo = PyMongo(app)

    @app.route('/')
    def home():
        return 'Rota Inicial'
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()

        if not data or not data.get('user') or not data.get('password'):
            return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400

        user = data['user']
        password = data['password']

        # Buscar usuário no banco
        user_data = mongo.db.pais.find_one({'usuario': user})

        if user_data:
            if check_password_hash(user_data['senha'], password):
                return jsonify({'message': 'Login realizado com sucesso!'})
            else:
                return jsonify({'error': 'Senha Inválida'}), 401
        else:
            return jsonify({'error': 'Usuário ou senha inválidos'}), 401
        
    @app.route('/pais', methods=['POST'])
    def pais():
        data = request.get_json()

        if not data or not data.get('user') or not data.get('password') or not data.get('email'):
            return jsonify({'error': 'Preencha todos os campos'}), 400

        image = data['image']
        user = data['user']
        password = generate_password_hash(data['password'])
        email = data['email']
        dataNasc = data['dataNasc']

        dados = {
            'foto': image,
            'usuario': user, 
            'senha': password, 
            'email': email, 
            'dataNasc': dataNasc,
        }

        # Buscar usuário no banco
        user_data = mongo.db.pais.find_one({'usuario': user})

        if user_data:
            return jsonify({'error': 'Usuário já existente'}), 401
        else:
            user_data = mongo.db.pais.insert_one(dados)
            return jsonify({'message': 'Usuário cadastrado com sucesso!'})

        