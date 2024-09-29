import datetime
from download import run
from playwright.sync_api import sync_playwright
from yaspin import yaspin
import format_csv

def main():
    CSV_FILE_NAME = "temporary_file.csv"
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day

    # Cambia las fechas según lo necesites
    # start_date = yesterday.strftime("%Y-%m-%d")
    # end_date = yesterday.strftime("%Y-%m-%d")
    
    start_date = "2024-09-15"
    end_date = "2024-09-28"

    try:
        # with yaspin(text="Downloading csv file...", color="yellow") as spinner:
        #     with sync_playwright() as playwright:
        #         run(playwright, start_date, end_date, CSV_FILE_NAME, invisible=False)
        #     spinner.ok("✔️  Download completed!")
        
        format_csv.format_csv(CSV_FILE_NAME)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
