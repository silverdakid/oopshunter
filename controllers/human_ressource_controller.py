from flask import Blueprint, flash, render_template, request, url_for, redirect
from queries.human_ressource_queries import *

hr_controller = Blueprint('hr_controller', __name__, template_folder='templates')

@hr_controller.route('/human_ressource')
def administrator():
    rows = get_employee()
    employees = [dict(row) for row in rows]
    for employee in employees:
        employee['score'] = get_employee_score(employee['id_employee'])[0]
    rows=get_data_type()
    data_types=[dict(row) for row in rows]
    return render_template('human_ressources/human_ressource.html',employees=employees, data_types=data_types)

@hr_controller.route('/add_employee_form')
def add_form():
    rows=get_locations()
    locations = [dict(row) for row in rows]

    rows=get_department()
    departments=[dict(row) for row in rows]
    return render_template('human_ressources/employee_form.html',locations=locations,departments=departments)

@hr_controller.route('/add_employee', methods=['POST'])
def add_employee():
    firstname=request.form.get('firstname')
    lastname=request.form.get('lastname')
    birthday=request.form.get('birthday')
    address=request.form.get('address')
    mail=request.form.get('mail')
    phone=request.form.get('phone')
    password=request.form.get('password')
    id_location = request.form.get('id_location')
    id_department=request.form.get('id_department')
    insert_employee(firstname, lastname, birthday, address, mail, phone, password, id_location, id_department)
    flash('Employee added successfully')
    return redirect(url_for('hr_controller.administrator'))

@hr_controller.route('/delete/<id>')
def delete_employee(id):
    remove_employee(id)
    flash('Employee removed successfully')
    return redirect(url_for('hr_controller.administrator'))


@hr_controller.route('/add_employee_form/<id_employee>')
def update_form(id_employee):
    rows=get_locations()
    locations = [dict(row) for row in rows]

    rows=get_department()
    departments=[dict(row) for row in rows]
    
    rows = get_one_employee(id_employee)
    employee = [dict(row) for row in rows][0]

    return render_template(
        'human_ressources/employee_form.html',
        locations=locations,
        departments=departments,

        id_employee=employee['id_employee'],
        firstname=employee['firstname'],
        lastname=employee['lastname'],
        birthday=employee['birthday'],
        address=employee['address'],
        mail=employee['mail'],
        phone=employee['phone'],
        password=employee['password'],
        id_department=employee['id_department'],
        id_location=employee['id_location']
    )

@hr_controller.route('/update/<id_employee>', methods=['POST'])
def update_employee(id_employee):
    new_firstname=request.form.get('firstname')
    new_lastname=request.form.get('lastname')
    new_birthday=request.form.get('birthday')
    new_address=request.form.get('address')
    new_mail=request.form.get('mail')
    new_phone=request.form.get('phone')
    new_password=request.form.get('password')
    new_id_location = request.form.get('id_location')
    new_id_department=request.form.get('id_department')
    update_personal_information(id_employee, new_firstname, new_lastname, new_birthday, new_address, new_mail, new_phone, new_password, new_id_location, new_id_department)
    flash('Employee updated successfully')
    return redirect(url_for('hr_controller.administrator'))
    
@hr_controller.route('/add_data_type_form')
def add_data_type_form():
    rows=get_function_name()
    algorithms = [dict(row) for row in rows]
    return render_template('human_ressources/data_form.html', algorithms = algorithms)

@hr_controller.route('/add_data_type', methods=['POST'])
def add_data_type():
    type_name=request.form.get('type_name')
    algorithm_name=request.form.get('algorithm_name')
    parameter=request.form.get('parameter')
    insert_data_type(type_name, algorithm_name, parameter)
    return redirect(url_for('hr_controller.administrator'))


@hr_controller.route('/update_data_type_form/<id>', methods=['GET','POST'])
def update_data_form(id):
    row = get_specific_data_type(id)
    data_type = dict(row)

    rows = get_function_name()
    algorithms = [dict(row) for row in rows]
    
    if request.method == 'POST':
        type_name = request.form.get('type_name')
        algorithm_name = request.form.get('algorithm_name')
        parameter = request.form.get('parameter')
        update_data_type(id ,type_name, algorithm_name, parameter)
        return redirect(url_for('hr_controller.administrator'))

    return render_template('human_ressources/data_form.html', algorithms = algorithms, data_type = data_type)

@hr_controller.route('/delete_data_type/<d_name>')
def delete_data_type(d_name):
    remove_data_type(d_name)
    return redirect(url_for('hr_controller.administrator'))