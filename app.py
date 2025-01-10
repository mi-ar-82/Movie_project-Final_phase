import os
import logging
from flask import Flask, request, render_template, redirect, url_for, abort
import omdb
from datamanager.sqlite_data_manager import SQLiteDataManager
from config.omdb_api_key import OMDB_API_KEY  # Import the API key from local file
from utils import fetch_movie_details  # Import utility function

# Set the API key for the omdb library
omdb.set_default('apikey', OMDB_API_KEY)

# Ensure 'data' directory exists
os.makedirs('data', exist_ok = True)

# Initialize Flask app
app = Flask(__name__)

# Dynamically set the database URI using the current working directory
working_directory = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{working_directory}/data/moviwebapp.db'  # Relative path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Initialize data manager
data_manager = SQLiteDataManager(app)

# Configure logging for error tracking
logging.basicConfig(filename = 'error.log', level = logging.ERROR)


@app.route('/')
def home():
    return render_template('home.html')  # Create a 'home.html' template


@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()  # Fetch all users from the database
        return render_template('users.html', users = users)
    except Exception as e:
        app.logger.error(f"Error fetching users: {str(e)}")
        abort(500)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    try:
        movies = data_manager.get_user_movies(user_id)  # Fetch movies for the user
        return render_template('user_movies.html', movies = movies, user_id = user_id)
    except Exception as e:
        app.logger.error(f"Error fetching movies for user {user_id}: {str(e)}")
        abort(500)


@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        try:
            name = request.form['name']
            data_manager.add_user({'name': name})  # Add user to database
            return redirect('/users')  # Redirect to users list
        except Exception as e:
            app.logger.error(f"Error adding user: {str(e)}")
            return render_template('add_user.html', error = "Failed to add user. Please try again.")
    return render_template('add_user.html')  # Render form for adding user


@app.route('/users/<int:user_id>/add_movie', methods = ['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        title = request.form['title']
        year = request.form.get('year')  # Optional field
        
        try:
            # Fetch movie details using OMDb API
            movie_details = fetch_movie_details(title, year)
            if not movie_details or 'error' in movie_details:
                raise ValueError(movie_details.get('error', 'Failed to fetch movie details.'))
            
            # Add movie to the database (using SQLiteDataManager)
            new_movie = {
                'name': movie_details['name'],
                'director': movie_details.get('director'),
                'year': movie_details.get('year'),
                'rating': movie_details.get('rating'),
                'user_id': user_id,
            }
            data_manager.add_movie(new_movie)
            return redirect(url_for('user_movies', user_id = user_id))
        
        except ValueError as ve:
            return render_template('add_movie.html', user_id = user_id, error = str(ve))
        except Exception as e:
            app.logger.error(f"Unexpected error while adding movie: {str(e)}")
            return render_template('add_movie.html', user_id = user_id, error = "An unexpected error occurred.")
    
    return render_template('add_movie.html', user_id = user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods = ['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        try:
            updated_data = {
                'id': movie_id,
                'name': request.form['name'],
                'director': request.form['director'],
                'year': request.form['year'],
                'rating': request.form['rating']
            }
            data_manager.update_movie(updated_data)  # Update movie in database
            return redirect(url_for('user_movies', user_id = user_id))  # Redirect to user's movies page
        except Exception as e:
            app.logger.error(f"Error updating movie {movie_id}: {str(e)}")
            return render_template('update_movie.html', error = "Failed to update movie. Please try again.")
    
    try:
        movie = data_manager.get_movie(movie_id)  # Fetch current movie details
        return render_template('update_movie.html', movie = movie)
    except Exception as e:
        app.logger.error(f"Error fetching movie {movie_id}: {str(e)}")
        abort(500)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods = ['POST'])
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(movie_id)  # Delete movie from database
        return redirect(url_for('user_movies', user_id = user_id))  # Redirect to user's movies page
    except Exception as e:
        app.logger.error(f"Error deleting movie {movie_id}: {str(e)}")
        abort(500)


# Error handlers for HTTP errors
@app.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Run the app
if __name__ == '__main__':
    print("Starting MovieWeb App...")
    print("Access the application at:")
    print("Local: http://127.0.0.1:5002")
    print("Network: http://<your-ip>:5002 (replace <your-ip> with your actual IP address)")
    app.run(debug=True, host='0.0.0.0', port=5002)
