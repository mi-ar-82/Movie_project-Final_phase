from flask_sqlalchemy import SQLAlchemy
from .data_manager_interface import DataManagerInterface

db = SQLAlchemy()

# Define User and Movie models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100), nullable=True)
    year = db.Column(db.String(4), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        # Initialize SQLAlchemy with Flask app
        db.init_app(app)
        self.db = db

        # Create tables if they don't exist
        with app.app_context():
            self.db.create_all()

    def get_all_users(self):
        """Retrieve all users."""
        return User.query.all()

    def get_user_movies(self, user_id):
        """Retrieve all movies for a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, user):
        """Add a new user."""
        new_user = User(name=user['name'])
        self.db.session.add(new_user)
        self.db.session.commit()

    def add_movie(self, movie):
        """Add a new movie."""
        new_movie = Movie(
            name=movie['name'],
            director=movie.get('director'),
            year=movie.get('year'),
            rating=movie.get('rating'),
            user_id=movie['user_id']
        )
        self.db.session.add(new_movie)
        self.db.session.commit()

    def update_movie(self, movie):
        """Update an existing movie's details."""
        existing_movie = Movie.query.get(movie['id'])
        if existing_movie:
            existing_movie.name = movie.get('name', existing_movie.name)
            existing_movie.director = movie.get('director', existing_movie.director)
            existing_movie.year = movie.get('year', existing_movie.year)
            existing_movie.rating = movie.get('rating', existing_movie.rating)
            self.db.session.commit()

    def delete_movie(self, movie_id):
        """Delete a movie by its ID."""
        movie_to_delete = Movie.query.get(movie_id)
        if movie_to_delete:
            self.db.session.delete(movie_to_delete)
            self.db.session.commit()
