from flask import Flask, render_template, url_for, redirect
from controllers.authentification_controller import *
from controllers.document_controller import *
from controllers.display_analysis_controller import *
from functools import wraps
from decorators.authentification import *
from controllers.analysis_controller import *

from controllers.human_ressource_controller import *

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', label='Not Found', status=404)

app.register_blueprint(document_controller)
app.register_blueprint(analysis_display_controller)
app.register_blueprint(authentification_controller)
app.register_blueprint(analysis_controller)
app.register_blueprint(hr_controller)

@app.route('/')
@login_required
def display_home():
    return redirect(url_for("document_controller.show_document"))