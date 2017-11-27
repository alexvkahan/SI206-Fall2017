from flask import Flask
app = Flask(__name__)


# the route() decorator is used to bind a function to a URL.
@app.route('/')
def index():
    return 'My Home Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

# The following converters exist:

# string	accepts any text without a slash (the default)
# int	accepts integers
# float	like int but for floating point values
# path	like the default but also accepts slashes
# any	matches one of the items provided
# uuid	accepts UUID strings


# REDIRECTION
@app.route('/projects/')
def projects():
	# Check out what happens when you have (and don't have) the trailing slash
    return 'The project page'

@app.route('/about')
def about():
	# Check out what happens when you have (and don't have) the trailing slash
    return 'The about page'