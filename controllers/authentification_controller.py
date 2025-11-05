from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from queries.authentification_queries import *

authentification_controller=Blueprint('authentification_controller', __name__,template_folder='templates')

@authentification_controller.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        error = None

        login = check_login(email, password)

        if login is None:
            error = "Login failed... Please check your credentials"
            flash(error, "error")
            return render_template('/authentification.html')
        else : 
            session.clear()
            session['email'] = email
            session['id'] = login
            return redirect(url_for("document_controller.show_document"))
    else : # Si méthode GET
        return render_template('/authentification.html')

@authentification_controller.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('authentification_controller.authentification'))