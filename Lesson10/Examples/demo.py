"""
Lesson 10 Demo: Integrated Web Application
=========================================

This demo shows how to integrate dynamic scraping, API calls, and
interactive dashboards into a single Flask application.
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly.express as px
import plotly.utils
import json
import requests
from flask_socketio import SocketIO, emit
import time
import threading
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

# Global data store
data_store = {
    'news': [],
    'stock_prices': {},
    'weather': {}
}

# Thread for background data updates
thread = None
thread_lock = threading.Lock()

# Scraper setup
def setup_selenium():
    """Set up and return a Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# API client for weather data
def get_weather_data(city):
    """Get weather data for a city using OpenWeatherMap API."""
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Background task to update data
def background_update_task():
    """Background task to update data periodically."""
    while True:
        # Update stock prices (simulated)
        update_stock_prices()
        
        # Update weather data
        update_weather_data()
        
        # Emit updates to connected clients
        socketio.emit('data_update', {
            'stocks': data_store['stock_prices'],
            'weather': data_store['weather']
        })
        
        # Sleep for a while
        socketio.sleep(30)  # Update every 30 seconds

def update_stock_prices():
    """Update simulated stock prices."""
    stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    
    for stock in stocks:
        # Initialize if not exists
        if stock not in data_store['stock_prices']:
            data_store['stock_prices'][stock] = {
                'price': random.uniform(100, 1000),
                'change': 0.0,
                'history': []
            }
        
        # Update with random change
        current_price = data_store['stock_prices'][stock]['price']
        change_pct = (random.random() - 0.5) * 0.02  # -1% to +1%
        new_price = current_price * (1 + change_pct)
        new_price = round(new_price, 2)
        
        # Update data store
        data_store['stock_prices'][stock]['price'] = new_price
        data_store['stock_prices'][stock]['change'] = round(new_price - current_price, 2)
        
        # Add to history (keep last 20 points)
        data_store['stock_prices'][stock]['history'].append({
            'time': time.strftime('%H:%M:%S'),
            'price': new_price
        })
        if len(data_store['stock_prices'][stock]['history']) > 20:
            data_store['stock_prices'][stock]['history'] = data_store['stock_prices'][stock]['history'][-20:]

def update_weather_data():
    """Update weather data for selected cities."""
    cities = ['New York', 'London', 'Tokyo', 'Sydney', 'Paris']
    
    for city in cities:
        weather_data = get_weather_data(city)
        if weather_data:
            data_store['weather'][city] = {
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'description': weather_data['weather'][0]['description'],
                'icon': weather_data['weather'][0]['icon']
            }

def scrape_news():
    """Scrape news headlines from a dynamic website."""
    driver = setup_selenium()
    try:
        # Navigate to a news website
        driver.get("https://news.google.com/")
        driver.implicitly_wait(10)
        
        # Find news headlines
        headlines = driver.find_elements(By.CSS_SELECTOR, ".NiLAwe .DY5T1d")
        
        # Extract text and links
        news_items = []
        for headline in headlines[:10]:  # Get first 10 headlines
            title = headline.text
            link = headline.get_attribute("href")
            news_items.append({
                'title': title,
                'link': link,
                'time': time.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Update data store
        data_store['news'] = news_items
        
        return news_items
    finally:
        driver.quit()

# Flask routes
@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

@app.route('/api/news')
def api_news():
    """API endpoint to get news data."""
    # This would normally scrape fresh data, but for demo we'll use cached data
    if not data_store['news']:
        try:
            scrape_news()
        except Exception as e:
            print(f"Error scraping news: {e}")
    
    return jsonify(data_store['news'])

@app.route('/api/stocks')
def api_stocks():
    """API endpoint to get stock data."""
    return jsonify(data_store['stock_prices'])

@app.route('/api/weather')
def api_weather():
    """API endpoint to get weather data."""
    return jsonify(data_store['weather'])

@app.route('/api/chart/stock/<symbol>')
def stock_chart(symbol):
    """Generate a stock price chart for the given symbol."""
    if symbol not in data_store['stock_prices']:
        return jsonify({'error': 'Symbol not found'}), 404
    
    # Extract data for the chart
    history = data_store['stock_prices'][symbol]['history']
    df = pd.DataFrame(history)
    
    # Create a Plotly figure
    fig = px.line(df, x='time', y='price', title=f'{symbol} Price History')
    
    # Convert to JSON
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({'chart': chart_json})

# SocketIO events
@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_update_task)
    
    # Send initial data to the client
    emit('data_update', {
        'stocks': data_store['stock_prices'],
        'weather': data_store['weather']
    })

@socketio.on('request_news_update')
def handle_news_update():
    """Handle request to update news data."""
    try:
        news = scrape_news()
        emit('news_update', news)
    except Exception as e:
        emit('error', {'message': f'Error updating news: {str(e)}'})

# Run the application
if __name__ == '__main__':
    # Initialize some data
    update_stock_prices()
    update_weather_data()
    
    # Run the app
    socketio.run(app, debug=True)
