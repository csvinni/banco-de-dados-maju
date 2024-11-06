from flask import Flask
from flask_login import UserMixin, LoginManager
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'your_secret_key'  


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_mytasks'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
login_manager = LoginManager(app)


def obter_conexao():
    return mysql.connection.cursor()


class User(UserMixin):
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha
        self.id = None

    @classmethod
    def get(cls, id):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE id=%s'  
        conexao.execute(SELECT, (id,))
        dados = conexao.fetchone()
        if dados:
            user = cls(dados['email'], dados['senha'])
            user.id = dados['id']
            return user
        return None

    @classmethod
    def get_by_email(cls, email):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE email=%s'  
        conexao.execute(SELECT, (email,))
        dados = conexao.fetchone()
        if dados:
            user = cls(dados['email'], dados['senha'])
            user.id = dados['id']
            return user
        return None


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
















































'''from flask_login import UserMixin
import sqlite3

BANCO = 'database.db'
def obter_conexao():
    conn = sqlite3.connect(BANCO)
    conn.row_factory = sqlite3.Row
    return conn

# classe python - Modelo (acessa o banco)
class User(UserMixin):
    id : str
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha
    
    @classmethod
    def get(cls, id):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE id=?'
        dados = conexao.execute(SELECT, (id,)).fetchone()
        user = User(dados['email'], dados['senha'])
        user.id = dados['id']
        return user

    @classmethod
    def get_by_email(cls, email):
        conexao = obter_conexao()
        SELECT = 'SELECT * FROM usuarios WHERE email=?'
        dados = conexao.execute(SELECT, (email,)).fetchone()
        if dados:    
            user = User(dados['email'], dados['senha'])
            user.id = dados['id']
            return user
        return None'''