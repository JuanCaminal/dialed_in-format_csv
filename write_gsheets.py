import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from faker import Faker



def write_gsheets(title="Full Name Upload", customers=None):
    if not customers:
        customers = []
        # The next lines are for testing with random names
        # fake = Faker('en_US')
        # for _ in range(10):
        #     name = fake.name()
        #     customers.append(name)
            
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    current_directory = os.getcwd()

    creds = ServiceAccountCredentials.from_json_keyfile_name(f"{current_directory}\\data\\secret_key.json", scopes=scopes)

    file = gspread.authorize(creds)
    
    workbook = file.open("Juan Dispatch <> QBO Test ")
    sheet = workbook.get_worksheet(1)
    
    previous_customers = sheet.col_values(1)
    amount_previous_customers = len(previous_customers)
    
    if amount_previous_customers == 0:
        sheet.update_acell('A1', title)
        
        for i, customer in enumerate(customers):
            sheet.update_cell(2 + i + amount_previous_customers, 1, customer)
    else:
        
        for i, customer in enumerate(customers):
            sheet.update_cell(1 + i + amount_previous_customers, 1, customer)
    
if __name__ == "__main__":
    write_gsheets()
    