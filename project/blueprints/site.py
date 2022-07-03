import io
import os
from flask import Blueprint, render_template, request, flash, redirect, send_file
from flask_login import login_required, login_user, current_user, logout_user
from project.models import User
import project.database
from project.parser import pdf_parser

site = Blueprint('site', __name__)

@site.route('/', methods=['GET', 'POST'])
def login():
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
        user = project.database.mongo.db.users.find_one(
            { "username": username, "password": password })

        if not user:
            # not valid credentials
            flash('Nesprávne prihlasovacie údaje.', category='error')
            return render_template('login.html'), 400

        login_user(
            User(str(user['_id']))  
        )

        return redirect('/home')

    return render_template('login.html'), 200


@site.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@site.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
           flash('PDF súbor nebol nahratý. Použite Browse tlačidlo.', category='error')
           return render_template('home.html'), 400

        pdf_file = request.files['pdf_file']

        if not pdf_file or not pdf_file.filename:
            flash('PDF súbor nebol nahratý. Použite Browse tlačidlo.', category='error')
            return render_template('home.html'), 400

        pdf_file_name = pdf_file.filename

        pdf_file.save(pdf_file_name)

        try:
            # TODO: create tests after getting permission for uploading sample pdf and isdoc on github
            invoice_object = pdf_parser.parse_pdf(file_name=pdf_file_name)

            os.remove(pdf_file_name)

            if invoice_object.success_parse_flag is False:
                for err in invoice_object.parsing_errors:
                    flash(err, category='error')
                
                return render_template('home.html'), 400

            creation_errors = pdf_parser.create_is_doc(invoice_object)

            if len(creation_errors):
                for err in creation_errors:
                    flash(err, category='err')

                return render_template('home.html'), 400

            return_data = io.BytesIO()
            isdoc_file_name = invoice_object.isdoc_name()
            
            with open(isdoc_file_name, 'rb') as file:
                return_data.write(file.read())

            return_data.seek(0) # return cursor from last byte to first one

            os.remove(isdoc_file_name)

            return send_file(return_data, mimetype='text/xml',
             as_attachment=True, attachment_filename=isdoc_file_name)

        except:
            if os.path.isfile(pdf_file_name):
                os.remove(pdf_file_name)

            flash('Aplikácia narazila na problém, kontaktujte správcu.', category='error')
            return render_template('home.html'), 400

    return render_template('home.html'), 200