import os
from playwright.sync_api import Playwright, sync_playwright, expect
from yaspin import yaspin

import format_csv

LOGIN_URL = "https://work.dispatch.me/login"

def run(playwright: Playwright,  user, password, start_date, end_date, filename: str="temporary_file.csv", invisible=True):
    browser = playwright.chromium.launch(headless=invisible)
    context = browser.new_context()
    page = context.new_page()
    
    login(page, user, password)
    apply_filters(page, start_date, end_date)
    flag_data_downloaded = download_data(page, filename)
    
    if flag_data_downloaded:
        format_csv.format_csv(filename)
    
    context.close()
    browser.close()

def login(page, user, password):
    page.goto(LOGIN_URL)
    page.get_by_test_id("Tab-email").click()
    page.get_by_placeholder("Enter your email").click()
    page.get_by_placeholder("Enter your email").fill(user)
    page.get_by_test_id("Button").click()
    page.get_by_placeholder("Enter your password").click()
    page.get_by_placeholder("Enter your password").fill(password)
    page.get_by_role("button", name="Submit").click()
    
def apply_filters(page, start_date, end_date):
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
    
def download_data(page, filename):
    spinner_locator = page.frame_locator("#report-dashboard").locator("div:nth-child(19) .spinner").first
    spinner_locator.wait_for(state="hidden", timeout=90000)
    
    page.frame_locator("#report-dashboard").locator(".cover").first.hover()
    error_message = page.frame_locator("#report-dashboard").locator("div:nth-child(19) > .error-message")
    
    if error_message.is_visible():
        print("\nThere was no data for the selected dates..")
        return False
    else:
        expand_button = page.frame_locator("#report-dashboard").locator(".expand").first
        expand_button.click()
        with page.expect_download() as download_info:
            page.frame_locator("#report-dashboard").get_by_text("Download Data").dblclick()
        download = download_info.value
    
        current_directory = os.getcwd()
        print(current_directory)
        download.save_as(current_directory + f"\\{filename}")
        
        return True
    
if __name__ == "__main__":
    with yaspin(text="Downloading csv file...", color="yellow") as spinner:
        with sync_playwright() as playwright:
            run(playwright, invisible=False)
        spinner.ok("✔️  Download completed!")
