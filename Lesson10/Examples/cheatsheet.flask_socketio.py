"""
Flask SocketIO Cheatsheet for Live Updates
=========================================

This cheatsheet provides simple patterns for creating real-time web applications
using Flask-SocketIO for live updates and bidirectional communication.
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import time
import threading
import random

# Basic Flask-SocketIO Setup
def basic_socketio_setup():
    """Basic Flask-SocketIO setup with a simple message echo."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    socketio = SocketIO(app)
    
    @app.route('/')
    def index():
        """Render the main page."""
        return render_template('index.html')
    
    @socketio.on('connect')
    def handle_connect():
        """This runs when a client connects to the server."""
        print('Client connected')
        # You can send a welcome message to the client
        emit('message', {'text': 'Welcome to the server!'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """This runs when a client disconnects from the server."""
        print('Client disconnected')
    
    @socketio.on('message')
    def handle_message(message):
        """This runs when a client sends a 'message' event."""
        print('Received message:', message)
        # Echo the message back to the client
        emit('message', {'text': f'Server received: {message}'})
    
    # To run the app:
    # if __name__ == '__main__':
    #     socketio.run(app, debug=True)
    
    return app, socketio

# Example HTML template for the basic setup
def basic_html_template():
    """Example HTML template for a simple chat application."""
    html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Chat</title>
    <!-- Include Socket.IO from CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        #messages { list-style-type: none; margin: 0; padding: 0; }
        #messages li { padding: 5px 10px; }
        #messages li:nth-child(odd) { background: #eee; }
    </style>
</head>
<body>
    <h1>Simple Chat</h1>
    
    <ul id="messages"></ul>
    
    <form id="message-form">
        <input id="message-input" autocomplete="off" placeholder="Type a message..."/>
        <button>Send</button>
    </form>
    
    <script>
        // Connect to the Socket.IO server
        const socket = io();
        
        // Handle form submission
        document.getElementById('message-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const input = document.getElementById('message-input');
            const message = input.value;
            
            if (message) {
                // Send message to server
                socket.emit('message', message);
                input.value = '';
            }
        });
        
        // Receive messages from server
        socket.on('message', function(data) {
            const messages = document.getElementById('messages');
            const li = document.createElement('li');
            li.textContent = data.text;
            messages.appendChild(li);
            
            // Scroll to bottom
            window.scrollTo(0, document.body.scrollHeight);
        });
    </script>
</body>
</html>
    """
    return html_code

# Simple Real-time Counter Example
def realtime_counter_example():
    """Example of a real-time counter that updates every second."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    socketio = SocketIO(app)
    
    # Thread for background updates
    thread = None
    thread_lock = threading.Lock()
    
    def background_thread():
        """Send counter updates to clients every second."""
        count = 0
        while True:
            socketio.sleep(1)
            count += 1
            # Emit the 'update_count' event to all clients
            socketio.emit('update_count', {'count': count})
    
    @app.route('/')
    def index():
        """Render the counter page."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Real-time Counter</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
        </head>
        <body>
            <h1>Real-time Counter</h1>
            <p>Count: <span id="count">0</span></p>
            
            <script>
                const socket = io();
                
                socket.on('update_count', function(data) {
                    document.getElementById('count').textContent = data.count;
                });
            </script>
        </body>
        </html>
        """
    
    @socketio.on('connect')
    def handle_connect():
        """Start the background thread when a client connects."""
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)
    
    # To run the app:
    # if __name__ == '__main__':
    #     socketio.run(app, debug=True)
    
    return app, socketio

# Simple Chat Room Example
def chat_room_example():
    """Example of a chat application with rooms."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    socketio = SocketIO(app)
    
    @app.route('/')
    def index():
        """Render the chat room page."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chat Rooms</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
            <style>
                .message { margin: 5px; padding: 5px; border-bottom: 1px solid #ccc; }
                .room { margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>Chat Rooms</h1>
            
            <div>
                <label for="username">Username:</label>
                <input id="username" value="User" />
            </div>
            
            <div>
                <label for="room-select">Room:</label>
                <select id="room-select">
                    <option value="general">General</option>
                    <option value="tech">Technology</option>
                    <option value="random">Random</option>
                </select>
                <button id="join-btn">Join Room</button>
            </div>
            
            <div class="room">
                <h2>Room: <span id="current-room">None</span></h2>
                <div id="messages"></div>
                
                <div>
                    <input id="message-input" placeholder="Type a message..." />
                    <button id="send-btn">Send</button>
                </div>
            </div>
            
            <script>
                const socket = io();
                let currentRoom = '';
                
                // Join room
                document.getElementById('join-btn').addEventListener('click', function() {
                    const username = document.getElementById('username').value;
                    const room = document.getElementById('room-select').value;
                    
                    // Leave current room if any
                    if (currentRoom) {
                        socket.emit('leave', {room: currentRoom});
                    }
                    
                    // Join new room
                    socket.emit('join', {username: username, room: room});
                    currentRoom = room;
                    document.getElementById('current-room').textContent = room;
                    document.getElementById('messages').innerHTML = '';
                });
                
                // Send message
                document.getElementById('send-btn').addEventListener('click', function() {
                    if (!currentRoom) {
                        alert('Please join a room first');
                        return;
                    }
                    
                    const username = document.getElementById('username').value;
                    const message = document.getElementById('message-input').value;
                    
                    if (message) {
                        socket.emit('room_message', {
                            username: username,
                            room: currentRoom,
                            message: message
                        });
                        document.getElementById('message-input').value = '';
                    }
                });
                
                // Receive room messages
                socket.on('room_message', function(data) {
                    const messages = document.getElementById('messages');
                    const div = document.createElement('div');
                    div.className = 'message';
                    div.textContent = `${data.username}: ${data.message}`;
                    messages.appendChild(div);
                });
                
                // Receive room status updates
                socket.on('room_status', function(data) {
                    const messages = document.getElementById('messages');
                    const div = document.createElement('div');
                    div.className = 'message';
                    div.style.fontStyle = 'italic';
                    div.textContent = data.message;
                    messages.appendChild(div);
                });
            </script>
        </body>
        </html>
        """
    
    @socketio.on('join')
    def on_join(data):
        """Handle a client joining a room."""
        username = data.get('username', 'Anonymous')
        room = data.get('room')
        
        join_room(room)
        emit('room_status', {'message': f'{username} has joined the room'}, to=room)
    
    @socketio.on('leave')
    def on_leave(data):
        """Handle a client leaving a room."""
        username = data.get('username', 'Anonymous')
        room = data.get('room')
        
        leave_room(room)
        emit('room_status', {'message': f'{username} has left the room'}, to=room)
    
    @socketio.on('room_message')
    def handle_room_message(data):
        """Handle a message sent to a room."""
        room = data.get('room')
        username = data.get('username', 'Anonymous')
        message = data.get('message', '')
        
        emit('room_message', {
            'username': username,
            'message': message
        }, to=room)
    
    # To run the app:
    # if __name__ == '__main__':
    #     socketio.run(app, debug=True)
    
    return app, socketio

# Simple Real-time Notification Example
def notification_example():
    """Example of sending real-time notifications to users."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    socketio = SocketIO(app)
    
    # Simulate database of notifications
    notifications = [
        {"id": 1, "message": "Welcome to the application!", "read": False},
        {"id": 2, "message": "You have a new message", "read": False},
        {"id": 3, "message": "Your account was updated", "read": False}
    ]
    
    @app.route('/')
    def index():
        """Render the notification page."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Real-time Notifications</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
            <style>
                .notification { 
                    padding: 10px; 
                    margin: 5px 0; 
                    background-color: #f8f9fa;
                    border-left: 4px solid #007bff;
                }
                .notification.read {
                    opacity: 0.6;
                    border-left-color: #6c757d;
                }
                .badge {
                    display: inline-block;
                    padding: 3px 7px;
                    background-color: #dc3545;
                    color: white;
                    border-radius: 10px;
                    font-size: 12px;
                }
            </style>
        </head>
        <body>
            <h1>Notifications <span id="badge" class="badge">0</span></h1>
            
            <button id="refresh-btn">Refresh Notifications</button>
            <button id="new-btn">Simulate New Notification</button>
            
            <div id="notifications-container"></div>
            
            <script>
                const socket = io();
                
                // Request notifications on page load
                socket.emit('get_notifications');
                
                // Refresh button
                document.getElementById('refresh-btn').addEventListener('click', function() {
                    socket.emit('get_notifications');
                });
                
                // New notification button
                document.getElementById('new-btn').addEventListener('click', function() {
                    socket.emit('create_notification');
                });
                
                // Handle notifications
                socket.on('notifications', function(data) {
                    const container = document.getElementById('notifications-container');
                    container.innerHTML = '';
                    
                    let unreadCount = 0;
                    
                    data.notifications.forEach(function(notification) {
                        const div = document.createElement('div');
                        div.className = 'notification' + (notification.read ? ' read' : '');
                        div.textContent = notification.message;
                        div.dataset.id = notification.id;
                        
                        if (!notification.read) {
                            unreadCount++;
                            
                            // Mark as read when clicked
                            div.addEventListener('click', function() {
                                socket.emit('mark_read', {id: notification.id});
                            });
                        }
                        
                        container.appendChild(div);
                    });
                    
                    // Update badge
                    const badge = document.getElementById('badge');
                    badge.textContent = unreadCount;
                    badge.style.display = unreadCount > 0 ? 'inline-block' : 'none';
                });
                
                // Handle new notification
                socket.on('new_notification', function(data) {
                    // Play sound or show browser notification here
                    
                    // Request updated list
                    socket.emit('get_notifications');
                });
            </script>
        </body>
        </html>
        """
    
    @socketio.on('get_notifications')
    def get_notifications():
        """Send all notifications to the client."""
        emit('notifications', {'notifications': notifications})
    
    @socketio.on('mark_read')
    def mark_read(data):
        """Mark a notification as read."""
        notification_id = data.get('id')
        
        for notification in notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                break
        
        # Send updated notifications to the client
        emit('notifications', {'notifications': notifications})
    
    @socketio.on('create_notification')
    def create_notification():
        """Create a new notification and notify all clients."""
        # Generate a new notification
        new_id = max(n['id'] for n in notifications) + 1
        new_notification = {
            "id": new_id,
            "message": f"New notification #{new_id} at {time.strftime('%H:%M:%S')}",
            "read": False
        }
        
        # Add to notifications
        notifications.append(new_notification)
        
        # Notify all clients
        socketio.emit('new_notification', {'notification': new_notification})
    
    # To run the app:
    # if __name__ == '__main__':
    #     socketio.run(app, debug=True)
    
    return app, socketio

# How to run the examples
if __name__ == "__main__":
    print("This is a cheatsheet for Flask-SocketIO.")
    print("To run an example, import the function and call it:")
    print("\nExample:")
    print("from cheatsheet_flask_socketio import realtime_counter_example")
    print("app, socketio = realtime_counter_example()")
    print("socketio.run(app, debug=True)")
    
    print("\nAvailable examples:")
    print("1. basic_socketio_setup() - Basic setup with message echo")
    print("2. realtime_counter_example() - Counter that updates every second")
    print("3. chat_room_example() - Chat application with rooms")
    print("4. notification_example() - Real-time notifications")
