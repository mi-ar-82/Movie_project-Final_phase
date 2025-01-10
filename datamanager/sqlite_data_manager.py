from sqlalchemy.exc import IntegrityError
from .data_manager_interface import DataManagerInterface
from datamanager.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    director = db.Column(db.String(100), nullable = True)
    year = db.Column(db.String(4), nullable = True)
    rating = db.Column(db.Float, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.app = app
        with self.app.app_context():
            db.create_all()
    
    def get_all_users(self):
        with self.app.app_context():
            return db.session.query(User).all()
    
    def get_user_movies(self, user_id):
        with self.app.app_context():
            return Movie.query.filter_by(user_id = user_id).all()
    
    def add_user(self, user):
        with self.app.app_context():
            try:
                new_user = User(name = user['name'])
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                raise ValueError("User already exists.")
    
    def update_user(self, user_id, updated_name):
        with self.app.app_context():
            user = db.session.get(User, user_id)
            if not user:
                raise ValueError("User not found.")
            
            user.name = updated_name
            db.session.commit()
    
    def delete_user(self, user_id):
        with self.app.app_context():
            user_to_delete = db.session.get(User, user_id)
            if not user_to_delete:
                raise ValueError("User not found.")
            
            db.session.delete(user_to_delete)
            db.session.commit()
    
    def add_movie(self, movie):
        with self.app.app_context():
            new_movie = Movie(
                name = movie['name'],
                director = movie.get('director'),
                year = movie.get('year'),
                rating = movie.get('rating'),
                user_id = movie['user_id']
            )
            db.session.add(new_movie)
            db.session.commit()
    
    def update_movie(self, updated_data):
        with self.app.app_context():
            movie = db.session.get(Movie, updated_data['id'])
            if not movie:
                raise ValueError("Movie not found.")
            
            movie.name = updated_data.get('name', movie.name)
            movie.director = updated_data.get('director', movie.director)
            movie.year = updated_data.get('year', movie.year)
            movie.rating = updated_data.get('rating', movie.rating)
            
            db.session.commit()
    
    def delete_movie(self, movie_id):
        with self.app.app_context():
            movie_to_delete = db.session.get(Movie, movie_id)
            if not movie_to_delete:
                raise ValueError("Movie not found.")
            
            db.session.delete(movie_to_delete)
            db.session.commit()
    
    def get_movie(self, movie_id):
        with self.app.app_context():
            movie = db.session.get(Movie, movie_id)
            if not movie:
                raise ValueError("Movie not found.")
            return movie
