import csv
import write_gsheets


def format_csv(input_filename='temporary_file.csv'):
    TITLE = "Full Name Upload"

    customers_formatted = []

    with open(input_filename) as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            customer = f"{row['customer']} - {row['job_id']}"
            customers_formatted.append(customer)

    # write_gsheets.write_gsheets(title=TITLE, customers=customers_formatted)
    
    # Print formatted csv:
    for cust in customers_formatted:
        print(cust)
    
if __name__ == "__main__":
    format_csv()