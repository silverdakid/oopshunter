import sqlite3
from flask import g

DATABASE = 'bdd/oopshunter.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def get_one_employee(id_employee: int):
    db = get_db()
    return db.execute('select * from employee where id_employee = ?', [id_employee])

def get_employee():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from employee as e join department on e.id_department=department.id_department join location on e.id_location=location.id_location;")
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_employee_score(id_employee: int):
    db = get_db()
    cursor = db.cursor()
    query = """
    WITH emp_docs AS (
    SELECT d.id_document 
    FROM DOCUMENT d, produces p 
    WHERE p.id_employee = ? 
    AND p.id_document = d.id_document
)
SELECT 
    CASE
        WHEN (SELECT COUNT(DISTINCT id_document) FROM emp_docs) = 0 THEN '0/0'
        ELSE 
            CAST((
                SELECT COUNT(DISTINCT ar.id_analysis)
                FROM emp_docs ed
                JOIN ANALYSIS_REPORT ar ON ed.id_document = ar.id_document
                JOIN SENSITIVE_DATA sd ON ar.id_analysis = sd.id_analysis
            ) AS TEXT)
            || '/' ||
            CAST((SELECT COUNT(DISTINCT id_document) FROM emp_docs) AS TEXT)
    END AS score;
    """

# Exécution de la requête avec l'ID de l'employé comme paramètre
    row = cursor.execute(query, (id_employee,)).fetchone()
    cursor.close()
    return row

def get_locations():
    db = get_db()
    return db.execute('\
        select * from location;\
    ').fetchall()

def get_department():
    db=get_db()
    return db.execute(' select * from department').fetchall()

def insert_employee(firstname: str, lastname: str, birthday: str, address: str,
                    mail: str, phone: str, password: str, id_location: int, id_department: int):
    db = get_db()
    db.execute('\
        insert into employee (firstname, lastname, birthday, address, mail, phone, password, id_location, id_department) values  (?, ?, ?, ?, ?, ?, ?, ?, ?)', 
        [firstname, lastname, birthday, address, mail, phone, password, id_location, id_department])
    return db.commit()

def remove_employee(id):
    db = get_db()

    db.execute('delete from EMPLOYEE where id_employee = ?;', [id])
    db.execute('delete from produces where id_employee = ?;', [id])
    return db.commit()

def update_personal_information(id_employee, new_firstname, new_lastname, new_birthday, 
                                 new_address, new_mail, new_phone, new_password, new_id_location, new_id_department):
    db = get_db()
    db.execute('update employee set firstname = ?, lastname = ?, birthday = ?, address = ?, mail = ?, phone = ?, password = ?, id_location = ?, id_department = ? WHERE id_employee = ?', [new_firstname, new_lastname, new_birthday, new_address, new_mail, new_phone, new_password, new_id_location, new_id_department, id_employee])
    return db.commit()

def get_data_type():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("select * from data_type")
    rows = cursor.fetchall()
    cursor.close()
    return rows

def get_function_name():
    db=get_db()
    rows=db.execute('select distinct(algorithm_name) from data_type').fetchall()   
    return rows

def insert_data_type(type_name, algorithm_name, parameter):
    db = get_db()
    db.execute('\
        insert into data_type (type_name, algorithm_name, parameter) values  (?, ?, ?)', 
        [type_name, algorithm_name, parameter])
    return db.commit()
 
def get_specific_data_type(id):
    db = get_db()
    return db.execute('select * from data_type where id_data_type = ?', [id]).fetchone()

def update_data_type(id_data_type, new_type_name, new_algorithm_name, parameter):
    db = get_db()
    db.execute('update data_type set type_name = ?, algorithm_name = ?, parameter = ? WHERE id_data_type  = ?', [new_type_name, new_algorithm_name, parameter, id_data_type])
    return db.commit()



def remove_data_type(d_name: str):
    db = get_db()
    result = db.execute('select id_data_type from data_type where type_name like ?;', [d_name]).fetchone()
    id_data_type = result['id_data_type']
    db.execute('delete from data_type where id_data_type = ?;', [id_data_type])
    return db.commit()