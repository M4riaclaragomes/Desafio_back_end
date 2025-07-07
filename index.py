from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)

def init_db():
    with sqlite3.connect('tasks.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL,
            due_date TEXT
        )''')
        conn.commit()

def validate_date(date_str):
    if not date_str:
        return True
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_status(status):
    return status in ['pendente', 'realizando', 'concluída']

@app.route('/tarefas', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('titulo')
    description = data.get('descricao')
    status = data.get('status')
    due_date = data.get('data_vencimento')

    if not title or not status:
        return jsonify({'error': 'Título e status são obrigatórios'}), 400
    
    if not validate_status(status):
        return jsonify({'error': 'Status inválido'}), 400
    
    if due_date and not validate_date(due_date):
        return jsonify({'error': 'Data de vencimento inválida'}), 400

    try:
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO tasks (title, description, status, due_date)
                            VALUES (?, ?, ?, ?)''', (title, description, status, due_date))
            conn.commit()
            task_id = cursor.lastrowid
            
            return jsonify({
                'id': task_id,
                'titulo': title,
                'descricao': description,
                'status': status,
                'data_vencimento': due_date
            }), 201
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor'}), 500

@app.route('/tarefas', methods=['GET'])
def list_tasks():
    status = request.args.get('status')
    
    try:
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            if status and validate_status(status):
                cursor.execute('SELECT * FROM tasks WHERE status = ?', (status,))
            else:
                cursor.execute('SELECT * FROM tasks')
                
            tasks = [{
                'id': row[0],
                'titulo': row[1],
                'descricao': row[2],
                'status': row[3],
                'data_vencimento': row[4]
            } for row in cursor.fetchall()]
            
            return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor'}), 500

@app.route('/tarefas/<int:id>', methods=['GET'])
def get_task(id):
    try:
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
            task = cursor.fetchone()
            
            if not task:
                return jsonify({'error': 'Tarefa não encontrada'}), 404
                
            return jsonify({
                'id': task[0],
                'titulo': task[1],
                'descricao': task[2],
                'status': task[3],
                'data_vencimento': task[4]
            }), 200
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor'}), 500

@app.route('/tarefas/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    title = data.get('titulo')
    description = data.get('descricao')
    status = data.get('status')
    due_date = data.get('data_vencimento')

    if not title or not status:
        return jsonify({'error': 'Título e status são obrigatórios'}), 400
    
    if not validate_status(status):
        return jsonify({'error': 'Status inválido'}), 400
    
    if due_date and not validate_date(due_date):
        return jsonify({'error': 'Data de vencimento inválida'}), 400

    try:
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Tarefa não encontrada'}), 404
                
            cursor.execute('''UPDATE tasks 
                            SET title = ?, description = ?, status = ?, due_date = ?
                            WHERE id = ?''', 
                          (title, description, status, due_date, id))
            conn.commit()
            
            return jsonify({
                'id': id,
                'titulo': title,
                'descricao': description,
                'status': status,
                'data_vencimento': due_date
            }), 200
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor'}), 500

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Tarefa não encontrada'}), 404
                
            cursor.execute('DELETE FROM tasks WHERE id = ?', (id,))
            conn.commit()
            
            return jsonify({'message': 'Tarefa excluída com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': 'Erro interno no servidor'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)