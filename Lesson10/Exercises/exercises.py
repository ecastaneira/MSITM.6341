"""
Lesson 10 Exercises: Advanced Web Application Techniques
=======================================================

These simplified exercises will help you practice the concepts covered in Lesson 10,
including dynamic web scraping, API integration, and building interactive dashboards.
Each exercise is designed to be beginner-friendly and executable.
"""

# Exercise 1: Dynamic Web Scraping with Selenium
"""
EXERCISE 1: Dynamic Web Scraping

In this exercise, you'll use Selenium to scrape data from a static website
that's safe to practice on. You'll extract information from the Python.org website.

Tasks:
1. Set up a Selenium WebDriver with Chrome
2. Navigate to the Python.org website
3. Extract the upcoming events from the home page
4. Store the data in a pandas DataFrame
5. Save the data to a CSV file
"""

def exercise1():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import pandas as pd
    import time
    
    print("Starting Exercise 1: Web Scraping with Selenium")
    
    # 1. Set up Selenium WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # 2. Navigate to Python.org
        print("Navigating to Python.org...")
        driver.get("https://www.python.org")
        
        # 3. Extract upcoming events
        print("Extracting upcoming events...")
        event_times = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
        event_names = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")
        
        # Create a list to store the events
        events = []
        for i in range(len(event_times)):
            events.append({
                "date": event_times[i].text,
                "name": event_names[i].text,
                "link": event_names[i].get_attribute("href")
            })
        
        # 4. Create DataFrame
        print(f"Found {len(events)} events")
        df = pd.DataFrame(events)
        
        # Display the events
        print("\nUpcoming Python Events:")
        for i, event in enumerate(events):
            print(f"{i+1}. {event['date']} - {event['name']}")
        
        # 5. Save to CSV
        df.to_csv("python_events.csv", index=False)
        print("\nSaved events to python_events.csv")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Always close the browser
        driver.quit()
        print("Browser closed")


# Exercise 2: Simple API Integration
"""
EXERCISE 2: Simple API Integration

In this exercise, you'll work with a public API that doesn't require authentication.
You'll use the Open Notify API to get information about the International Space Station (ISS).

Tasks:
1. Create a function to fetch the current location of the ISS
2. Create a function to get the number of people currently in space
3. Implement error handling for API requests
4. Display the information in a user-friendly format
"""

def exercise2():
    import requests
    import time
    from datetime import datetime
    
    print("Starting Exercise 2: API Integration")
    
    def get_iss_location():
        """Get the current location of the International Space Station."""
        try:
            response = requests.get("http://api.open-notify.org/iss-now.json")
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            data = response.json()
            latitude = data["iss_position"]["latitude"]
            longitude = data["iss_position"]["longitude"]
            timestamp = data["timestamp"]
            
            # Convert timestamp to readable date
            time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            return {
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": time_str
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Request error: {e}"}
    
    def get_people_in_space():
        """Get information about people currently in space."""
        try:
            response = requests.get("http://api.open-notify.org/astros.json")
            response.raise_for_status()
            
            data = response.json()
            number = data["number"]
            people = data["people"]
            
            return {
                "number": number,
                "people": people
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Request error: {e}"}
    
    # Get ISS location
    print("\nFetching ISS location...")
    location = get_iss_location()
    
    if "error" in location:
        print(location["error"])
    else:
        print("\nCurrent ISS Location:")
        print(f"Latitude: {location['latitude']}")
        print(f"Longitude: {location['longitude']}")
        print(f"Timestamp: {location['timestamp']}")
    
    # Get people in space
    print("\nFetching information about people in space...")
    people_data = get_people_in_space()
    
    if "error" in people_data:
        print(people_data["error"])
    else:
        print(f"\nThere are currently {people_data['number']} people in space:")
        for i, person in enumerate(people_data['people']):
            print(f"{i+1}. {person['name']} on {person['craft']}")
    
    # Bonus: Track ISS for a few positions
    print("\nTracking ISS for 3 positions (with 5-second intervals)...")
    positions = []
    
    for i in range(3):
        location = get_iss_location()
        if "error" not in location:
            positions.append(location)
            print(f"Position {i+1}: Lat {location['latitude']}, Long {location['longitude']}")
        time.sleep(5)  # Wait 5 seconds between requests
    
    print("\nExercise 2 completed!")


# Exercise 3: Simple Interactive Dashboard
"""
EXERCISE 3: Simple Interactive Dashboard

In this exercise, you'll create a basic interactive dashboard using Plotly Dash.
The dashboard will display some simple visualizations with interactive controls.

Tasks:
1. Set up a Dash application with a basic layout
2. Create a bar chart and a line chart with sample data
3. Add a dropdown to select different data views
4. Implement a callback to update the charts based on user selection
"""

def exercise3():
    import dash
    from dash import dcc, html, Input, Output
    import plotly.express as px
    import pandas as pd
    import numpy as np
    
    print("Starting Exercise 3: Interactive Dashboard with Plotly Dash")
    print("This will start a local web server. Access the dashboard at http://127.0.0.1:8050/")
    print("Press Ctrl+C in the terminal to stop the server when you're done.")
    
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
    
    df = pd.DataFrame({
        'date': dates,
        'sales': np.random.randint(10, 100, size=30),
        'customers': np.random.randint(1, 50, size=30),
        'category': np.random.choice(['A', 'B', 'C'], size=30)
    })
    
    # Initialize the Dash app
    app = dash.Dash(__name__)
    
    # Define the layout
    app.layout = html.Div([
        html.H1("Simple Interactive Dashboard"),
        
        html.Div([
            html.Label("Select Data to Display:"),
            dcc.Dropdown(
                id='data-selector',
                options=[
                    {'label': 'Sales', 'value': 'sales'},
                    {'label': 'Customers', 'value': 'customers'}
                ],
                value='sales'  # Default value
            )
        ], style={'width': '300px', 'margin': '20px'}),
        
        html.Div([
            html.Div([
                html.H3("Daily Values"),
                dcc.Graph(id='line-chart')
            ], style={'width': '70%', 'display': 'inline-block'}),
            
            html.Div([
                html.H3("By Category"),
                dcc.Graph(id='bar-chart')
            ], style={'width': '30%', 'display': 'inline-block'})
        ])
    ])
    
    # Define callback to update charts
    @app.callback(
        [Output('line-chart', 'figure'),
         Output('bar-chart', 'figure')],
        [Input('data-selector', 'value')]
    )
    def update_charts(selected_data):
        # Create line chart
        line_fig = px.line(
            df, 
            x='date', 
            y=selected_data,
            title=f'Daily {selected_data.capitalize()}',
            markers=True
        )
        
        # Create bar chart
        bar_data = df.groupby('category')[selected_data].mean().reset_index()
        bar_fig = px.bar(
            bar_data,
            x='category',
            y=selected_data,
            title=f'Average {selected_data.capitalize()} by Category',
            color='category'
        )
        
        return line_fig, bar_fig
    
    # Run the app
    app.run_server(debug=True)


# Exercise 4: Simple Flask App with Templates
"""
EXERCISE 4: Simple Flask App with Templates

In this exercise, you'll create a basic Flask web application with templates.
The app will display data from a simple "database" (a Python dictionary).

Tasks:
1. Set up a Flask application with routes
2. Create HTML templates with Jinja2
3. Pass data from the backend to the templates
4. Add a simple form to collect user input
"""

def exercise4():
    from flask import Flask, render_template, request, redirect, url_for
    
    print("Starting Exercise 4: Flask App with Templates")
    print("This will start a local web server. Access the app at http://127.0.0.1:5000/")
    print("Press Ctrl+C in the terminal to stop the server when you're done.")
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Sample "database" (a Python dictionary)
    products = [
        {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
        {"id": 2, "name": "Headphones", "price": 99.99, "category": "Electronics"},
        {"id": 3, "name": "Coffee Mug", "price": 12.99, "category": "Kitchen"},
        {"id": 4, "name": "Book", "price": 24.99, "category": "Books"},
        {"id": 5, "name": "Smartphone", "price": 699.99, "category": "Electronics"}
    ]
    
    # Create a templates directory and files if they don't exist
    import os
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create base template
    with open(os.path.join(templates_dir, 'base.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Flask App{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        nav { background-color: #f8f9fa; padding: 10px; margin-bottom: 20px; }
        nav a { margin-right: 15px; text-decoration: none; color: #007bff; }
        table { width: 100%; border-collapse: collapse; }
        table, th, td { border: 1px solid #ddd; }
        th, td { padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input, select { width: 100%; padding: 8px; box-sizing: border-box; }
        button { padding: 10px 15px; background-color: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="/">Home</a>
            <a href="/products">Products</a>
            <a href="/add">Add Product</a>
        </nav>
        
        <h1>{% block heading %}Flask App{% endblock %}</h1>
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>""")
    
    # Create home template
    with open(os.path.join(templates_dir, 'home.html'), 'w') as f:
        f.write("""{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block heading %}Welcome to our Product Store{% endblock %}

{% block content %}
    <p>This is a simple Flask application with templates.</p>
    <p>We have {{ product_count }} products in our store.</p>
    <p><a href="/products">View all products</a></p>
{% endblock %}""")
    
    # Create products template
    with open(os.path.join(templates_dir, 'products.html'), 'w') as f:
        f.write("""{% extends 'base.html' %}

{% block title %}Products{% endblock %}

{% block heading %}Our Products{% endblock %}

{% block content %}
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Price</th>
                <th>Category</th>
            </tr>
        </thead>
        <tbody>
            {% for product in products %}
            <tr>
                <td>{{ product.id }}</td>
                <td>{{ product.name }}</td>
                <td>${{ product.price }}</td>
                <td>{{ product.category }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% endblock %}""")
    
    # Create add product template
    with open(os.path.join(templates_dir, 'add.html'), 'w') as f:
        f.write("""{% extends 'base.html' %}

{% block title %}Add Product{% endblock %}

{% block heading %}Add New Product{% endblock %}

{% block content %}
    <form method="POST">
        <div class="form-group">
            <label for="name">Product Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        
        <div class="form-group">
            <label for="price">Price:</label>
            <input type="number" id="price" name="price" step="0.01" min="0" required>
        </div>
        
        <div class="form-group">
            <label for="category">Category:</label>
            <select id="category" name="category" required>
                <option value="">Select a category</option>
                <option value="Electronics">Electronics</option>
                <option value="Kitchen">Kitchen</option>
                <option value="Books">Books</option>
                <option value="Clothing">Clothing</option>
                <option value="Other">Other</option>
            </select>
        </div>
        
        <button type="submit">Add Product</button>
    </form>
{% endblock %}""")
    
    # Define routes
    @app.route('/')
    def home():
        return render_template('home.html', product_count=len(products))
    
    @app.route('/products')
    def product_list():
        return render_template('products.html', products=products)
    
    @app.route('/add', methods=['GET', 'POST'])
    def add_product():
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name')
            price = float(request.form.get('price'))
            category = request.form.get('category')
            
            # Generate a new ID (just increment the highest existing ID)
            new_id = max(product['id'] for product in products) + 1
            
            # Add the new product
            products.append({
                'id': new_id,
                'name': name,
                'price': price,
                'category': category
            })
            
            # Redirect to the products page
            return redirect(url_for('product_list'))
        
        # If it's a GET request, just render the form
        return render_template('add.html')
    
    # Run the app
    app.run(debug=True)


# Exercise 5: Simple Web Scraper and API Dashboard
"""
EXERCISE 5: Simple Web Scraper and API Dashboard

In this exercise, you'll create a simple web application that combines
web scraping and API data into a single dashboard.

Tasks:
1. Create a Flask application with a dashboard layout
2. Fetch data from a public API (Open Notify API for ISS location)
3. Scrape data from a static website (Python.org upcoming events)
4. Display both data sources in a single dashboard
5. Add automatic refresh for the API data
"""

def exercise5():
    from flask import Flask, render_template, jsonify
    import requests
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import pandas as pd
    import threading
    import time
    import os
    import json
    
    print("Starting Exercise 5: Web Scraper and API Dashboard")
    print("This will start a local web server. Access the dashboard at http://127.0.0.1:5000/")
    print("Press Ctrl+C in the terminal to stop the server when you're done.")
    
    # Initialize Flask app
    app = Flask(__name__)
    
    # Create a data store
    data_store = {
        'iss_data': {
            'latitude': 0,
            'longitude': 0,
            'timestamp': 'Not available'
        },
        'python_events': []
    }
    
    # Create templates directory and files
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create base template
    with open(os.path.join(templates_dir, 'dashboard.html'), 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Data Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; }
        .card { border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 20px; }
        .row { display: flex; flex-wrap: wrap; margin: 0 -10px; }
        .col { flex: 1; padding: 0 10px; min-width: 300px; }
        h1, h2 { color: #333; }
        table { width: 100%; border-collapse: collapse; }
        table, th, td { border: 1px solid #ddd; }
        th, td { padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
        #map { height: 300px; background-color: #f8f9fa; border: 1px solid #ddd; border-radius: 5px; }
        .iss-position { padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 15px; }
    </style>
    <!-- Add a simple map placeholder -->
    <script>
        // Function to update ISS data
        function updateISSData() {
            fetch('/api/iss')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('iss-lat').textContent = data.latitude;
                    document.getElementById('iss-long').textContent = data.longitude;
                    document.getElementById('iss-time').textContent = data.timestamp;
                })
                .catch(error => console.error('Error fetching ISS data:', error));
        }
        
        // Update ISS data every 10 seconds
        setInterval(updateISSData, 10000);
        
        // Initialize when the page loads
        document.addEventListener('DOMContentLoaded', function() {
            updateISSData();
        });
    </script>
</head>
<body>
    <div class="container">
        <h1>Data Dashboard</h1>
        
        <div class="row">
            <div class="col">
                <div class="card">
                    <h2>ISS Current Location</h2>
                    <div class="iss-position">
                        <p><strong>Latitude:</strong> <span id="iss-lat">{{ iss_data.latitude }}</span></p>
                        <p><strong>Longitude:</strong> <span id="iss-long">{{ iss_data.longitude }}</span></p>
                        <p><strong>Last Updated:</strong> <span id="iss-time">{{ iss_data.timestamp }}</span></p>
                    </div>
                    <div id="map">
                        <p style="text-align: center; padding-top: 130px;">Map Placeholder</p>
                    </div>
                    <p><small>Data refreshes automatically every 10 seconds</small></p>
                </div>
            </div>
            
            <div class="col">
                <div class="card">
                    <h2>Upcoming Python Events</h2>
                    {% if python_events %}
                        <table>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Event</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for event in python_events %}
                                <tr>
                                    <td>{{ event.date }}</td>
                                    <td>{{ event.name }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    {% else %}
                        <p>No upcoming events found.</p>
                    {% endif %}
                    <p><small>Data from Python.org</small></p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>""")
    
    # Function to get ISS location
    def get_iss_location():
        try:
            response = requests.get("http://api.open-notify.org/iss-now.json")
            response.raise_for_status()
            
            data = response.json()
            latitude = data["iss_position"]["latitude"]
            longitude = data["iss_position"]["longitude"]
            timestamp = data["timestamp"]
            
            # Convert timestamp to readable date
            from datetime import datetime
            time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            # Update data store
            data_store['iss_data'] = {
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": time_str
            }
            
            return data_store['iss_data']
        except Exception as e:
            print(f"Error fetching ISS data: {e}")
            return data_store['iss_data']
    
    # Function to scrape Python.org events
    def scrape_python_events():
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                driver.get("https://www.python.org")
                
                event_times = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
                event_names = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")
                
                events = []
                for i in range(len(event_times)):
                    events.append({
                        "date": event_times[i].text,
                        "name": event_names[i].text
                    })
                
                # Update data store
                data_store['python_events'] = events
                
                return events
            finally:
                driver.quit()
        except Exception as e:
            print(f"Error scraping Python events: {e}")
            return data_store['python_events']
    
    # Background data update thread
    def background_update():
        while True:
            get_iss_location()
            time.sleep(10)  # Update ISS location every 10 seconds
    
    # Start the background thread
    update_thread = threading.Thread(target=background_update, daemon=True)
    update_thread.start()
    
    # Initialize data
    get_iss_location()
    scrape_python_events()
    
    # Define routes
    @app.route('/')
    def dashboard():
        return render_template('dashboard.html', 
                              iss_data=data_store['iss_data'],
                              python_events=data_store['python_events'])
    
    @app.route('/api/iss')
    def api_iss():
        return jsonify(data_store['iss_data'])
    
    @app.route('/api/events')
    def api_events():
        return jsonify(data_store['python_events'])
    
    # Run the app
    app.run(debug=True)


# Run the exercises
if __name__ == "__main__":
    print("Choose an exercise to run (1-5):")
    print("1. Web Scraping with Selenium")
    print("2. API Integration")
    print("3. Interactive Dashboard with Plotly Dash")
    print("4. Flask App with Templates")
    print("5. Web Scraper and API Dashboard")
    
    choice = input("> ")
    
    if choice == "1":
        exercise1()
    elif choice == "2":
        exercise2()
    elif choice == "3":
        exercise3()
    elif choice == "4":
        exercise4()
    elif choice == "5":
        exercise5()
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
