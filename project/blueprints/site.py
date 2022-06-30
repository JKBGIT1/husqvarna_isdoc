from flask import Blueprint, render_template, request, flash, redirect, abort
from flask_login import login_required, login_user, current_user, logout_user
from project.models import User
from project.database import mongo

site = Blueprint('site', __name__)

@site.route('/', methods=['GET', 'POST'])
def login():
    ''' login for authenticated and not authenticated user '''

    # Cannot access member "is_authenticated" for type "LocalProxy"
    if current_user.is_authenticated and request.method == 'GET': # type: ignore 
        return redirect('/home')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # make sure user's credentials was filled
        if not password or not username or username == '' or password == '':
            flash('Vyplnte prihlásovacia údaje.', category='error')
            return render_template('login.html'), 400

        # db is database and users is collection
        user = mongo.db.users.find_one({ "username": username, "password": password })

        if not user:
            # not valid credentials
            flash('Nesprávne prihlasovacie údaje.', category='error')
            return render_template('login.html'), 400

        login_user(
            User(str(user['_id']))  
        )

        return redirect('/home')

    return render_template('login.html'), 200

@site.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    ''' display home page to user or generate isdoc file from submitted PDF and allow him/her to download it '''

    if request.method == 'POST':
        pdf_file = request.files["pdf_file"]

        if not pdf_file or not pdf_file.filename:
            flash('PDF súbor nebol nahratý. Použite Browse tlačidlo.', category='error')
            return render_template('home.html'), 400

        pdf_file_name = pdf_file.filename

        pdf_file.save(pdf_file_name)

        # TODO: create isdoc

        # TODO: remove uploaded pdf

        # TODO: allow isdoc download

    return render_template('home.html'), 200

@site.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')
