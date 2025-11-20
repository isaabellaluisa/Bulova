from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
import os
import time

# Configuração de logs
logging.basicConfig(level=logging.INFO)

# --- CONFIGURAÇÃO DO SERVIDOR WEB ---
app = Flask(__name__, static_url_path='', static_folder='.')
CORS(app)

# --- CONFIGURAÇÃO DE UPLOAD ---
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Cria a pasta uploads se não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
def get_db_connection():
    try:
        # Configuração direta e explícita
        conn = mysql.connector.connect(
            host="127.0.0.1",  # Endereço IPv4 forçado
            user="root",       # Usuário padrão
            password="",       # Senha vazia
            database="bulova_db",
            use_pure=True      # CORREÇÃO FUNDAMENTAL: Evita o erro RuntimeError no Windows
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar no MySQL: {err}")
        return None

# --- ROTA DA PÁGINA INICIAL ---
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ==========================================
#                 API - PRODUTOS
# ==========================================

@app.route('/produtos', methods=['GET'])
def get_produtos():
    conn = get_db_connection()
    if not conn: 
        return jsonify({"error": "Não foi possível conectar ao Banco de Dados"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT p.id, p.nome, p.preco, p.imagem_url, p.marca_id, p.descricao, p.material, m.nome as nome_marca 
            FROM produtos p 
            LEFT JOIN marcas m ON p.marca_id = m.id
            ORDER BY p.id DESC
        """
        cursor.execute(query)
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected(): conn.close()

@app.route('/produtos', methods=['POST'])
def create_produto():
    conn = get_db_connection()
    if not conn: 
        return jsonify({"error": "Não foi possível conectar ao Banco de Dados"}), 500
    
    try:
        cursor = conn.cursor()
        
        # Dados do formulário
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        marca_id = request.form.get('marca_id')
        descricao = request.form.get('descricao')
        material = request.form.get('material')
        img_path = ""

        # Upload de Imagem
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{int(time.time())}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img_path = f"uploads/{filename}"
        elif request.form.get('imagem_url'):
             img_path = request.form.get('imagem_url')

        # Se não tiver imagem, coloca um placeholder
        if not img_path:
            img_path = "https://via.placeholder.com/300x400?text=Sem+Imagem"

        query = "INSERT INTO produtos (nome, preco, imagem_url, marca_id, descricao, material) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (nome, preco, img_path, marca_id, descricao, material)
        
        cursor.execute(query, values)
        conn.commit()
        
        return jsonify({"message": "Produto criado com sucesso!", "id": cursor.lastrowid}), 201
    except Exception as err:
        print(f"Erro ao criar produto: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if conn.is_connected(): conn.close()

@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    conn = get_db_connection()
    if not conn: 
        return jsonify({"error": "Não foi possível conectar ao Banco de Dados"}), 500
    
    try:
        cursor = conn.cursor()
        
        nome = request.form.get('nome')
        preco = request.form.get('preco')
        marca_id = request.form.get('marca_id')
        descricao = request.form.get('descricao')
        material = request.form.get('material')
        
        # Verifica se veio nova imagem
        img_path = None
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{int(time.time())}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img_path = f"uploads/{filename}"
        
        # Constroi query dinamicamente baseada na presença da imagem
        if img_path:
            query = """
                UPDATE produtos 
                SET nome=%s, preco=%s, marca_id=%s, descricao=%s, material=%s, imagem_url=%s 
                WHERE id=%s
            """
            values = (nome, preco, marca_id, descricao, material, img_path, id)
        else:
            query = """
                UPDATE produtos 
                SET nome=%s, preco=%s, marca_id=%s, descricao=%s, material=%s 
                WHERE id=%s
            """
            values = (nome, preco, marca_id, descricao, material, id)

        cursor.execute(query, values)
        conn.commit()
        
        return jsonify({"message": "Produto atualizado com sucesso!"}), 200
    except Exception as err:
        print(f"Erro ao atualizar produto: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if conn.is_connected(): conn.close()

@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Erro BD"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"message": "Deletado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected(): conn.close()

# ==========================================
#                 API - MARCAS
# ==========================================

@app.route('/marcas', methods=['GET'])
def get_marcas():
    conn = get_db_connection()
    if not conn: 
        return jsonify({"error": "Não foi possível conectar ao Banco de Dados"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM marcas ORDER BY nome ASC")
        return jsonify(cursor.fetchall())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected(): conn.close()

@app.route('/marcas', methods=['POST'])
def create_marca():
    conn = get_db_connection()
    if not conn: 
        return jsonify({"error": "Não foi possível conectar ao Banco de Dados"}), 500
        
    try:
        cursor = conn.cursor()
        
        nome = request.form.get('nome')
        if not nome and request.is_json:
            nome = request.json.get('nome')
            
        img_path = ""
        
        # Upload de Imagem da Marca
        if 'imagem' in request.files:
            file = request.files['imagem']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"brand_{int(time.time())}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                img_path = f"uploads/{filename}"
        elif request.is_json and request.json.get('imagem_url'):
             img_path = request.json.get('imagem_url')

        query = "INSERT INTO marcas (nome, imagem_url) VALUES (%s, %s)"
        values = (nome, img_path)
        
        cursor.execute(query, values)
        conn.commit()
        
        return jsonify({"message": "Marca criada!", "id": cursor.lastrowid}), 201
    except Exception as err:
        print(f"Erro ao criar marca: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if conn.is_connected(): conn.close()

if __name__ == '__main__':
    print("--- SERVIDOR BULOVA INICIADO ---")
    print("Acesse: http://localhost:3000")
    app.run(port=3000, debug=True)