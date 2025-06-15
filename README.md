Django WebSocket Chat Application
This is a real-time chat application built using Django, Channels, and WebSockets. It allows users to join or create chat rooms, select groups created by an admin, and communicate with others in real-time. The application features a responsive UI and persistent message storage in a database.
Features

Real-Time Messaging: Users can send and receive messages instantly using WebSockets.
Room Management: Admins can create chat rooms, and users can join existing rooms.
Persistent Storage: Messages are saved in the database with timestamps and user information.
Responsive Design: The UI is optimized for both desktop and mobile devices.
User Identification: Users set a username before chatting, stored locally for convenience.
Connection Status: A status indicator shows WebSocket connection state.
Error Handling: Robust logging and error handling for WebSocket operations.

Tech Stack

Backend: Django, Django Channels
WebSocket: ASGI with Channels
Frontend: HTML, CSS, JavaScript
Database: SQLite (default, configurable to others like PostgreSQL)
Dependencies: Managed via requirements.txt

Prerequisites

Python 3.8+
Redis (for Channels layer in production)
Git

Setup Instructions

Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies
pip install -r requirements.txt


Apply Migrations
python manage.py makemigrations
python manage.py migrate


Run the Development Server
python manage.py runserver


Access the ApplicationOpen your browser and navigate to http://127.0.0.1:8000.


Usage

Home Page: View available chat rooms or enter a new room name to create/join.
Set Username: Enter a username to start chatting (saved in local storage).
Chat Room: Send messages in real-time, view message history, and see connection status.
Admin Features: Admins can create rooms via the Django admin panel (/admin).

Project Structure

chat/consumers.py: Handles WebSocket connections and message processing.
chat/routing.py: Defines WebSocket URL patterns.
chat/views.py: Manages HTTP views for room listing and message retrieval.
chat/templates/: Contains HTML templates (index.html, room.html).
chat/models.py: Defines Room and Message models for database storage.

Notes

Redis Configuration: For production, configure a Redis backend for Channels in settings.py.
Security: Ensure HTTPS in production for secure WebSocket connections (wss://).
Scalability: Use a production-ready ASGI server like Daphne or Uvicorn.

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit your changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
