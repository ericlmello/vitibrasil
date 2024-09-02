#jwt

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_aqui'
jwt = JWTManager(app)

# Dados de usuário e senha (em produção, use um banco de dados)
users = {
    'admin': generate_password_hash('senha123', method='sha256')
}

# Rota para login e obtenção do token JWT
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()  # Corrigido para obter JSON
        username = data.get('username', None)
        password = data.get('password', None)

        # Verificação de usuário e senha
        if username not in users or not check_password_hash(users[username], password):
            return jsonify({"msg": "Bad username or password"}), 401

        # Cria um token de acesso
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    except Exception as e:
        return jsonify({"msg": str(e)}), 400

# Rota protegida por JWT
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"msg": "Access granted"})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)





#curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "senha123"}'
#poatmanÇ {
#    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNTMwMjYwNiwianRpIjoiZjkxNTExNzMtZWEwMS00MTJmLWE3M2EtYTlkYTAyNmY1MTU3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzI1MzAyNjA2LCJjc3JmIjoiNWRjM2U4MDktOWQ1NS00NmY2LWE4YTUtMzczM2ZhMjcwYjMxIiwiZXhwIjoxNzI1MzAzNTA2fQ.pHHUht6CwIv2-89pVnZ9YsSONDbJjgyIyPPFMwgYWYI"
#}

#
