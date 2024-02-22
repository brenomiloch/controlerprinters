import os.path
import mysql.connector
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Se modificar esses escopos, exclua o arquivo token.json.
# Permissão de escopos, no caso somente leitura.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# ID e intervalo de uma planilha de exemplo.
SAMPLE_SPREADSHEET_ID = "17AsV218oIOSvnaUwTybHW7Nesgp-lYk9JDSIcvQg9KI"
SAMPLE_RANGE_NAME = "toner!A1:D"

# Configuração do banco de dados
DB_HOST = "192.92.1.3"
DB_USER = "root"
DB_PASSWORD = "@Gpadrao#3309#"
DB_DATABASE = "db_inventario"

# Títulos das colunas a serem verificados na primeira linha
EXPECTED_COLUMN_TITLES = [
    "serial", "modelo", "cor","__id" 
]

def connect_to_database():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

def check_data_existence(cursor, values):
    query = "SELECT COUNT(*) FROM toner WHERE serial = %s AND modelo = %s AND cor = %s AND __id = %s"
    cursor.execute(query, values)
    return cursor.fetchone()[0] > 0

def insert_into_database(cursor, values):
    if not check_data_existence(cursor, values):
        query = "INSERT INTO toner (serial,modelo,cor,__id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, values)

def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credenciais.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values or len(values) < 2:
            print("Linhas em Brancos!")
            return

        # Verifica se a primeira linha contém os títulos esperados
        if values[0] == EXPECTED_COLUMN_TITLES:
            # Pula a primeira linha
            values = values[1:]

        # Restante do código permanece o mesmo

        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()

        # Iterate through the rows and insert into the database
        for row in values:
            insert_into_database(cursor, tuple(row))

        # Commit and close the database connection
        connection.commit()
        cursor.close()
        connection.close()

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()
