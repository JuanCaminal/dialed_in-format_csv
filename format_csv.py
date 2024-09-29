import csv
from datetime import datetime, timedelta
import os
import write_gsheets


def format_csv(input_filename='temporary_file.csv'):
    TITLE = "Full Name Upload"

    customers = []
    customers_formatted = []

    with open(input_filename) as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            customers.append({"job_id":row["job_id"], "customer":row["customer"]})

    for customer in customers:
        if customer:
            customer_formatted = customer['customer'] + " - " + customer['job_id']
            customers_formatted.append(customer_formatted)

    write_gsheets.write_gsheets(title=TITLE, customers=customers_formatted)
    
    # for cust in customers_formatted:
    #     print(cust["Full Name Upload"])
    
if __name__ == "__main__":
    format_csv()