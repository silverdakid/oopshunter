from flask import Blueprint, render_template, abort, redirect, url_for, flash
from queries.display_analysis_queries import *
from decorators.authentification import *

analysis_display_controller = Blueprint('analysis', __name__)

@analysis_display_controller.route('/analysis/<int:analysis_id>')
@login_required
def show_analysis(analysis_id):

    db = get_db()
    

    analysis_data = get_analysis_with_details(db, analysis_id)
    
    if analysis_data is None:
        return render_template(
            'error.html',
            label="This analysis doesn't exist",
            status=404
        )
    
    return render_template(
        '/display_analysis/display_analysis.html',
        document=analysis_data['document'],
        analysis=analysis_data['analysis'],
        leaks=analysis_data['leaks']
    )

@analysis_display_controller.route("/analysis_history")
@login_required
def show_analysis_history() :
    db = get_db()
    analysis = get_all_analysis(db)
    return render_template('/analysis_history/history.html', analysis=analysis)

@analysis_display_controller.route('/analysis/<int:analysis_id>/delete', methods=['POST'])
@login_required
def delete_analysis_route(analysis_id):
    db = get_db()
    success = delete_analysis(db, analysis_id)
    
    if success:
        flash('Analysis successfully deleted', 'success')
    else:
        flash('Error deleting analysis', 'error')
        
    return redirect(url_for('analysis.show_analysis_history'))
