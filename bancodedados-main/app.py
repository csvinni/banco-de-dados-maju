from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mysqldb import MySQL
from datetime import datetime
from flask_login import LoginManager, login_required, login_user, logout_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPERMEGADIFICIL'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_mytasks'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


conexao = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('index.html')

# Rota de Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])
        cursor = conexao.connection.cursor()
        INSERT = 'INSERT INTO usuarios(email,senha) VALUES (%s, %s)'

        try:
            cursor.execute(INSERT, (email, senha)) 
            conexao.connection.commit()  
        except Exception as e:
            print(f"An error occurred: {e}")  
            conexao.connection.rollback()  
        finally:
            cursor.close()
            return redirect(url_for('login'))
        
    return render_template('register.html')

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.get_by_email(email)

        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('tasks')) 
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', 'error')
            return redirect(url_for('login'))


    return render_template('login.html')

# Rota de Gerenciamento de Tarefas
@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    cursor = conexao.connection.cursor()
    params = [current_user.id]
    query = "SELECT * FROM tarefas WHERE usuario_id = %s"
    
    status_filter = request.args.get('status')
    prioridade_filter = request.args.get('prioridade')
    categoria_filter = request.args.get('categoria')
    titulo_filter = request.args.get('titulo')

    if status_filter:
        query += " AND status = %s"
        params.append(status_filter)
    if prioridade_filter:
        query += " AND prioridade = %s"
        params.append(prioridade_filter)
    if categoria_filter:
        query += " AND categoria = %s"
        params.append(categoria_filter)
    if titulo_filter:
        query += " AND titulo = %s"
        params.append(titulo_filter)



    cursor.execute(query, params)
    tarefas = cursor.fetchall()
    cursor.close()
    
    return render_template('tasks.html', tarefas=tarefas)


@app.route('/criartarefas', methods=['GET', 'POST'])
@login_required
def create():
    cursor = conexao.connection.cursor()
    if request.method == 'POST':
        descricao = request.form['descricao']
        data_limite = request.form['data_limite']
        prioridade = request.form['prioridade']
        categoria = request.form['categoria']
        data_criacao = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("""
            INSERT INTO tarefas (usuario_id, descricao, status, data_criacao, data_limite, prioridade, categoria)
            VALUES (%s, %s, 'Em andamento', %s, %s, %s, %s)
        """, (current_user.id, descricao, data_criacao, data_limite, prioridade, categoria))

        conexao.connection.commit()
        cursor.close()

        return redirect(url_for('tasks'))

    return render_template('create.html')

# Rota para Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    cursor = conexao.connection.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = %s", (id,))
    conexao.connection.commit()
    cursor.close()
    return redirect(url_for('tasks'))

@app.route('/concluida/<int:id>', methods=['POST'])
@login_required
def concluida(id):
    cursor = conexao.connection.cursor()
    cursor.execute("UPDATE tarefas SET status = 'Concluída' WHERE id = %s", (id,))
    conexao.connection.commit()
    cursor.close()
    return redirect(url_for('tasks'))

@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar(id):
    cursor = conexao.connection.cursor()
    cursor.execute('SELECT id, email FROM usuarios WHERE id = %s', (id,))
    user = cursor.fetchone()
    cursor.execute('SELECT id, descricao, data_limite, status FROM tarefas WHERE id = %s', (id,))
    tarefa = cursor.fetchone()
    
    if request.method == 'POST':
        if 'descricao' in request.form:
            descricao = request.form['descricao']
            data_limite = request.form['data_limite']
            status = request.form['status']
            prioridade = request.form["prioridade"]
            categoria = request.form["categoria"]

            
            cursor.execute('UPDATE tarefas SET descricao = %s, data_limite = %s, status = %s, prioridade = %s, categoria = %s WHERE id = %s', 
               (descricao, data_limite, status, prioridade, categoria, id))
            conexao.connection.commit()
            cursor.close()
            
            return redirect(url_for('tasks'))

    return render_template('editar.html', tarefa=tarefa, user=user)