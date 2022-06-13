from flask import Blueprint, render_template, request, url_for, flash, redirect

site = Blueprint('site', __name__)

@site.route('/', methods=['GET', 'POST'])
def index():
    message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not password or not username or username == '' or password == '':
            flash('Vyplnte prihlásovacia údaje.', category='error')
        else:
            return redirect('/home')

    return render_template('login.html', message=message)


@site.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
