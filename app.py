from flask import Flask

# Initialize Flask app
app = Flask(__name__)

# Define a test route
@app.route('/')
def home():
    return "Welcome to MoviWeb App!"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
