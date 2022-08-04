from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyAIwWO1bXhnp80f3n5uOlohwB1yFZAwgYs",
  "authDomain": "cs-project-64567.firebaseapp.com",
  "projectId": "cs-project-64567",
  "storageBucket": "cs-project-64567.appspot.com",
  "messagingSenderId": "992586419517",
  "appId": "1:992586419517:web:39e05439789edad37dc954",
  "measurementId": "G-DF677BXLNN",
  "databaseURL": "https://cs-project-64567-default-rtdb.europe-west1.firebasedatabase.app/"
}

pics_of_cats =  [ "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/1200px-Cat_November_2010-1a.jpg", 
"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/cute-photos-of-cats-sleeping-arms-1593184782.jpg?crop=0.7887179487179488xw:1xh;center,top&resize=480:*",
"https://cdn.britannica.com/91/181391-050-1DA18304/cat-toes-paw-number-paws-tiger-tabby.jpg"
]
i = 0
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        user = {"list_of_pics": pics_of_cats}
        db.child("Users").child(login_session['user']['localId']).set(user)
        return redirect(url_for('login'))  
    return render_template("signup.html")
      

@app.route('/home', methods=['GET', 'POST'])
def home():
        global i
        if request.method == 'POST':
            if request.form['submit'] == "NOPE":
                db.child("Users").child(login_session['user']['localId']).child("list_of_pics").child(0).remove()  
            i += 1
            if i == 3:
                i = 0
        return render_template("home.html", pic = pics_of_cats[i])         

if __name__ == '__main__':
    app.run(debug=True)