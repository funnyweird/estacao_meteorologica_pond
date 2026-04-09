import sqlite3
import os

# Nome do arquivo do banco de dados
DATABASE = 'dados.db'

def get_db_connection():
    """Cria a conexão com o banco com as configurações de concorrência exigidas."""
    conn = sqlite3.connect(DATABASE, timeout=10)
    # Configurações cruciais para permitir leitura/escrita simultânea do Flask e do Script Serial
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA busy_timeout=5000')  # espera até 5s caso esteja ocupado
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados lendo o arquivo schema.sql."""
    # Descobre o caminho absoluto para o schema.sql
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    with get_db_connection() as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
    print("Banco de dados inicializado com sucesso!")

def inserir_leitura(temperatura, umidade, pressao=None):
    """Salva uma nova leitura vinda do Arduino no banco de dados."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO leituras (temperatura, umidade, pressao) VALUES (?, ?, ?)',
            (temperatura, umidade, pressao)
        )
        conn.commit()
        return cursor.lastrowid

def obter_leituras(limite=10):
    """Busca as últimas leituras para o painel principal."""
    with get_db_connection() as conn:
        leituras = conn.execute(
            'SELECT * FROM leituras ORDER BY timestamp DESC LIMIT ?',
            (limite,)
        ).fetchall()
        # Converte as linhas do banco (sqlite3.Row) para dicionários (JSON)
        return [dict(leitura) for leitura in leituras]

def deletar_leitura(id_leitura):
    """Remove uma leitura específica do banco de dados pelo seu ID."""
    with get_db_connection() as conn:
        conn.execute('DELETE FROM leituras WHERE id = ?', (id_leitura,))
        conn.commit()

def buscar_leitura(id_leitura):
    """Busca uma leitura específica pelo ID para preencher o formulário."""
    with get_db_connection() as conn:
        leitura = conn.execute('SELECT * FROM leituras WHERE id = ?', (id_leitura,)).fetchone()
        return dict(leitura) if leitura else None

def atualizar_leitura(id_leitura, temperatura, umidade):
    """Atualiza os dados de uma leitura existente no banco (UPDATE)."""
    with get_db_connection() as conn:
        conn.execute(
            'UPDATE leituras SET temperatura = ?, umidade = ? WHERE id = ?',
            (temperatura, umidade, id_leitura)
        )
        conn.commit()