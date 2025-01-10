from flask import Flask

from datamanager.sqlite_data_manager import SQLiteDataManager

# Initialize Flask app
app = Flask(__name__)

data_manager = SQLiteDataManager('moviwebapp.db')



@app.route('/')
def home():
    return render_template('home.html')  # Create a 'home.html' template

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()  # Fetch all users from the database
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)  # Fetch movies for the user
    return render_template('user_movies.html', movies=movies, user_id=user_id)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        data_manager.add_user({'name': name})  # Add user to database
        return redirect('/users')  # Redirect to users list
    return render_template('add_user.html')  # Render form for adding user

@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_data = {
            'name': request.form['name'],
            'director': request.form['director'],
            'year': request.form['year'],
            'rating': request.form['rating'],
            'user_id': user_id
        }
        data_manager.add_movie(movie_data)  # Add movie to database
        return redirect(f'/users/{user_id}')  # Redirect to user's movies page
    return render_template('add_movie.html', user_id=user_id)

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    if request.method == 'POST':
        updated_data = {
            'id': movie_id,
            'name': request.form['name'],
            'director': request.form['director'],
            'year': request.form['year'],
            'rating': request.form['rating']
        }
        data_manager.update_movie(updated_data)  # Update movie in database
        return redirect(f'/users/{user_id}')  # Redirect to user's movies page
    movie = data_manager.get_movie(movie_id)  # Fetch current movie details
    return render_template('update_movie.html', movie=movie)

@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)  # Delete movie from database
    return redirect(f'/users/{user_id}')  # Redirect to user's movies page

@app.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
