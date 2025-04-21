"""
Selenium Cheatsheet for Dynamic Web Scraping
=============================================

This beginner-friendly cheatsheet provides common patterns for scraping dynamic websites
using Selenium WebDriver with Python.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd

# Setup Chrome WebDriver
def setup_driver(headless=True):
    """Set up and return a Chrome WebDriver instance.
    
    Args:
        headless (bool): If True, browser will run in background without UI
    
    Returns:
        webdriver.Chrome: A configured Chrome WebDriver instance
    
    Example:
        driver = setup_driver(headless=False)  # Show browser window
        driver.get("https://www.google.com")
        driver.quit()
    """
    # Create Chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")  # Required for some environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Required for some environments
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size
    
    # Create a Service object
    service = Service()
    
    # Create the driver with the service and options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Basic navigation
def basic_navigation_example():
    """Example of basic browser navigation with Selenium."""
    # Create a driver (browser)
    driver = setup_driver(headless=False)  # Set to False to see the browser
    
    try:
        # Navigate to a URL
        driver.get("https://www.google.com")
        print("Navigated to Google")
        
        # Get the page title
        title = driver.title
        print(f"Page title: {title}")
        
        # Get the current URL
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        # Find the search box and type something
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium WebDriver Python")
        
        # Wait a moment to see what we typed
        time.sleep(2)
        
        # Submit the form
        search_box.submit()
        print("Submitted search")
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        # Get the search results
        results = driver.find_elements(By.CSS_SELECTOR, ".g")
        print(f"Found {len(results)} search results")
        
        # Navigate back
        driver.back()
        print("Navigated back")
        
        # Navigate forward
        driver.forward()
        print("Navigated forward")
        
        # Refresh the page
        driver.refresh()
        print("Refreshed the page")
        
        # Wait a moment to see the results
        time.sleep(2)
    
    finally:
        # Always close the browser when done
        driver.quit()
        print("Browser closed")

# Finding elements - different ways to locate elements on a page
def finding_elements_example():
    """Example of finding elements on a webpage."""
    driver = setup_driver()
    
    try:
        # Go to a webpage
        driver.get("https://www.wikipedia.org")
        
        # 1. Find element by ID
        # This finds the search input box on Wikipedia's homepage
        search_box = driver.find_element(By.ID, "searchInput")
        print("Found search box by ID")
        
        # 2. Find element by NAME
        # This finds the same search box using its name attribute
        search_box_by_name = driver.find_element(By.NAME, "search")
        print("Found search box by NAME")
        
        # 3. Find element by CLASS_NAME
        # This finds the central logo area
        central_featured = driver.find_element(By.CLASS_NAME, "central-featured")
        print("Found central featured area by CLASS_NAME")
        
        # 4. Find element by CSS_SELECTOR
        # This finds the English Wikipedia link
        english_link = driver.find_element(By.CSS_SELECTOR, ".central-featured-lang[lang='en']")
        print("Found English link by CSS_SELECTOR")
        
        # 5. Find element by XPATH
        # This finds the same English link using XPath
        english_link_xpath = driver.find_element(By.XPATH, "//div[@lang='en']")
        print("Found English link by XPATH")
        
        # 6. Find element by LINK_TEXT
        # This finds a link by its exact text
        english_link_text = driver.find_element(By.LINK_TEXT, "English")
        print("Found English link by LINK_TEXT")
        
        # 7. Find element by PARTIAL_LINK_TEXT
        # This finds a link by part of its text
        english_partial = driver.find_element(By.PARTIAL_LINK_TEXT, "Engl")
        print("Found English link by PARTIAL_LINK_TEXT")
        
        # 8. Find element by TAG_NAME
        # This finds all input elements
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(inputs)} input elements by TAG_NAME")
        
        # 9. Find multiple elements
        # This finds all language links
        languages = driver.find_elements(By.CSS_SELECTOR, ".central-featured-lang")
        print(f"Found {len(languages)} language links")
        
        # Print the text of each language link
        for i, lang in enumerate(languages):
            print(f"Language {i+1}: {lang.text}")
    
    finally:
        driver.quit()

# Interacting with elements
def interacting_with_elements_example():
    """Example of interacting with elements on a webpage."""
    driver = setup_driver(headless=False)
    
    try:
        # Go to Google
        driver.get("https://www.google.com")
        
        # Find the search box
        search_box = driver.find_element(By.NAME, "q")
        
        # Type text into the search box
        search_box.send_keys("Selenium automation")
        print("Typed 'Selenium automation' in search box")
        time.sleep(1)
        
        # Clear the text
        search_box.clear()
        print("Cleared search box")
        time.sleep(1)
        
        # Type new text
        search_box.send_keys("Python programming")
        print("Typed 'Python programming' in search box")
        time.sleep(1)
        
        # Click the Google Search button
        # First, we need to make it visible by clicking out of the search box
        search_box.send_keys("\t")  # Tab key
        time.sleep(1)
        
        # Now find and click the search button
        search_button = driver.find_element(By.NAME, "btnK")
        search_button.click()
        print("Clicked search button")
        
        # Wait for results page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        # Get text from an element
        results_stats = driver.find_element(By.ID, "result-stats")
        print(f"Results stats: {results_stats.text}")
        
        # Check if an element is displayed
        logo = driver.find_element(By.CSS_SELECTOR, ".lnXdpd")
        print(f"Logo is displayed: {logo.is_displayed()}")
        
        # Get an attribute value
        first_link = driver.find_element(By.CSS_SELECTOR, "#search a")
        href = first_link.get_attribute("href")
        print(f"First link href: {href}")
        
        # Simulate pressing Enter key
        driver.get("https://www.google.com")  # Go back to Google
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("Python tutorials")
        search_box.submit()  # Same as pressing Enter
        print("Submitted search with Enter key")
        
        # Wait for results
        time.sleep(2)
    
    finally:
        driver.quit()

# Waiting for elements to appear
def waiting_for_elements_example():
    """Example of waiting for elements to appear on a webpage."""
    driver = setup_driver()
    
    try:
        # Go to a dynamic website
        driver.get("https://www.wikipedia.org")
        
        # 1. Implicit wait - tells WebDriver to wait for a certain amount of time
        # when trying to find elements if they are not immediately available
        driver.implicitly_wait(10)  # Wait up to 10 seconds
        print("Set implicit wait to 10 seconds")
        
        # This will wait up to 10 seconds for the element to be available
        search_box = driver.find_element(By.ID, "searchInput")
        print("Found search box with implicit wait")
        
        # 2. Explicit wait - wait for a specific condition
        # Let's search for something and wait for results
        search_box.send_keys("Python programming")
        search_box.submit()
        
        # Wait until the title contains "Python programming"
        WebDriverWait(driver, 10).until(
            EC.title_contains("Python programming")
        )
        print("Title now contains 'Python programming'")
        
        # 3. Wait for an element to be clickable
        # Wait for the first link to be clickable
        first_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".mw-search-result-heading a"))
        )
        print("First search result link is now clickable")
        
        # 4. Wait for visibility of an element
        # Wait for the search results to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "searchresults"))
        )
        print("Search results are now visible")
        
        # 5. Custom wait condition
        # Let's create a custom condition to wait until at least 3 search results are present
        def at_least_n_elements_found(locator, n):
            """Custom wait condition that waits until at least n elements are found."""
            def condition(driver):
                elements = driver.find_elements(*locator)
                return len(elements) >= n
            return condition
        
        # Wait until at least 3 search results are found
        WebDriverWait(driver, 10).until(
            at_least_n_elements_found((By.CSS_SELECTOR, ".mw-search-result-heading"), 3)
        )
        
        # Count the search results
        results = driver.find_elements(By.CSS_SELECTOR, ".mw-search-result-heading")
        print(f"Found {len(results)} search results")
    
    except TimeoutException:
        print("Timed out waiting for element")
    
    finally:
        driver.quit()

# Taking screenshots
def screenshot_example():
    """Example of taking screenshots with Selenium."""
    driver = setup_driver()
    
    try:
        # Go to Wikipedia
        driver.get("https://www.wikipedia.org")
        
        # Take a screenshot of the entire page
        driver.save_screenshot("wikipedia_homepage.png")
        print("Saved screenshot of entire page to wikipedia_homepage.png")
        
        # Take a screenshot of a specific element
        search_box = driver.find_element(By.ID, "searchInput")
        search_box.screenshot("search_box.png")
        print("Saved screenshot of search box to search_box.png")
        
        # Search for something
        search_box.send_keys("Python programming")
        search_box.submit()
        
        # Wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "searchresults"))
        )
        
        # Take a screenshot of the search results
        driver.save_screenshot("search_results.png")
        print("Saved screenshot of search results to search_results.png")
    
    finally:
        driver.quit()

# Handling alerts and popups
def alert_example():
    """Example of handling JavaScript alerts and popups."""
    driver = setup_driver(headless=False)  # Alerts may not work in headless mode
    
    try:
        # Create a simple HTML page with alerts
        html = """
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Alert Examples</h2>
            <button onclick="alert('This is an alert!')">Show Alert</button>
            <button onclick="confirm('Do you confirm?')">Show Confirm</button>
            <button onclick="prompt('Enter your name:')">Show Prompt</button>
        </body>
        </html>
        """
        
        # Write the HTML to a temporary file
        with open("alerts.html", "w") as f:
            f.write(html)
        
        # Open the file in the browser
        driver.get("file://" + os.path.abspath("alerts.html"))
        
        # 1. Handle a simple alert
        # Click the button to show an alert
        driver.find_element(By.XPATH, "//button[contains(text(), 'Show Alert')]").click()
        
        # Switch to the alert
        alert = driver.switch_to.alert
        
        # Get the text of the alert
        alert_text = alert.text
        print(f"Alert text: {alert_text}")
        
        # Accept the alert (click OK)
        alert.accept()
        print("Accepted the alert")
        
        # 2. Handle a confirm dialog
        # Click the button to show a confirm dialog
        driver.find_element(By.XPATH, "//button[contains(text(), 'Show Confirm')]").click()
        
        # Switch to the confirm dialog
        confirm = driver.switch_to.alert
        
        # Get the text of the confirm dialog
        confirm_text = confirm.text
        print(f"Confirm text: {confirm_text}")
        
        # Dismiss the confirm dialog (click Cancel)
        confirm.dismiss()
        print("Dismissed the confirm dialog")
        
        # 3. Handle a prompt dialog
        # Click the button to show a prompt dialog
        driver.find_element(By.XPATH, "//button[contains(text(), 'Show Prompt')]").click()
        
        # Switch to the prompt dialog
        prompt = driver.switch_to.alert
        
        # Get the text of the prompt dialog
        prompt_text = prompt.text
        print(f"Prompt text: {prompt_text}")
        
        # Enter text into the prompt dialog
        prompt.send_keys("John Doe")
        print("Entered 'John Doe' into the prompt")
        
        # Accept the prompt dialog (click OK)
        prompt.accept()
        print("Accepted the prompt dialog")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up
        import os
        if os.path.exists("alerts.html"):
            os.remove("alerts.html")
        
        driver.quit()

# Simple practical example: Scraping a weather website
def scrape_weather_example():
    """Practical example: Scrape weather information from a website."""
    driver = setup_driver()
    
    try:
        # Go to a weather website
        driver.get("https://www.weather.gov/")
        
        # Find the search box for location
        search_box = driver.find_element(By.ID, "inputstring")
        
        # Enter a location
        location = "New York, NY"
        search_box.send_keys(location)
        print(f"Searching for weather in {location}")
        
        # Submit the search
        search_box.submit()
        
        # Wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "panel-title"))
        )
        
        # Extract the current conditions
        try:
            current_conditions = driver.find_element(By.CSS_SELECTOR, ".current-conditions .myforecast-current").text
            temperature = driver.find_element(By.CSS_SELECTOR, ".current-conditions .myforecast-current-lrg").text
            weather_description = driver.find_element(By.CSS_SELECTOR, ".current-conditions .myforecast-current-sm").text
            
            print("\nCurrent Weather:")
            print(f"Conditions: {current_conditions}")
            print(f"Temperature: {temperature}")
            print(f"Description: {weather_description}")
            
            # Extract the forecast
            forecast_days = driver.find_elements(By.CSS_SELECTOR, ".tombstone-container .period-name")
            forecast_descs = driver.find_elements(By.CSS_SELECTOR, ".tombstone-container .forecast-text")
            forecast_temps = driver.find_elements(By.CSS_SELECTOR, ".tombstone-container .temp")
            
            print("\nForecast:")
            for i in range(min(len(forecast_days), 5)):  # Show up to 5 days
                print(f"{forecast_days[i].text}: {forecast_temps[i].text} - {forecast_descs[i].text}")
            
            # Save the data to a CSV file
            weather_data = []
            for i in range(min(len(forecast_days), len(forecast_descs), len(forecast_temps))):
                weather_data.append({
                    "Day": forecast_days[i].text,
                    "Temperature": forecast_temps[i].text,
                    "Description": forecast_descs[i].text
                })
            
            df = pd.DataFrame(weather_data)
            df.to_csv("weather_forecast.csv", index=False)
            print("\nSaved forecast to weather_forecast.csv")
        
        except NoSuchElementException:
            print("Could not find weather information. The website structure might have changed.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()

# Practical example: Filling out a form
def form_filling_example():
    """Practical example: Fill out a web form."""
    driver = setup_driver(headless=False)
    
    try:
        # Create a simple HTML form
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Form Example</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; }
                input, select, textarea { width: 300px; padding: 8px; }
                button { padding: 10px 15px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                #result { margin-top: 20px; padding: 10px; border: 1px solid #ddd; display: none; }
            </style>
        </head>
        <body>
            <h2>Registration Form</h2>
            <form id="registrationForm">
                <div class="form-group">
                    <label for="name">Full Name:</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <div class="form-group">
                    <label for="dob">Date of Birth:</label>
                    <input type="date" id="dob" name="dob">
                </div>
                
                <div class="form-group">
                    <label for="gender">Gender:</label>
                    <select id="gender" name="gender">
                        <option value="">Select</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Interests:</label>
                    <div>
                        <input type="checkbox" id="tech" name="interests" value="technology">
                        <label for="tech">Technology</label>
                    </div>
                    <div>
                        <input type="checkbox" id="sports" name="interests" value="sports">
                        <label for="sports">Sports</label>
                    </div>
                    <div>
                        <input type="checkbox" id="music" name="interests" value="music">
                        <label for="music">Music</label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Subscribe to newsletter:</label>
                    <div>
                        <input type="radio" id="yes" name="subscribe" value="yes">
                        <label for="yes">Yes</label>
                    </div>
                    <div>
                        <input type="radio" id="no" name="subscribe" value="no">
                        <label for="no">No</label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="comments">Comments:</label>
                    <textarea id="comments" name="comments" rows="4"></textarea>
                </div>
                
                <button type="submit">Submit</button>
            </form>
            
            <div id="result">
                <h3>Form Submitted Successfully!</h3>
                <p>Thank you for your submission.</p>
            </div>
            
            <script>
                document.getElementById('registrationForm').addEventListener('submit', function(e) {
                    e.preventDefault();
                    document.getElementById('result').style.display = 'block';
                });
            </script>
        </body>
        </html>
        """
        
        # Write the HTML to a temporary file
        with open("form.html", "w") as f:
            f.write(html)
        
        # Open the file in the browser
        driver.get("file://" + os.path.abspath("form.html"))
        
        # Fill out the form
        # Text inputs
        driver.find_element(By.ID, "name").send_keys("John Doe")
        driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
        driver.find_element(By.ID, "password").send_keys("securepassword")
        
        # Date input
        driver.find_element(By.ID, "dob").send_keys("01/15/1990")
        
        # Select dropdown
        from selenium.webdriver.support.ui import Select
        select = Select(driver.find_element(By.ID, "gender"))
        select.select_by_value("male")  # Select by value
        # Alternative ways to select:
        # select.select_by_visible_text("Male")  # Select by text
        # select.select_by_index(1)  # Select by index (0-based)
        
        # Checkboxes
        driver.find_element(By.ID, "tech").click()  # Check Technology
        driver.find_element(By.ID, "music").click()  # Check Music
        
        # Radio buttons
        driver.find_element(By.ID, "yes").click()  # Select Yes for newsletter
        
        # Textarea
        driver.find_element(By.ID, "comments").send_keys("This is a comment entered by Selenium WebDriver.")
        
        # Take a screenshot before submitting
        driver.save_screenshot("form_filled.png")
        print("Saved screenshot of filled form to form_filled.png")
        
        # Submit the form
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Wait for the result message
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "result"))
        )
        
        # Take a screenshot after submitting
        driver.save_screenshot("form_submitted.png")
        print("Saved screenshot of submitted form to form_submitted.png")
        
        # Verify the result message
        result = driver.find_element(By.ID, "result").text
        print(f"Result message: {result}")
        
        print("\nForm submitted successfully!")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Clean up
        import os
        if os.path.exists("form.html"):
            os.remove("form.html")
        
        driver.quit()

# Run examples
if __name__ == "__main__":
    print("Selenium WebDriver Examples")
    print("==========================")
    print("Choose an example to run:")
    print("1. Basic Navigation")
    print("2. Finding Elements")
    print("3. Interacting with Elements")
    print("4. Waiting for Elements")
    print("5. Taking Screenshots")
    print("6. Handling Alerts")
    print("7. Scraping Weather")
    print("8. Filling Out a Form")
    
    choice = input("Enter your choice (1-8): ")
    
    if choice == "1":
        basic_navigation_example()
    elif choice == "2":
        finding_elements_example()
    elif choice == "3":
        interacting_with_elements_example()
    elif choice == "4":
        waiting_for_elements_example()
    elif choice == "5":
        screenshot_example()
    elif choice == "6":
        alert_example()
    elif choice == "7":
        scrape_weather_example()
    elif choice == "8":
        form_filling_example()
    else:
        print("Invalid choice. Please run the script again and select a number from 1 to 8.")
