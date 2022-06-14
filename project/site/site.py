from flask import Blueprint, render_template, request, flash, redirect, abort

site = Blueprint('site', __name__)

@site.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not password or not username or username == '' or password == '':
            flash('Vyplnte prihlásovacia údaje.', category='error')
            return render_template('login.html'), 400
        else:
            return redirect('/home')

    return render_template('login.html'), 200

@site.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html'), 200
