from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Store registered users in a list (for demonstration purposes)
registered_users = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Simple validation
        if username and password:
            # Check if username already exists
            if any(user['username'] == username for user in registered_users):
                flash('Username already exists!', 'danger')
            else:
                registered_users.append({'username': username, 'password': password})
                flash('Registration successful!', 'success')
                return redirect(url_for('home'))
        else:
            flash('Please fill out all fields.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists and password is correct
        if any(user['username'] == username and user['password'] == password for user in registered_users):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return f'Welcome, {session["username"]}! <br><a href="/logout">Logout</a>'
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
