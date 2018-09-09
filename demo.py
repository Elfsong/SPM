import models.data
from flask import Flask, request, render_template, redirect, flash, url_for, session, abort

app = Flask(__name__, static_url_path='', root_path='/root/SPM')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/show')
def user_view():
    try:
        info = session["info"]
        entries = [{"title": "123", "text": "123123"}, {"title": "123", "text": "123123"},
                   {"title": "123", "text": "123123"}, {"title": "123", "text": "123123"}]
        return render_template('user_view.html', entries=entries, info=info)
    except Exception:
        return redirect(url_for("login"))


@app.route('/add_order', methods=['POST'])
def add_order():
    if not session.get('logged_in'):
        abort(401)
    print(request.form['title'])
    print(request.form['text'])

    flash('New entry was successfully posted')
    return redirect(url_for('user_view'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        title = request.form['title']

        data_connector = models.data.data_layer()
        check_result, userinfo = data_connector.login_check(username, password, title)

        if not check_result:
            error = "Invaild username or password!"
            return render_template('login.html', message=error, title=title)

        else:
            session['logged_in'] = True
            session["name"] = userinfo["username"]
            session['info'] = userinfo
            flash('You were logged in')
            if title == "manager":
                return redirect("https://www.facebook.com")
            elif title == "user":
                return redirect(url_for("user_view"))


    if request.method == "GET":
        title = request.args.get('title')
        if not title:
            title = "user"
        return render_template('login.html', title=title)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        home_address = request.form['home_address']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']

        user_dict = {"username": username,
                     "password": password,
                     "home_address": home_address,
                     "phone_number": phone_number,
                     "email_address": email_address}

        try:
            data_connector = models.data.data_layer()
            if data_connector.register_new_customer(user_dict):
                message = "Sign up successful!"
                return redirect(url_for("login", message=message))
            else:
                raise Exception("Database connect error!")
        except Exception as e:
            print("Exception(Datalayer): ", e)
            return render_template('register.html')
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(host='0.0.0.0', debug=True)
