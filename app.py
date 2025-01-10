from flask import Flask

from datamanager.sqlite_data_manager import SQLiteDataManager

# Initialize Flask app
app = Flask(__name__)

data_manager = SQLiteDataManager('moviwebapp.db')



# Define a test route
@app.route('/')
def home():
    return "Welcome to MoviWeb App!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
