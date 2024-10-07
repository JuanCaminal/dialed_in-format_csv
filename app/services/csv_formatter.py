import csv
import os

from . import gsheets_writer
# from app.services import gsheets_writer



def format_csv(input_filename='temporary_file.csv'):
    TITLE = "Full Name Upload"

    customers_formatted = []
    project_root = get_project_root()
    
    csv_file_path = os.path.join(project_root, "tmp", "temporary_file.csv")
    
    with open(csv_file_path) as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            customer = f"{row['customer']} - {row['job_id']}"
            customers_formatted.append(customer)

    # write_gsheets.write_gsheets(title=TITLE, customers=customers_formatted)
    gsheets_writer.write_gsheets(title=TITLE, customers=customers_formatted)
    
    # Print formatted csv:
    # for cust in customers_formatted:
    #     print(cust)
    
def get_project_root():
    """
    Gets root directory
    """
    current_dir = os.path.dirname(__file__)
    parent_dir = os.path.join(current_dir, os.pardir, os.pardir)
    project_root = os.path.abspath(parent_dir)
    return project_root    

if __name__ == "__main__":
    format_csv()