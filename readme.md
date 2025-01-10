# MovieWeb App

MovieWeb App is a Flask-based web application designed to manage movie collections for multiple users. It integrates with the OMDb API to fetch movie details and provides a user-friendly interface for managing users and their associated movies.

## Features

### **User Management**
- Add new users to the database.
- View a list of all registered users.
- Delete users from the system.

### **Movie Management**
- Add movies to a specific user's collection.
- Update movie details such as name, director, year, and rating.
- Delete movies from a user's collection.
- View all movies associated with a specific user.

### **OMDb API Integration**
- Fetch detailed movie information (title, director, year, rating) directly from the OMDb API using the movie's title and optional release year.

### **Error Handling**
- Custom error pages for:
  - **404 Not Found**: Displayed when a requested resource is unavailable.
  - **500 Internal Server Error**: Displayed for unexpected server-side issues.

### **Database**
- Uses SQLite as the database for storing user and movie data.
- Automatically initializes the database on first run.

### **Logging**
- Logs errors and debugging information to an `error.log` file for easier troubleshooting.

## Getting Started

### Prerequisites
- Python 3.8 or later installed on your system.
- OMDb API key for fetching movie details. Place the key in `config/omdb_api_key.py`.

### Installation
1. Clone this repository to your local machine.
2. Install required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Access the app at `http://127.0.0.1:5002`.

## Usage
1. Navigate to the homepage to view available options.
2. Add users and manage their movie collections through intuitive forms.
3. Use error pages or logs for debugging if issues arise.

## Folder Structure
- **`app.py`**: Main application file containing routes and logic.
- **`templates/`**: HTML templates for rendering pages.
- **`data/`**: Directory where SQLite database files are stored.
- **`config/`**: Configuration files, including the OMDb API key.
- **`utils.py`**: Helper functions like fetching movie details from OMDb.

---
