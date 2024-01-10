from flask import Flask

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return 'Hello, THIS is the DEMO PROJECT from HAMEED AKSHAL'

# Route with dynamic content
@app.route('/<username>')
def user_profile(username):
    return f'Hello, this is {username}!'
