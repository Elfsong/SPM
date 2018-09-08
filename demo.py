from flask import Flask, request, render_template, redirect, flash, url_for, session

app = Flask(__name__, static_url_path='', root_path='/root/SPM')    

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/show')
def show_entries():
    entries = [{"title":"123", "text":"123123"},{"title":"123", "text":"123123"},{"title":"123", "text":"123123"},{"title":"123", "text":"123123"}]
    return render_template('show_entries.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != "user":
            error = 'Invalid username'
        elif request.form['password'] != "passwd":
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', message=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        home_address = request.form['home_address']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']

        print("Username:", username)
        print("Password:", password)
        print("home_address:", home_address)
        print("phone_number:", phone_number)
        print("email_address:", email_address)
        # TODO: Connect with Database

        message = "Sign up successful!"
        return redirect(url_for("login", message = message))
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', debug=True)
