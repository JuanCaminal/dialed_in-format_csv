import os
from playwright.sync_api import Playwright, sync_playwright, expect
from yaspin import yaspin
from . import csv_formatter
LOGIN_URL = "https://work.dispatch.me/login"

def run(playwright: Playwright,  user, password, start_date, end_date, filename: str="temporary_file.csv", invisible=True):
    try: 
        browser = playwright.chromium.launch(headless=invisible)
        context = browser.new_context()
        page = context.new_page()
        
        login(page, user, password)
        apply_filters(page, start_date, end_date)
        flag_data_downloaded = download_data(page, filename)
        
        if flag_data_downloaded:
            csv_formatter.format_csv(filename)
    except Exception as e:
        print(f"An error occurred during the scraping process: {e}")
    finally:
        context.close()
        browser.close()

def login(page, user, password):
    try:
        page.goto(LOGIN_URL)
        page.get_by_test_id("Tab-email").click()
        page.get_by_placeholder("Enter your email").click()
        page.get_by_placeholder("Enter your email").fill(user)
        page.get_by_test_id("Button").click()
        page.get_by_placeholder("Enter your password").click()
        page.get_by_placeholder("Enter your password").fill(password)
        page.get_by_role("button", name="Submit").click()
    except Exception as e:
        print(f"Login failed: {e}")
        raise
        
def apply_filters(page, start_date, end_date):
    """ Goes to report section and apply the filters for the dates """
    try:
        page.get_by_text("Reports").click()
        page.get_by_text("Operations").click()
        page.frame_locator("#report-dashboard").get_by_text("Filters (1)").click()
        page.frame_locator("#report-dashboard").locator(".small-radio-button > .icon").first.click()
        page.frame_locator("#report-dashboard").get_by_placeholder("Start Date").click()
        page.frame_locator("#report-dashboard").get_by_placeholder("Start Date").fill(start_date)
        page.frame_locator("#report-dashboard").get_by_placeholder("End Date").click()
        page.frame_locator("#report-dashboard").get_by_placeholder("End Date").fill(end_date)
        page.frame_locator("#report-dashboard").get_by_placeholder("End Date").click()
        page.frame_locator("#report-dashboard").get_by_text("Apply").click()
        page.wait_for_timeout(1500)     # Waits 1.5 seconds for letting the page load
    except Exception as e:
        print(f"Filtering dates failed {e}")
        raise
            
def download_data(page, filename):
    """ Waits until the table is loaded and does the download of the CSV file """
    
    try:
        # Waits for the spinner to be hidden 
        spinner_locator = page.frame_locator("#report-dashboard").locator("div:nth-child(19) .spinner").first
        spinner_locator.wait_for(state="hidden", timeout=90000)
    except Exception as e:
        print(f"Error waiting for spinner to disappear: {e}")
        return False
    
    try:    
        #Hover over the table because the button is previously hidden
        page.frame_locator("#report-dashboard").locator(".cover").first.hover()
        # Message shown where the table is empty
        error_message = page.frame_locator("#report-dashboard").locator("div:nth-child(19) > .error-message")
        
        if error_message.is_visible():
            print("\nThere was no data for the selected dates..")
            return False
        else:
            # Selects the download button
            expand_button = page.frame_locator("#report-dashboard").locator(".expand").first
            expand_button.click()
            with page.expect_download() as download_info:
                page.frame_locator("#report-dashboard").get_by_text("Download Data").dblclick()
            download = download_info.value

            # Saves the file in a tmp folder
            current_directory = os.getcwd()
            tmp_directory = "/tmp"
            try:
                download.save_as(os.path.join(tmp_directory, filename))
                return True
            
            except FileNotFoundError:
                print(f"Directory '{tmp_directory}' not found, and it couldn't be created.")
                return False
            
            except Exception as e:
                print(f"Error saving the file: {e}")
                return False
            
    except Exception as e:
        print(f"Error during data download: {e}")
        raise
        
if __name__ == "__main__":
    with yaspin(text="Downloading csv file...", color="yellow") as spinner:
        try:
            with sync_playwright() as playwright:
                run(playwright, invisible=False)
            spinner.ok("✔️  Download completed!")
        except Exception as e:
            spinner.fail(f"Download failed: {e}")
