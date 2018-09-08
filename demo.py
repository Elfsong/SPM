from flask import Flask,request,render_template,redirect

app = Flask(__name__, static_url_path='', root_path='/root/SPM')    

@app.route('/')
def index():
    return app.send_static_file('index.html')


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
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        print("Username:", username)
        print("Password:", password)
        message = "Sign up successful!"
        return render_template('login.html',message=message)
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
