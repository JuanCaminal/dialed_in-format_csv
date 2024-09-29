import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def write_gsheets(title="Full Name Upload", customers=None):
    if customers is None:
        customers = []

    try:
        # Configurar credenciales y acceso a Google Sheets
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        current_directory = os.getcwd()

        creds = ServiceAccountCredentials.from_json_keyfile_name(f"{current_directory}\\data\\secret_key.json", scopes=scopes)

        file = gspread.authorize(creds)
    
        workbook = file.open("Juan Dispatch <> QBO Test")
        sheet = workbook.get_worksheet(1)
    
        previous_customers = sheet.col_values(1)
        amount_previous_customers = len(previous_customers)

        # Insertar título y los nuevos clientes en la columna A
        if amount_previous_customers == 0:
            sheet.update_acell('A1', title)
        for i, customer in enumerate(customers):
            sheet.update_cell(2 + i + amount_previous_customers, 1, customer)
    except Exception as e:
        print(f"Error updating Google Sheets: {str(e)}")

if __name__ == "__main__":
    write_gsheets()
