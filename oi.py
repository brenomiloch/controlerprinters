from flask import Flask, render_template, request
import sqlite3
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados local SQLite
app.config['LOCAL_DB_NAME'] = 'local_database.db'

# Configurações do banco de dados remoto MySQL
app.config['REMOTE_DB_HOST'] = '62.72.62.1'
app.config['REMOTE_DB_USER'] = 'u749227288_app'
app.config['REMOTE_DB_PASSWORD'] = 'Mogiforte@1'
app.config['REMOTE_DB_DATABASE'] = 'u749227288_inventario'

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        serial = request.form['serial']
        modelo = request.form['modelo']
        cor = request.form['cor']

        # Salva localmente
        save_local_db(serial, modelo, cor)

        # Salva remotamente
        save_remote_db(serial, modelo, cor)

    return render_template('index.html')

# Inicialização do banco de dados local
def init_local_db():
    conn_local = sqlite3.connect(app.config['LOCAL_DB_NAME'])
    cursor_local = conn_local.cursor()

    cursor_local.execute("""
        CREATE TABLE IF NOT EXISTS toner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial TEXT NOT NULL,
            modelo TEXT NOT NULL,
            cor TEXT NOT NULL
        )
    """)

    conn_local.commit()
    conn_local.close()

# Salvar no banco de dados local
def save_local_db(serial, modelo, cor):
    conn_local = sqlite3.connect(app.config['LOCAL_DB_NAME'])
    cursor_local = conn_local.cursor()

    cursor_local.execute("INSERT INTO toner (serial, modelo, cor) VALUES (?, ?, ?)",
                         (serial, modelo, cor))

    conn_local.commit()
    conn_local.close()

# Salvar no banco de dados remoto
def save_remote_db(serial, modelo, cor):
    conn_remote = mysql.connector.connect(host=app.config['REMOTE_DB_HOST'],
                                          user=app.config['REMOTE_DB_USER'],
                                          password=app.config['REMOTE_DB_PASSWORD'],
                                          database=app.config['REMOTE_DB_DATABASE'])
    cursor_remote = conn_remote.cursor()

    cursor_remote.execute("INSERT INTO toner (serial, modelo, cor) VALUES (%s, %s, %s)",
                          (serial, modelo, cor))

    conn_remote.commit()
    conn_remote.close()

if __name__ == '__main__':
    init_local_db()
    app.run(debug=True)
