"""
Playwright Cheatsheet for Dynamic Web Scraping
==============================================

This cheatsheet provides common patterns for scraping dynamic websites
using Playwright with Python.
"""

import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import time

# Basic setup and navigation
async def basic_navigation():
    """Basic browser setup and navigation with Playwright."""
    async with async_playwright() as p:
        # Launch browser (chromium, firefox, or webkit)
        browser = await p.chromium.launch(headless=True)
        
        # Create a new browser context (like an incognito window)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        # Create a new page
        page = await context.new_page()
        
        # Navigate to URL
        await page.goto("https://www.example.com")
        
        # Get page title
        title = await page.title()
        print(f"Page title: {title}")
        
        # Get current URL
        url = page.url
        print(f"Current URL: {url}")
        
        # Navigate back and forward
        await page.go_back()
        await page.go_forward()
        
        # Reload the page
        await page.reload()
        
        # Close everything
        await context.close()
        await browser.close()

# Finding elements
async def finding_elements():
    """Examples of finding elements with Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.example.com")
        
        # Find element by CSS selector (preferred method)
        element = await page.query_selector("#example-id")
        
        # Find all elements matching a selector
        elements = await page.query_selector_all(".example-class")
        
        # Find element by text
        text_element = await page.query_selector("text=Click here")
        
        # Find element by XPath
        xpath_element = await page.query_selector("//div[@id='example-id']")
        
        # Check if element exists
        exists = await page.is_visible("#example-id")
        
        await browser.close()

# Interacting with elements
async def interacting_with_elements():
    """Examples of interacting with elements using Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # visible for demonstration
        page = await browser.new_page()
        await page.goto("https://www.example.com/form")
        
        # Click on an element
        await page.click("#submit-button")
        
        # Fill a form field
        await page.fill("input[name='username']", "example_user")
        
        # Type text (simulates keystrokes)
        await page.type("#search", "search query")
        
        # Get text content
        heading_text = await page.text_content("h1")
        print(f"Heading text: {heading_text}")
        
        # Get attribute value
        href = await page.get_attribute("a.main-link", "href")
        print(f"Link href: {href}")
        
        # Check if element is visible/enabled
        is_visible = await page.is_visible("#terms")
        is_enabled = await page.is_enabled("#terms")
        
        if is_visible and is_enabled:
            await page.check("#terms")  # Check a checkbox
        
        # Select from dropdown
        await page.select_option("select#country", "US")
        
        await browser.close()

# Waiting for elements and events
async def waiting_for_elements():
    """Examples of waiting for elements and events in Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate with wait until option
        await page.goto("https://www.example.com", wait_until="networkidle")
        
        # Wait for selector to be visible
        await page.wait_for_selector("#dynamic-element", state="visible")
        
        # Wait for element to be hidden
        await page.wait_for_selector(".loading-spinner", state="hidden")
        
        # Wait for specific timeout
        await page.wait_for_timeout(1000)  # 1 second
        
        # Wait for navigation to complete
        async with page.expect_navigation():
            await page.click("a.nav-link")
        
        # Wait for network request
        async with page.expect_request("**/api/data") as request_info:
            await page.click("#load-data")
        request = await request_info.value
        
        # Wait for response
        async with page.expect_response("**/api/data") as response_info:
            await page.click("#load-data")
        response = await response_info.value
        json_data = await response.json()
        
        await browser.close()

# Handling JavaScript
async def handling_javascript():
    """Examples of executing and handling JavaScript with Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.example.com")
        
        # Execute JavaScript
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        # Execute JavaScript with arguments
        await page.evaluate("element => element.style.backgroundColor = 'yellow'", 
                           await page.query_selector("#example-id"))
        
        # Get data from JavaScript
        page_title = await page.evaluate("() => document.title")
        
        # Inject JavaScript
        await page.add_script_tag(content="window.myCustomVar = 'Hello World';")
        
        # Get result from JavaScript
        result = await page.evaluate("() => window.myCustomVar")
        print(f"Custom variable: {result}")
        
        await browser.close()

# Handling dialogs (alerts, confirms, prompts)
async def handling_dialogs():
    """Examples of handling JavaScript dialogs with Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Handle dialog before triggering it
        page.on("dialog", lambda dialog: dialog.accept())
        # Or to dismiss: dialog.dismiss()
        # Or to fill prompt: dialog.accept("input text")
        
        await page.goto("https://www.example.com/alerts")
        
        # Trigger alert
        await page.click("#alert-button")
        
        # For a specific dialog, use expect_dialog
        async with page.expect_dialog() as dialog_info:
            await page.click("#confirm-button")
        dialog = await dialog_info.value
        print(f"Dialog message: {dialog.message}")
        await dialog.accept()
        
        await browser.close()

# Taking screenshots
async def taking_screenshots():
    """Examples of taking screenshots with Playwright."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.example.com")
        
        # Screenshot full page
        await page.screenshot(path="screenshot.png", full_page=True)
        
        # Screenshot specific element
        element = await page.query_selector("#example-id")
        await element.screenshot(path="element_screenshot.png")
        
        # Screenshot as bytes
        screenshot_bytes = await page.screenshot()
        
        await browser.close()

# Real-world example: Scraping a job board
async def scrape_job_board(url, num_pages=1):
    """
    Scrape job listings from a dynamic job board using Playwright.
    Returns a pandas DataFrame with job data.
    """
    all_jobs = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        # Add a slight delay to be respectful
        await context.route("**/*", lambda route: asyncio.sleep(0.1).then(lambda _: route.continue_()))
        
        page = await context.new_page()
        
        try:
            for page_num in range(1, num_pages + 1):
                # Navigate to the page
                page_url = f"{url}?page={page_num}"
                await page.goto(page_url, wait_until="networkidle")
                
                # Wait for job listings to load
                await page.wait_for_selector(".job-card", state="visible")
                
                # Extract job data
                job_cards = await page.query_selector_all(".job-card")
                
                for job in job_cards:
                    try:
                        # Extract basic info
                        title = await job.text_content(".job-title")
                        company = await job.text_content(".company-name")
                        location = await job.text_content(".location")
                        
                        # Click to view details (if needed)
                        await job.click()
                        
                        # Wait for details to load
                        await page.wait_for_selector(".job-description", state="visible")
                        
                        # Get description
                        description = await page.text_content(".job-description")
                        
                        all_jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "description": description
                        })
                        
                        # Go back to results (if needed)
                        await page.go_back()
                        
                        # Add delay to be respectful
                        await page.wait_for_timeout(1000)
                        
                    except Exception as e:
                        print(f"Error extracting job data: {e}")
                        continue
                
                print(f"Completed page {page_num}")
                
                # Be respectful with rate limiting
                await page.wait_for_timeout(2000)
        
        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            await browser.close()
    
    # Convert to DataFrame
    return pd.DataFrame(all_jobs)

# Example of running the async functions
def run_example(async_func):
    """Helper function to run async examples."""
    asyncio.run(async_func())

# Example usage
if __name__ == "__main__":
    print("This is a cheatsheet for Playwright. Import the functions to use them.")
    # To run an example:
    # run_example(basic_navigation)
