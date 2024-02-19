import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import json
import os

class CadastroTonerApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.serial_label = Label(text="Serial do Toner:")
        self.serial_entry = TextInput(multiline=False, height=30)

        self.modelo_label = Label(text="Modelo:")
        self.modelo_entry = TextInput(multiline=False, height=30)

        self.tipo_label = Label(text="Tipo:")
        self.tipo_entry = TextInput(multiline=False, height=30)

        self.folder_label = Label(text="Escolha a pasta de destino:")
        self.folder_button = Button(text="Escolher Pasta", on_press=self.choose_folder)

        self.cadastrar_button = Button(text="Cadastrar", on_press=self.cadastrar_toner)

        self.root.add_widget(self.serial_label)
        self.root.add_widget(self.serial_entry)
        self.root.add_widget(self.modelo_label)
        self.root.add_widget(self.modelo_entry)
        self.root.add_widget(self.tipo_label)
        self.root.add_widget(self.tipo_entry)
        self.root.add_widget(self.folder_label)
        self.root.add_widget(self.folder_button)
        self.root.add_widget(self.cadastrar_button)

        return self.root

    def choose_folder(self, instance):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_label.text = f"Escolha a pasta de destino: {folder_path}"

    def cadastrar_toner(self, instance):
        serial = self.serial_entry.text
        modelo = self.modelo_entry.text
        tipo = self.tipo_entry.text
        folder_path = self.folder_label.text.replace("Escolha a pasta de destino: ", "")

        if serial and modelo and tipo and folder_path:
            self.show_popup("Cadastro realizado", "Toner cadastrado com sucesso!")

            # Salvar as informações em um arquivo JSON
            data = {"serial": serial, "modelo": modelo, "tipo": tipo}
            json_data = json.dumps(data, indent=2)

            json_filename = f"{serial}_{modelo}_{tipo}.json"
            json_path = os.path.join(folder_path, json_filename)

            with open(json_path, 'w') as json_file:
                json_file.write(json_data)

            # Limpar os campos após o cadastro
            self.serial_entry.text = ""
            self.modelo_entry.text = ""
            self.tipo_entry.text = ""
            self.folder_label.text = "Escolha a pasta de destino:"
        else:
            self.show_popup("Erro", "Preencha todos os campos e escolha a pasta de destino!")

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == "__main__":
    CadastroTonerApp().run()
