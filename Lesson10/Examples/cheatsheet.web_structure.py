"""
Web Application Structure and Deployment Cheatsheet
==================================================

This cheatsheet provides patterns for structuring and deploying
full-stack web applications with Flask.
"""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
import logging
from dotenv import load_dotenv

# Example of a well-structured Flask application
def create_app(config=None):
    """Create and configure a Flask application using the factory pattern."""
    # Create the Flask app
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key-for-development-only'),
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.static_folder, 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16 MB max upload
    )
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Load the specified configuration object
    if config:
        app.config.from_mapping(config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Configure logging
    if not app.debug:
        handler = logging.FileHandler(os.path.join(app.instance_path, 'app.log'))
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
    
    # Fix for running behind a proxy
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    # Register blueprints
    from .routes import main_bp, api_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Initialize database
    from .data import db
    db.init_app(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

# Error handlers
def register_error_handlers(app):
    """Register error handlers for the Flask app."""
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

# Example directory structure
"""
my_flask_app/
│
├── app/                        # Application package
│   ├── __init__.py            # Contains create_app factory function
│   ├── routes/                # Route definitions
│   │   ├── __init__.py
│   │   ├── main.py            # Main routes
│   │   ├── api.py             # API routes
│   │   └── auth.py            # Authentication routes
│   │
│   ├── data/                  # Data access layer
│   │   ├── __init__.py
│   │   ├── db.py              # Database connection
│   │   └── models.py          # Data models
│   │
│   ├── utils/                 # Utility functions
│   │   ├── __init__.py
│   │   ├── helpers.py         # Helper functions
│   │   └── decorators.py      # Custom decorators
│   │
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── scraper.py         # Web scraping service
│   │   └── api_client.py      # External API client
│   │
│   ├── static/                # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── templates/             # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       └── errors/
│           ├── 404.html
│           └── 500.html
│
├── instance/                  # Instance-specific data
│   └── config.py              # Local config overrides
│
├── migrations/                # Database migrations (if using Flask-Migrate)
│
├── tests/                     # Test suite
│   ├── conftest.py
│   ├── test_routes.py
│   └── test_models.py
│
├── .env                       # Environment variables (not in version control)
├── .gitignore
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── setup.py                   # Package setup
└── wsgi.py                    # WSGI entry point for production
"""

# Example routes module
def routes_example():
    """Example of routes organization using blueprints."""
    from flask import Blueprint, render_template, request, jsonify, current_app
    
    # Main routes blueprint
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def index():
        return render_template('index.html')
    
    @main_bp.route('/dashboard')
    def dashboard():
        # Get data for dashboard
        from ..services import get_dashboard_data
        data = get_dashboard_data()
        return render_template('dashboard.html', data=data)
    
    # API routes blueprint
    api_bp = Blueprint('api', __name__)
    
    @api_bp.route('/data')
    def get_data():
        from ..data.models import get_all_items
        items = get_all_items()
        return jsonify(items)
    
    @api_bp.route('/data', methods=['POST'])
    def add_data():
        data = request.json
        from ..data.models import add_item
        result = add_item(data)
        return jsonify(result), 201
    
    # Auth routes blueprint
    auth_bp = Blueprint('auth', __name__)
    
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # Handle login
            username = request.form['username']
            password = request.form['password']
            from ..services.auth import authenticate
            if authenticate(username, password):
                # Set session, etc.
                return redirect(url_for('main.dashboard'))
            else:
                return render_template('auth/login.html', error="Invalid credentials")
        return render_template('auth/login.html')
    
    return main_bp, api_bp, auth_bp

# Example data models
def data_models_example():
    """Example of data models and database access."""
    import sqlite3
    from flask import current_app, g
    
    # Database connection
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        return g.db
    
    def close_db(e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()
    
    def init_app(app):
        app.teardown_appcontext(close_db)
    
    # Example model functions
    def get_all_items():
        db = get_db()
        items = db.execute('SELECT * FROM items').fetchall()
        return [dict(item) for item in items]
    
    def get_item(item_id):
        db = get_db()
        item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
        return dict(item) if item else None
    
    def add_item(item_data):
        db = get_db()
        cursor = db.execute(
            'INSERT INTO items (name, description, value) VALUES (?, ?, ?)',
            (item_data['name'], item_data['description'], item_data['value'])
        )
        db.commit()
        return {'id': cursor.lastrowid, **item_data}
    
    def update_item(item_id, item_data):
        db = get_db()
        db.execute(
            'UPDATE items SET name = ?, description = ?, value = ? WHERE id = ?',
            (item_data['name'], item_data['description'], item_data['value'], item_id)
        )
        db.commit()
        return get_item(item_id)
    
    def delete_item(item_id):
        db = get_db()
        db.execute('DELETE FROM items WHERE id = ?', (item_id,))
        db.commit()
        return {'deleted': True, 'id': item_id}

# Example service for web scraping
def scraper_service_example():
    """Example of a web scraping service."""
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    class WebScraper:
        def __init__(self, use_selenium=False):
            self.use_selenium = use_selenium
            self.driver = None
            if use_selenium:
                self._setup_selenium()
        
        def _setup_selenium(self):
            """Set up Selenium WebDriver."""
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            self.driver = webdriver.Chrome(options=chrome_options)
        
        def scrape_static_page(self, url):
            """Scrape a static web page."""
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        
        def scrape_dynamic_page(self, url):
            """Scrape a dynamic web page using Selenium."""
            if not self.use_selenium:
                raise ValueError("Selenium is not enabled for this scraper instance")
            
            self.driver.get(url)
            # Wait for dynamic content to load
            self.driver.implicitly_wait(10)
            
            # Get the page source after JavaScript execution
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            return soup
        
        def extract_data(self, soup, selector, attribute=None):
            """Extract data from BeautifulSoup object."""
            elements = soup.select(selector)
            
            if attribute:
                return [element.get(attribute) for element in elements]
            else:
                return [element.text.strip() for element in elements]
        
        def to_dataframe(self, data_dict):
            """Convert extracted data to pandas DataFrame."""
            return pd.DataFrame(data_dict)
        
        def close(self):
            """Close the Selenium WebDriver if it exists."""
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    # Example usage
    def scrape_example():
        # Static page scraping
        scraper = WebScraper()
        soup = scraper.scrape_static_page('https://example.com')
        titles = scraper.extract_data(soup, 'h2.title')
        links = scraper.extract_data(soup, 'a.link', 'href')
        
        data = {
            'title': titles,
            'link': links
        }
        
        df = scraper.to_dataframe(data)
        return df
    
    # Example with Selenium for dynamic content
    def scrape_dynamic_example():
        scraper = WebScraper(use_selenium=True)
        try:
            soup = scraper.scrape_dynamic_page('https://example.com/dynamic')
            data = scraper.extract_data(soup, '.dynamic-content')
            return data
        finally:
            scraper.close()
    
    return WebScraper, scrape_example, scrape_dynamic_example

# Example API client service
def api_client_service_example():
    """Example of an API client service."""
    import requests
    import json
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    class APIClient:
        def __init__(self, base_url, api_key=None):
            self.base_url = base_url
            self.api_key = api_key
            self.session = self._create_session()
        
        def _create_session(self):
            """Create a requests session with retry logic."""
            session = requests.Session()
            retry = Retry(
                total=3,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504]
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            return session
        
        def _get_headers(self):
            """Get request headers including authentication if available."""
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            return headers
        
        def get(self, endpoint, params=None):
            """Make a GET request to the API."""
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(
                url,
                headers=self._get_headers(),
                params=params
            )
            response.raise_for_status()
            return response.json()
        
        def post(self, endpoint, data):
            """Make a POST request to the API."""
            url = f"{self.base_url}/{endpoint}"
            response = self.session.post(
                url,
                headers=self._get_headers(),
                data=json.dumps(data)
            )
            response.raise_for_status()
            return response.json()
        
        def put(self, endpoint, data):
            """Make a PUT request to the API."""
            url = f"{self.base_url}/{endpoint}"
            response = self.session.put(
                url,
                headers=self._get_headers(),
                data=json.dumps(data)
            )
            response.raise_for_status()
            return response.json()
        
        def delete(self, endpoint):
            """Make a DELETE request to the API."""
            url = f"{self.base_url}/{endpoint}"
            response = self.session.delete(
                url,
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    # Example usage
    def api_client_example():
        # Create an API client
        client = APIClient(
            base_url='https://api.example.com/v1',
            api_key='your-api-key'
        )
        
        # Get data from the API
        data = client.get('items', params={'limit': 10})
        
        # Create a new item
        new_item = {
            'name': 'New Item',
            'description': 'This is a new item',
            'value': 42
        }
        created_item = client.post('items', data=new_item)
        
        # Update an item
        updated_item = client.put(f"items/{created_item['id']}", data={
            'name': 'Updated Item',
            'description': 'This item has been updated',
            'value': 43
        })
        
        # Delete an item
        client.delete(f"items/{created_item['id']}")
        
        return data
    
    return APIClient, api_client_example

# Example background task scheduler
def background_tasks_example():
    """Example of background task scheduling."""
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    from apscheduler.triggers.cron import CronTrigger
    import atexit
    
    def setup_scheduler(app):
        """Set up a background scheduler for the Flask app."""
        scheduler = BackgroundScheduler()
        
        # Add jobs to the scheduler
        
        # Job that runs every 10 minutes
        @scheduler.scheduled_job(IntervalTrigger(minutes=10))
        def update_cache():
            with app.app_context():
                app.logger.info("Updating cache...")
                # Fetch new data and update cache
                from .services import update_data_cache
                update_data_cache()
        
        # Job that runs at specific times (every day at 2 AM)
        @scheduler.scheduled_job(CronTrigger(hour=2))
        def daily_report():
            with app.app_context():
                app.logger.info("Generating daily report...")
                # Generate and send daily report
                from .services import generate_daily_report
                generate_daily_report()
        
        # Start the scheduler
        scheduler.start()
        
        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())
        
        return scheduler
    
    return setup_scheduler

# Example deployment configuration
def deployment_config_examples():
    """Examples of deployment configurations for different platforms."""
    
    # Heroku Procfile
    heroku_procfile = """
web: gunicorn wsgi:app
    """
    
    # Docker Dockerfile
    dockerfile = """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
    """
    
    # NGINX configuration for Flask
    nginx_conf = """
server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 30d;
    }
}
    """
    
    # Systemd service file
    systemd_service = """
[Unit]
Description=Flask Web Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/app/venv/bin"
ExecStart=/path/to/your/app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
    """
    
    # PythonAnywhere WSGI configuration
    pythonanywhere_wsgi = """
import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

# Import your app
from wsgi import app as application
    """
    
    return {
        'heroku_procfile': heroku_procfile,
        'dockerfile': dockerfile,
        'nginx_conf': nginx_conf,
        'systemd_service': systemd_service,
        'pythonanywhere_wsgi': pythonanywhere_wsgi
    }

# Example usage
if __name__ == "__main__":
    print("This is a cheatsheet for web application structure and deployment. Import the functions to use them.")
