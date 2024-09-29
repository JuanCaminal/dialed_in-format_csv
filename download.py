import os
import re
from playwright.sync_api import Playwright, sync_playwright, expect
from yaspin import yaspin


def run(playwright: Playwright,  start_date, end_date, filename: str="temporary_file.csv", invisible=True) -> None:
    browser = playwright.chromium.launch(headless=invisible)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://work.dispatch.me/login")
    page.get_by_test_id("Tab-email").click()
    page.get_by_placeholder("Enter your email").click()
    page.get_by_placeholder("Enter your email").fill("hmcparker@diblogins.com")
    page.get_by_test_id("Button").click()
    page.get_by_placeholder("Enter your password").click()
    page.get_by_placeholder("Enter your password").fill("eds!WH7#82eLxKmF")
    page.get_by_role("button", name="Submit").click()
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
    page.wait_for_timeout(10000)  # Waits 10 seconds
    
    page.frame_locator("#report-dashboard").locator(".cover").first.hover()
    expand_button = page.frame_locator("#report-dashboard").locator(".expand").first
    expand_button.click()
    with page.expect_download() as download_info:
        page.frame_locator("#report-dashboard").get_by_text("Download Data").dblclick()
    download = download_info.value
    
    current_directory = os.getcwd()
    
    download.save_as(current_directory + f"\\{filename}")
    # ---------------------
    context.close()
    browser.close()

if __name__ == "__main__":
    with yaspin(text="Downloading csv file...", color="yellow") as spinner:
        with sync_playwright() as playwright:
            run(playwright, invisible=False)
        spinner.ok("✔️  Download completed!")
