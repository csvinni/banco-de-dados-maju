from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mysql'
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

conexao = MySQL(app)

def banco(banco_dados):
    with app.app_context():
        cursor = conexao.connection.cursor()
        with open(banco_dados, 'r') as file:
            sql = file.read()
            comandos_raw = sql.split(';') 

            commands = [] 
            for comando in comandos_raw:
                comando_limpo = comando.strip() 
                if comando_limpo:
                    commands.append(comando_limpo)

            for command in commands: 
                cursor.execute(command) 
        conexao.connection.commit()
        cursor.close()

if __name__ == "__main__":
    banco('db/database.sql')  
    print("Banco de dados e tabelas inicializados com sucesso!")



