import csv
import os

from . import gsheets_writer
# from app.services import gsheets_writer



def format_csv(input_filename='temporary_file.csv'):
    TITLE = "Full Name Upload"

    customers_formatted = []
    csv_file_path = os.path.join("/tmp", "temporary_file.csv")
    
    try:
        with open(csv_file_path) as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                customer = f"{row['customer']} - {row['job_id']}"
                customers_formatted.append(customer)

        gsheets_writer.write_gsheets(title=TITLE, customers=customers_formatted)
    except FileNotFoundError:
        print(f"CSV file not found at path: {csv_file_path}")
    except KeyError as e:
        print(f"Missing key in CSV data: {e}")
    except Exception as e:
        print(f"Error occurred during CSV formatting: {e}")
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