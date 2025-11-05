from flask import Blueprint, request, jsonify, render_template, redirect
from controllers.display_analysis_controller import *

analysis_controller=Blueprint('analysis_controller', __name__,template_folder='templates')
import analyse.analyse as analyse

@analysis_controller.route("/analyse_doc", methods=["POST"])
def analyse_document():
    try:
        path = request.form.get('path')
        id = request.form.get('id')
        result = analyse.realise_analyse(path, int(id))
        return redirect(url_for("analysis.show_analysis", analysis_id=result))
    except Exception as e:
        print(e)
        return render_template(
            'error.html',
            label="Internal server error: analysis failed",
            status=500
        )
