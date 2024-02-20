from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import sqlite3
import mysql.connector

class TonerApp(App):
    def build(self):
        return TonerLayout()

class TonerLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(TonerLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        # Adicione widgets aqui
        self.add_widget(Label(text='Serial:'))
        self.ids.serial_input = TextInput(multiline=False)
        self.add_widget(self.ids.serial_input)

        self.add_widget(Label(text='Modelo:'))
        self.ids.modelo_input = TextInput(multiline=False)
        self.add_widget(self.ids.modelo_input)

        self.add_widget(Label(text='Cor:'))
        self.ids.cor_input = TextInput(multiline=False)
        self.add_widget(self.ids.cor_input)

        submit_button = Button(text='Submit', on_press=self.on_submit)
        self.add_widget(submit_button)

        # Inicializar o banco de dados local
        self.init_local_db()

    def init_local_db(self):
        # Conectar ao banco de dados SQLite local
        conn_local = sqlite3.connect('local_database.db')
        cursor_local = conn_local.cursor()

        # Criar a tabela 'toner' se não existir
        cursor_local.execute("""
            CREATE TABLE IF NOT EXISTS toner (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial TEXT NOT NULL,
                modelo TEXT NOT NULL,
                cor TEXT NOT NULL
            )
        """)

        # Commit e fechar conexão
        conn_local.commit()
        conn_local.close()

    def save_local_db(self, serial, modelo, cor):
        # Conectar ao banco de dados SQLite local
        conn_local = sqlite3.connect('local_database.db')
        cursor_local = conn_local.cursor()

        # Inserir dados na tabela 'toner'
        cursor_local.execute("INSERT INTO toner (serial, modelo, cor) VALUES (?, ?, ?)",
                             (serial, modelo, cor))

        # Commit e fechar conexão
        conn_local.commit()
        conn_local.close()

    def save_remote_db(self, serial, modelo, cor):
        # Conectar ao banco de dados MySQL remoto
        conn_remote = mysql.connector.connect(host='62.72.62.1', user='u749227288_app',
                                              password='Mogiforte@1', database='u749227288_inventario')
        cursor_remote = conn_remote.cursor()

        # Inserir dados na tabela 'toner'
        cursor_remote.execute("INSERT INTO toner (serial, modelo, cor) VALUES (%s, %s, %s)",
                              (serial, modelo, cor))

        # Commit e fechar conexão
        conn_remote.commit()
        conn_remote.close()

    def on_submit(self, instance):
        # Obtém dados do QR Code e outros inputs
        serial = self.ids.serial_input.text
        modelo = self.ids.modelo_input.text
        cor = self.ids.cor_input.text

        # Salva localmente
        self.save_local_db(serial, modelo, cor)

        # Salva remotamente
        self.save_remote_db(serial, modelo, cor)

if __name__ == '__main__':
    TonerApp().run()
