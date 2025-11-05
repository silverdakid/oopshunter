import os
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for, session
from werkzeug.datastructures import FileStorage
from urllib.parse import quote

from controllers.default_controller import *
from queries.document_queries import *

from decorators.authentification import *
document_controller = Blueprint('document_controller', __name__, template_folder='templates')

AUTHORIZED_TYPES = ['.docx', '.md', '.pdf', '.xlsx', ".txt"]
RELATIVE_UPLOAD_FOLDER_DOCUMENT = 'files/documents'
UPLOAD_FOLDER_DOCUMENT = os.path.join(os.getcwd(), RELATIVE_UPLOAD_FOLDER_DOCUMENT)


@document_controller.teardown_app_request
def teardown_db(exception): close_db(exception)


def upload_document(file: FileStorage, folder: str):
    if not os.path.exists(folder): os.makedirs(folder)

    file_path = os.path.join(folder, file.filename).replace('\\', '/')

    try:
        file.save(file_path)
        flash('Document added successfully', 'success')
        return redirect(url_for('document_controller.show_document'))
    except Exception as e:
        flash('Error: Unable to save file', 'error')
        return render_template(
            'error.html',
            label="Internal server error: unable to save file",
            status=500
        )



@document_controller.route('/document/show', methods=['GET'])
@login_required
def show_document():
    def apply_filters(
        documents: list, start_date: str, end_date: str, location: str, sensitive_data: bool, type: str, search: str
    ) -> list:
        filtered_documents = []

        if start_date and end_date and start_date > end_date:
            start_date, end_date = end_date, start_date

        for doc in documents:
            containsSensitiveData = doc['sensitive_data'] > 0 if sensitive_data == 'True'\
                else doc['sensitive_data'] == 0 or not sensitive_data
            isGoodLoc = not location or doc['id_location'] == int(location)
            isGoodType = not type or doc['type'] == type
            date_creation = str(datetime.strptime(doc['date_creation'], "%Y-%m-%d %H:%M:%S").date())
            isGoodStartDate = not start_date or date_creation >= start_date
            isGoodEndDate = not end_date or date_creation <= end_date
            matchesSearch = not search or search.lower() in doc['title'].lower()

            if containsSensitiveData and isGoodLoc and isGoodType and isGoodStartDate and isGoodEndDate and matchesSearch:
                filtered_documents.append(doc)

        return filtered_documents

    rows = get_documents()
    documents = [dict(row) for row in rows]
    rows = get_locations()
    locations = [dict(row) for row in rows]

    search_input = request.args.get('search_input')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    location = request.args.get('location')
    sensitive_data = request.args.get('sensitive_data')
    type = request.args.get('type')
    search = request.args.get('search', '')

    filtered_documents = apply_filters(documents, start_date, end_date, location, sensitive_data, type, search)

    return render_template(
        'document/show.html',
        documents=filtered_documents,
        len=len(filtered_documents),

        selected_search_input=search_input if search_input else '',
        selected_start_date=start_date,
        selected_end_date=end_date,
        selected_location=int(location) if location else location,
        selected_sensitive_data=sensitive_data,
        selected_type=type,
        search_query=search,

        types=AUTHORIZED_TYPES,
        locations=locations
    )



@document_controller.route('/document/filter', methods=['POST'])
@login_required
def filter_document():
    want_search_input = request.args.get('want_search_input')

    if want_search_input:
        search_input = request.form.get('search_input')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        location = request.args.get('location')
        sensitive_data = request.args.get('sensitive_data')
        type = request.args.get('type')

    else:
        search_input = request.args.get('search_input')
        sensitive_data = request.form.get('sensitive_data')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        location = request.form.get('id_location')
        type = request.form.get('type')

    return redirect(url_for(
        'document_controller.show_document',
        search_input=search_input,
        sensitive_data=sensitive_data,
        start_date=start_date, 
        end_date=end_date, 
        location=location, 
        type=type
    ))



@document_controller.route('/document/download', methods=['POST'])
@login_required
def download_document():
    filename = request.form.get('filename')
    path = os.path.join(UPLOAD_FOLDER_DOCUMENT, filename)
    return download_locally(path)



@document_controller.route('/document/add', methods=['POST'])
@login_required
def add_document():
    if 'file' not in request.files:
        return render_template(
            'error.html',
            label="Bad request: No file selected",
            status=400
        )

    file = request.files['file']

    if file.filename == '':
        return render_template('error.html', label="Bad Request: No file selected", status=400)

    type = os.path.splitext(file.filename)[1]

    if not type.lower() in AUTHORIZED_TYPES:
        return render_template(
            'error.html',
            label="Bad Request: Unsupported file type",
            status=400
        )

    id_document = insert_document(file.filename, type, os.path.join(RELATIVE_UPLOAD_FOLDER_DOCUMENT, file.filename).replace('\\', '/')  )
    insert_produces(session["id"], id_document)

    return upload_document(file, UPLOAD_FOLDER_DOCUMENT)



@document_controller.route('/document/delete/<filename>')
@login_required
def delete_document(filename: str):
    remove_document(filename)

    try:
        file_path = os.path.join(UPLOAD_FOLDER_DOCUMENT, filename).replace('\\', '/')
        os.remove(file_path)
        flash('Document removed successfully', 'success')
        return redirect(url_for('document_controller.show_document'))
    except Exception as e:
        flash('Error: Document does not exist', 'error')
        return render_template(
            'error.html',
            label="Internal server error: document doesn't exist",
            status=500
        )