import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import openai
import boto3
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Configure MySQL database
app.config['MYSQL_HOST'] = 'mysql_host'
app.config['MYSQL_USER'] = 'mysql_user'
app.config['MYSQL_PASSWORD'] = 'mysql_passwd'
app.config['MYSQL_DB'] = 'alnafi'
mysql = MySQL(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize AWS Comprehend
comprehend = boto3.client('comprehend', region_name='us-east-1')

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        # Assuming the columns are in the order: id, username, password
        return User(user[0], user[1])  # Adjust indices based on your columns
    return None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user is None:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('A user with that username already exists.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            # user[0] is id, user[1] is username
            user_obj = User(user[0], user[1])
            login_user(user_obj)
            session['loggedin'] = True
            session['username'] = user[1]  # user[1] is username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=session['username'])

@app.route('/question_answer', methods=['GET', 'POST'])
@login_required
def question_answer():
    if request.method == 'POST':
        question = request.form['question']
        answer = None
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message['content'].strip()
        except openai.error.RateLimitError:
            answer = "Sorry, the service is currently experiencing high demand. Please try again later."
        except Exception as e:
            answer = f"An error occurred: {str(e)}"
        return render_template('question_answer.html', question=question, answer=answer)
    return render_template('qa.html')

@app.route('/sentiment_analysis', methods=['GET', 'POST'])
@login_required
def sentiment_analysis():
    if request.method == 'POST':
        text = request.form['text']
        result = comprehend.detect_sentiment(Text=text, LanguageCode='en')
        sentiment = result['Sentiment']
        return render_template('sentiment_analysis.html', text=text, sentiment=sentiment)
    return render_template('sentiment_analysis.html')

@app.route('/image_classification', methods=['GET', 'POST'])
@login_required
def image_classification():
    if request.method == 'POST':
        image = request.files['image']
        classification_result = "dummy classification result"  # Replace with actual result
        return render_template('image_classification.html', classification_result=classification_result)
    return render_template('image.html')

if __name__ == '__main__':
    app.run(host=0.0.0.0,debug=True)
