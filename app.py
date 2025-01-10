import os
import logging
from flask import Flask, request, render_template, redirect, url_for, abort, flash
import omdb
from datamanager.sqlite_data_manager import SQLiteDataManager, db
from config.omdb_api_key import OMDB_API_KEY
from utils import fetch_movie_details
from datamanager.sqlite_data_manager import User, Movie

# Set the API key for the OMDb library
omdb.set_default('apikey', OMDB_API_KEY)

# Ensure 'data' directory exists
os.makedirs('data', exist_ok=True)

# Initialize Flask app
def create_app(test_config=None):
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)

    if test_config:
        # Use test configuration if provided
        app.config.from_mapping(test_config)
    else:
        # Default configuration
        working_directory = os.getcwd()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{working_directory}/data/moviwebapp.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.secret_key = 'supersecretkey'

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Import models to ensure they are registered before creating tables
    with app.app_context():
        db.create_all()

    return app

# Create the application instance
app = create_app()

# Initialize data manager
data_manager = SQLiteDataManager(app)

# Configure logging for error tracking
logging.basicConfig(filename='error.log', level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('home.html')  # Create a 'home.html' template

@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()  # Fetch all users from the database
        return render_template('users.html', users=users)
    except Exception as e:
        app.logger.error(f"Error fetching users: {str(e)}")
        abort(500)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    try:
        # Use the data manager to delete the user
        data_manager.delete_user(user_id)
        flash("User deleted successfully!", "success")
        return redirect(url_for('list_users'))  # Redirect back to the list of users
    except ValueError as ve:
        flash(str(ve), "error")  # Handle cases where the user is not found
        return redirect(url_for('list_users'))
    except Exception as e:
        app.logger.error(f"Error deleting user {user_id}: {str(e)}")
        flash("An unexpected error occurred while deleting the user.", "error")
        return redirect(url_for('list_users'))


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    try:
        # Fetch user details using db.session.get()
        user = db.session.get(User, user_id)
        if not user:
            abort(404, description="User not found")

        # Fetch movies for the user
        movies = data_manager.get_user_movies(user_id)

        # Pass user name and movies to the template
        return render_template('user_movies.html', movies=movies, user_name=user.name, user_id=user_id)
    except Exception as e:
        app.logger.error(f"Error fetching movies for user {user_id}: {str(e)}")
        abort(500)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        try:
            name = request.form['name']
            data_manager.add_user({'name': name})  # Add user to database
            return redirect('/users')  # Redirect to users list
        except Exception as e:
            app.logger.error(f"Error adding user: {str(e)}")
            return render_template('add_user.html', error="Failed to add user. Please try again.")
    return render_template('add_user.html')  # Render form for adding user

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
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
            flash(f"Movie '{movie_details['name']}' added successfully!", "success")
            return redirect(url_for('user_movies', user_id=user_id))
        except ValueError as ve:
            flash(str(ve), "error")
        except Exception as e:
            app.logger.error(f"Unexpected error while adding movie: {str(e)}")
            flash("An unexpected error occurred while adding the movie.", "error")

    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
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
            data_manager.update_movie(updated_data)
            flash("Movie updated successfully!", "success")
            return redirect(url_for('user_movies', user_id=user_id))
        except Exception as e:
            app.logger.error(f"Error updating movie {movie_id}: {str(e)}")
            flash("Failed to update movie. Please try again.", "error")
    try:
        movie = data_manager.get_movie(movie_id)
        return render_template('update_movie.html', movie=movie)
    except Exception as e:
        app.logger.error(f"Error fetching movie {movie_id}: {str(e)}")
        abort(500)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    try:
        data_manager.delete_movie(movie_id)
        flash("Movie deleted successfully!", "success")
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        app.logger.error(f"Error deleting movie {movie_id}: {str(e)}")
        abort(500)

@app.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("Starting MovieWeb App...")
    print("Access the application at:")
    print("Local: http://127.0.0.1:5002")
    app.run(debug=True, host='0.0.0.0', port=5002)
