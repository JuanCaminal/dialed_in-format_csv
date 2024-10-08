import datetime
from services.csv_downloader import run
from playwright.sync_api import sync_playwright
from yaspin import yaspin
import json

def main():
    CSV_FILE_NAME = "temporary_file.csv"
    
    try:
        credentials = load_credentials()
        user = credentials["dispatch_username"]
        password = credentials["dispatch_password"]
    except KeyError as e:
        print(f"Missing key in credentials: {e}")
        return
    except FileNotFoundError:
        print(f"Credentials file not found. Ensure the file exists in the config folder.")
        return
    
    dates = {"start_date":"", "end_date":""}
    
    yesterday = get_yesterday()
    
    # dates = set_yesterday_dates(dates, yesterday)
    
    # Variables for testing with and without data
    dates = set_dates_with_data(dates)
    # dates = set_dates_without_data(dates)
    
    start_date = dates["start_date"]
    end_date = dates["end_date"]
    
    try:
        with yaspin(text="Downloading csv file...", color="yellow") as spinner:
            with sync_playwright() as playwright:
                run(playwright, user, password, start_date, end_date, CSV_FILE_NAME)
            spinner.ok("✔️  Download completed!")
    except Exception as e:
        print(f"Error occurred during the CSV download process: {e}")

def get_yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    return today - one_day

# Set the dates from the csv file that will be downloaded to the previous day date
def set_yesterday_dates(dates, yesterday):
    dates["start_date"] = yesterday.strftime("%Y-%m-%d")
    dates["end_date"] = yesterday.strftime("%Y-%m-%d")
    
    return dates

# Set the dates from the csv file that will be downloaded with dates that have data
# (Choose one of them)
def set_dates_with_data(dates):
     # First dates asked for
    dates["start_date"] = "2024-08-01"
    dates["end_date"] = "2024-08-22"
    
    # Second dates asked for
    # dates["start_date"] = "2024-08-23"
    # dates["end_date"] = "2024-08-31"
    
    return dates

# Set the dates from the csv file that will be downloaded with dates that don't have data
def set_dates_without_data(dates):
    
    dates["start_date"] = "2024-09-28"
    dates["end_date"] = "2024-09-28"
    
    return dates

def load_credentials():
    try:
        with open("config/credentials.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Credentials file not found")
    except json.JSONDecodeErro:
        raise ValueError("Invalid JSON format in credentials file")

if __name__ == "__main__":
    main()
