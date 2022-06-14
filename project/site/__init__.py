from flask import Blueprint, render_template, request, flash, redirect, abort
from flask_login import login_required
from project.db import init_db

site = Blueprint('site', __name__)
db = init_db()

@site.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # make sure user's credentials was filled
        if not password or not username or username == '' or password == '':
            flash('Vyplnte prihlásovacia údaje.', category='error')
            return render_template('login.html'), 400
        else:
            user = db.users.find_one({ "username": username, "password": password })

            if not user:
                # not valid credentials
                flash('Nesprávne prihlasovacie údaje.', category='error')
                return render_template('login.html'), 400

            return redirect('/home')

    return render_template('login.html'), 200

@site.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pdf_file = request.files["pdf_file"]

        if not pdf_file or not pdf_file.filename:
            # TODO: handle not submitted
            abort(404)

        pdf_file_name = pdf_file.filename

        pdf_file.save(pdf_file_name)

        # TODO: create isdoc

        # TODO: remove uploaded pdf

        # TODO: allow isdoc download

    return render_template('home.html'), 200