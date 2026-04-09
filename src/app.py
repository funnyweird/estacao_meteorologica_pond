from flask import Flask, request, jsonify, render_template
import database as db

app = Flask(__name__)

# Inicializa o banco de dados logo que o servidor liga
with app.app_context():
    db.init_db()

# ==========================================
# ROTAS DA INTERFACE WEB (Páginas HTML)
# ==========================================

@app.route('/')
def index():
    """Rota para o Painel Principal (Dashboard)."""
    # Busca as últimas 10 leituras para mostrar na tela inicial
    leituras = db.obter_leituras(limite=10)
    return render_template('index.html', leituras=leituras)

@app.route('/historico')
def historico():
    """Rota para a página de Histórico."""
    leituras = db.obter_leituras(limite=50)
    return render_template('historico.html', leituras=leituras)

# ==========================================
# ROTAS DA API REST (Comunicação com Arduino)
# ==========================================

@app.route('/leituras', methods=['POST'])
def criar():
    """Rota que recebe o JSON do Arduino e salva no banco de dados."""
    dados = request.get_json()
    
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400
        
    # Chama a função que criamos no database.py
    id_novo = db.inserir_leitura(
        dados.get('temperatura'),
        dados.get('umidade'),
        dados.get('pressao')
    )
    
    return jsonify({'id': id_novo, 'status': 'criado'}), 201

@app.route('/leituras', methods=['GET'])
def listar_api():
    """Rota que retorna os dados em formato JSON."""
    leituras = db.obter_leituras(limite=50)
    return jsonify(leituras)

@app.route('/editar/<int:id>')
def editar(id):
    """Rota que exibe a tela HTML de edição pré-preenchida."""
    leitura = db.buscar_leitura(id)
    if not leitura:
        return "Leitura não encontrada", 404
    return render_template('editar.html', leitura=leitura)

@app.route('/leituras/<int:id>', methods=['DELETE'])
def deletar(id):
    """Rota que remove uma leitura do banco."""
    db.deletar_leitura(id)
    return jsonify({'status': 'excluido', 'id': id}), 200

@app.route('/leituras/<int:id>', methods=['PUT'])
def atualizar(id):
    """Rota da API que recebe os novos dados e atualiza o banco de dados."""
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400

    db.atualizar_leitura(id, dados.get('temperatura'), dados.get('umidade'))
    return jsonify({'status': 'atualizado', 'id': id}), 200

# Roda o servidor na porta 5000
if __name__ == '__main__':
    app.run(debug=True, port=5000)