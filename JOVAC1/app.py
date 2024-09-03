from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pickle

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secretKey'
app.config['MONGO_URI'] = 'mongodb+srv://admin:aQ7lG5a5A4N3bSFb@cluster0.mlod4ao.mongodb.net/plantationProject'
mongo = PyMongo(app)
db = mongo.db


crop_recommendation_model_path = 'models/crop_recommendation.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

deficiency_prediction_model_path = 'models/Deficiency_prediction.pkl'
deficiency_prediction_model = pickle.load(open(deficiency_prediction_model_path, 'rb'))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/nd')
def first():
    return render_template("nutrition_deficiency.html")

@app.route('/crop-recc')
def second():
    return render_template("crop_recommendation.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = mongo.db.users.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your email and/or password.', 'danger')
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = {
            'name': name,
            'email': email,
            'password': hashed_password
        }
        app.logger.debug(f"Inserting new user: {new_user}")
        try:
            mongo.db.users.insert_one(new_user)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            app.logger.error(f'Registration failed: {str(e)}')
            flash(f'Registration failed: {str(e)}', 'danger')
            return redirect(url_for('register'))
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Handle the form submission logic here (e.g., save to database, send email, etc.)
    return "Message sent successfully!"

@app.route('/crop-predict', methods=['POST'])
def crop_prediction():
    if request.method == 'POST':
        N = float(request.form['nitrogen'])
        P = float(request.form['phosphorous'])
        K = float(request.form['pottasium'])
        T = float(request.form['temperature'])
        H = float(request.form['humidity'])
        ph = float(request.form['ph'])
        
        data = np.array([[N, P, K, T, H, ph]])
        my_prediction = crop_recommendation_model.predict(data)
        final_prediction = my_prediction[0]
        
        return render_template('recommend_result.html', prediction=final_prediction)

@app.route('/crop-deficiency', methods=['POST'])
def crop_deficiency():
    if request.method == 'POST':
        N = float(request.form['nitrogen'])
        P = float(request.form['phosphorous'])
        K = float(request.form['pottasium'])
        ph = float(request.form['ph'])
        CT = request.form['cropname']
        
        data = np.array([[N, P, K, ph, CT]], dtype=object)
        my_prediction = deficiency_prediction_model.predict(data)
        final_prediction = my_prediction[0]
        
        return render_template('deficiency_result.html', prediction=final_prediction)

@app.route('/disease-detection',methods=['POST'])
def disease_detection():
    if request.method == 'POST':

if __name__ == "__main__":
    app.run(port=5555, debug=True)
