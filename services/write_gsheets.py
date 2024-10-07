import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def write_gsheets(title="Full Name Upload", customers=None):
    if not customers:
        customers = []

    file = authorize_gsheets()
    
    workbook = file.open("Juan Dispatch <> QBO Test ")
    sheet = workbook.get_worksheet(1)
    
    previous_customers = sheet.col_values(1)
    start_row = len(previous_customers) + 1
    
    if start_row == 1:
        sheet.update_acell('A1', title)
        start_row += 1

    for i, customer in enumerate(customers, start=start_row):
        sheet.update_cell(i, 1, customer)
            
            
def authorize_gsheets():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]


    current_directory = os.getcwd()

    creds = ServiceAccountCredentials.from_json_keyfile_name(f"{current_directory}\\config\\secret_key.json", scopes=scopes)
    
    return gspread.authorize(creds)
    
if __name__ == "__main__":
    write_gsheets()
    