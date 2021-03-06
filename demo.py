import models.data
import models.email_notice
from flask import Flask, request, render_template, redirect, flash, url_for, session, abort

app = Flask(__name__, static_url_path='', root_path='/root/SPM')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/user_view')
def user_view():
    if not session.get('logged_in'):
        return redirect(url_for("login"))

    try:
        data_connector = models.data.data_layer()
        entries = data_connector.find_all_order_by_username(session["name"])

        info = session["info"]

        return render_template('user_view.html', entries=entries, info=info)
    except Exception as e:
        print(e)
        return redirect(url_for("login"))

@app.route('/manage_view')
def manage_view():
    if not session.get('logged_in'):
        return redirect(url_for("login", title="manager"))

    try:
        data_connector = models.data.data_layer()

        entries = data_connector.find_all_order()
        info = session["info"]

        return render_template('manage_view.html', entries=entries, info=info)
    except Exception as e:
        print(e)
        return redirect(url_for("login"))

@app.route('/add_order', methods=['POST'])
def add_order():
    if not session.get('logged_in'):
        abort(401)

    order_info = {
        "username": session["name"],
        "number_box": request.form['number_box'],
        "d_address": request.form['d_address'],
        "a_address": request.form['a_address'],
        "d_date": request.form['d_date'],
        "a_date": request.form['a_date'],
        "o_message": request.form['o_message']
    }

    data_connector = models.data.data_layer()

    if data_connector.add_new_order(order_info):
        flash('New entry was successfully posted!')
    else:
        flash('Unknown Error!')

    return redirect(url_for('user_view'))

@app.route('/update_order', methods=['GET', 'POST'])
def update_order():
    if not session.get('logged_in'):
        abort(401)

    if request.method == 'POST':
        order_info = {
            "order_number": request.form['order_number'],
            "status": request.form['status'],
            "d_address": request.form['d_address'],
            "a_address": request.form['a_address'],
            "d_date": request.form['d_date'],
            "a_date": request.form['a_date'],
            "p_date": request.form['p_date'],
            "h_number": request.form['h_number'],
            "o_message": request.form['o_message'],
            "os_message": request.form['os_message'],
        }

        # print(order_info)
        data_connector = models.data.data_layer()
        if data_connector.update_order_by_order_number(order_info):
            flash('This entry was successfully updated!')
            order_number = order_info["order_number"]
            print("order_number:", order_number)
            email_address = data_connector.get_email_by_order_number(order_number)
            print("email_address:", email_address)
            models.email_notice.send_email(email_address, order_info)
        else:
            flash('Unknown Error!')

        return redirect(url_for('manage_view'))

    if request.method == "GET":
        order_number = request.args.get('order_number')

        data_connector = models.data.data_layer()
        entire = data_connector.find_order(order_number)

        return render_template('order_modify.html', entire=entire)


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
                return redirect(url_for("manage_view"))
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
