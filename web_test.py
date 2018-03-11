# export FLASK_APP=web_gui.py
# flask run --host=0.0.0.0


from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route("/")
def index():
    return "The index"


@app.route('/hello')
@app.route('/blah')
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


@app.route('/projects/')          # without slash will redirect to this
def projects():
    return 'The project page'


@app.route('/about')              # with slash will 404
def about():
    return 'The about page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()


@app.route('/test2/')
@app.route('/test2/<name>')
def test2(name=None):
    return render_template('test2.html', name=name)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


## for GET method params
## searchword = request.args.get('key', '')




@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')


from flask import request
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))


if __name__ == "__main__":
    app.run()


















