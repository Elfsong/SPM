from flask import Flask, request, render_template, redirect, flash

app = Flask(__name__, static_url_path='', root_path='/root/SPM')    

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/show')
def show_entries():
    entries = [{"title":"123", "text":"123123"},{"title":"123", "text":"123123"},{"title":"123", "text":"123123"},{"title":"123", "text":"123123"}]
    return render_template('show_entries.html', entries=entries)

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        if username =="user" and password=="password":
            return redirect("http://www.google.com")
        else:
            message = "Failed Login"
            return render_template('login.html',message=message)
    return render_template('login.html')

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
        return render_template('login.html',message=message)
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
