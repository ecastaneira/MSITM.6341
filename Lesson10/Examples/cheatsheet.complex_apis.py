"""
Complex Web APIs Cheatsheet
==========================

This cheatsheet provides patterns for working with complex web APIs,
including authentication, rate limiting, and data handling.
"""

import requests
import json
import pandas as pd
import time
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from functools import wraps
import requests_cache
from apscheduler.schedulers.background import BackgroundScheduler

# Basic API Request Patterns
def basic_api_requests():
    """Basic patterns for API requests."""
    # GET request
    response = requests.get("https://api.example.com/data")
    
    # POST request with JSON data
    payload = {"name": "John", "age": 30}
    response = requests.post("https://api.example.com/users", json=payload)
    
    # PUT request
    response = requests.put("https://api.example.com/users/1", json={"age": 31})
    
    # DELETE request
    response = requests.delete("https://api.example.com/users/1")
    
    # Request with query parameters
    params = {"page": 1, "limit": 10, "sort": "name"}
    response = requests.get("https://api.example.com/users", params=params)
    
    # Check response status
    if response.status_code == 200:
        # Process successful response
        data = response.json()
        print(f"Retrieved {len(data)} items")
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Authentication Patterns
def authentication_patterns():
    """Patterns for API authentication."""
    # Basic Authentication
    response = requests.get(
        "https://api.example.com/data",
        auth=("username", "password")
    )
    
    # API Key in header
    headers = {"X-API-Key": "your_api_key_here"}
    response = requests.get("https://api.example.com/data", headers=headers)
    
    # API Key in query parameter
    params = {"api_key": "your_api_key_here"}
    response = requests.get("https://api.example.com/data", params=params)
    
    # Bearer Token Authentication
    headers = {"Authorization": "Bearer your_token_here"}
    response = requests.get("https://api.example.com/data", headers=headers)
    
    # OAuth 2.0 Client Credentials Flow
    def get_oauth_token(client_id, client_secret, token_url):
        response = requests.post(
            token_url,
            data={"grant_type": "client_credentials"},
            auth=(client_id, client_secret)
        )
        return response.json()["access_token"]
    
    token = get_oauth_token("client_id", "client_secret", "https://api.example.com/oauth/token")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.example.com/data", headers=headers)

# Rate Limiting and Retry Logic
def setup_retry_session(retries=3, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504)):
    """Set up a session with retry logic."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def rate_limit_decorator(calls_per_second=1):
    """Decorator to limit API calls to a certain rate."""
    min_interval = 1.0 / calls_per_second
    last_call_time = [0.0]  # Use list for mutable state
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            elapsed = current_time - last_call_time[0]
            
            if elapsed < min_interval:
                sleep_time = min_interval - elapsed
                time.sleep(sleep_time)
            
            result = func(*args, **kwargs)
            last_call_time[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit_decorator(calls_per_second=2)
def get_api_data(url):
    """Get data from API with rate limiting."""
    session = setup_retry_session()
    response = session.get(url)
    response.raise_for_status()
    return response.json()

# Example of using rate limiting and retry logic
def rate_limiting_example():
    """Example of using rate limiting and retry logic."""
    # Set up a session with retry logic
    session = setup_retry_session()
    
    # Make a request with automatic retries
    try:
        response = session.get("https://api.example.com/data")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
    
    # Using the rate-limited function
    for i in range(5):
        data = get_api_data(f"https://api.example.com/data?page={i}")
        print(f"Retrieved page {i}")

# Caching API Responses
def caching_example():
    """Example of caching API responses."""
    # Set up a cached session (saves to SQLite by default)
    session = requests_cache.CachedSession(
        'api_cache',
        expire_after=3600  # Cache expires after 1 hour
    )
    
    # Make a request (will be cached)
    response = session.get("https://api.example.com/data")
    print(f"From cache: {response.from_cache}")
    
    # Make the same request again (will use cache)
    response = session.get("https://api.example.com/data")
    print(f"From cache: {response.from_cache}")
    
    # Force a fresh request
    response = session.get("https://api.example.com/data", expire_after=0)
    print(f"From cache: {response.from_cache}")

# Scheduled API Polling
def setup_api_polling(url, interval_seconds=60):
    """Set up scheduled polling of an API."""
    scheduler = BackgroundScheduler()
    
    def poll_api():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"Polled API at {time.strftime('%H:%M:%S')}, got {len(data)} items")
                # Process data here
                return data
        except Exception as e:
            print(f"Error polling API: {e}")
    
    # Schedule the job to run at the specified interval
    scheduler.add_job(poll_api, 'interval', seconds=interval_seconds)
    scheduler.start()
    
    return scheduler  # Return scheduler so it can be shut down later

# Handling Nested JSON with Pandas
def handle_nested_json():
    """Example of handling nested JSON data with pandas."""
    # Sample nested JSON data
    data = [
        {
            "id": 1,
            "name": "John",
            "details": {
                "age": 30,
                "location": {
                    "city": "New York",
                    "country": "USA"
                }
            },
            "tags": ["developer", "python"]
        },
        {
            "id": 2,
            "name": "Jane",
            "details": {
                "age": 28,
                "location": {
                    "city": "San Francisco",
                    "country": "USA"
                }
            },
            "tags": ["designer", "ui"]
        }
    ]
    
    # Convert to DataFrame
    df = pd.json_normalize(
        data,
        sep='_',  # Separator for nested fields
        # Specify paths to nested objects you want to flatten
        meta=[
            'id', 
            'name',
            ['details', 'age'],
            ['details', 'location', 'city'],
            ['details', 'location', 'country']
        ]
    )
    
    print(df.head())
    
    # Handling arrays within JSON
    # Extract tags to a separate DataFrame with one row per tag
    tags_df = pd.DataFrame([
        {'id': item['id'], 'tag': tag}
        for item in data
        for tag in item['tags']
    ])
    
    print(tags_df.head())

# Spotify API Example
class SpotifyAPI:
    """Example class for working with the Spotify API."""
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expiry = 0
        self.base_url = "https://api.spotify.com/v1"
        self.session = setup_retry_session()
    
    def get_token(self):
        """Get or refresh the access token."""
        if self.token and time.time() < self.token_expiry:
            return self.token
        
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = self.session.post(
            auth_url,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret)
        )
        auth_response.raise_for_status()
        
        auth_data = auth_response.json()
        self.token = auth_data["access_token"]
        self.token_expiry = time.time() + auth_data["expires_in"] - 60  # Buffer of 60 seconds
        
        return self.token
    
    def get_headers(self):
        """Get headers with authentication token."""
        return {"Authorization": f"Bearer {self.get_token()}"}
    
    def search(self, query, search_type="track", limit=10):
        """Search for items on Spotify."""
        endpoint = f"{self.base_url}/search"
        params = {
            "q": query,
            "type": search_type,
            "limit": limit
        }
        
        response = self.session.get(endpoint, headers=self.get_headers(), params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_artist(self, artist_id):
        """Get information about an artist."""
        endpoint = f"{self.base_url}/artists/{artist_id}"
        
        response = self.session.get(endpoint, headers=self.get_headers())
        response.raise_for_status()
        
        return response.json()
    
    def get_artist_top_tracks(self, artist_id, country="US"):
        """Get an artist's top tracks."""
        endpoint = f"{self.base_url}/artists/{artist_id}/top-tracks"
        params = {"country": country}
        
        response = self.session.get(endpoint, headers=self.get_headers(), params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_related_artists(self, artist_id):
        """Get artists related to an artist."""
        endpoint = f"{self.base_url}/artists/{artist_id}/related-artists"
        
        response = self.session.get(endpoint, headers=self.get_headers())
        response.raise_for_status()
        
        return response.json()
    
    def get_track_audio_features(self, track_id):
        """Get audio features for a track."""
        endpoint = f"{self.base_url}/audio-features/{track_id}"
        
        response = self.session.get(endpoint, headers=self.get_headers())
        response.raise_for_status()
        
        return response.json()

# Example usage of Spotify API
def spotify_api_example():
    """Example of using the Spotify API."""
    # Replace with your own credentials
    client_id = os.environ.get("SPOTIFY_CLIENT_ID", "your_client_id")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET", "your_client_secret")
    
    spotify = SpotifyAPI(client_id, client_secret)
    
    # Search for an artist
    results = spotify.search("Taylor Swift", search_type="artist")
    
    # Get the first artist from the search results
    if results["artists"]["items"]:
        artist = results["artists"]["items"][0]
        artist_id = artist["id"]
        
        print(f"Artist: {artist['name']}")
        print(f"Popularity: {artist['popularity']}")
        print(f"Followers: {artist['followers']['total']}")
        
        # Get the artist's top tracks
        top_tracks = spotify.get_artist_top_tracks(artist_id)
        
        print("\nTop Tracks:")
        for i, track in enumerate(top_tracks["tracks"], 1):
            print(f"{i}. {track['name']} - {track['album']['name']}")
        
        # Get audio features for the first track
        if top_tracks["tracks"]:
            track_id = top_tracks["tracks"][0]["id"]
            audio_features = spotify.get_track_audio_features(track_id)
            
            print("\nAudio Features for", top_tracks["tracks"][0]["name"])
            print(f"Danceability: {audio_features['danceability']}")
            print(f"Energy: {audio_features['energy']}")
            print(f"Tempo: {audio_features['tempo']} BPM")
    else:
        print("No artists found")

# Example usage
if __name__ == "__main__":
    print("This is a cheatsheet for working with complex web APIs. Import the functions to use them.")
