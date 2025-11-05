import sqlite3
from flask import g

DATABASE = 'bdd/oopshunter.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def get_documents():
    db = get_db()
    return db.execute("""
        SELECT d.*,
            ar.title as analysis,
            ar.id_analysis as last_analysis_id,
            ifnull(sd.id_sensitive_data, 0) as sensitive_data,
            e.id_location
        FROM document as d
        LEFT JOIN (
            SELECT id_document, title, id_analysis
            FROM analysis_report 
            WHERE (id_document, date_analysis) IN (
                SELECT id_document, MAX(date_analysis)
                FROM analysis_report
                GROUP BY id_document
            )
        ) as ar ON ar.id_document = d.id_document
        LEFT JOIN sensitive_data as sd ON sd.id_analysis = ar.id_analysis
        INNER JOIN produces as p ON p.id_document = d.id_document
        INNER JOIN employee as e ON e.id_employee = p.id_employee
        GROUP BY d.id_document;
    """).fetchall()

def get_locations():
    db = get_db()
    return db.execute('\
        select * from location;\
    ').fetchall()

def insert_document(title: str, type: str, path: str):
    db = get_db()
    document = db.execute('\
        insert into document (title, path, type, date_creation, date_update)\
        values (?, ?, ?, datetime(), datetime());',
        [title, path, type]
    )
    db.commit()
    return document.lastrowid

def insert_produces(id_employee: int, id_document: int):
    db = get_db()
    db.execute('\
        insert into produces (id_employee, id_document) values (?, ?);',
        [id_employee, id_document]
    )
    return db.commit()

def remove_document(title: str):
    db = get_db()
    result = db.execute('select id_document from document where title like ?;', [title]).fetchone()
    id_document = result['id_document']
    db.execute('delete from analysis_report where id_document = ?;', [id_document])
    db.execute('delete from produces where id_document = ?;', [id_document])
    db.execute('delete from document where id_document = ?', [id_document])
    return db.commit()

def insert_analysis_report(id_document: int, title: str):
    db = get_db()
    cursor = db.execute('''
        insert into analysis_report (id_document, date_analysis, title)
        values (?, DateTime('now'), ?)''',
        [id_document, title]
    )
    db.commit()
    last_id = cursor.lastrowid
    return last_id

def get_analysis_report(id_document: int, title: str):
    db = get_db()
    return db.execute('\
        select * from analysis_report where id_document = ? and title = ?;',
        [id_document, title]
    ).fetchone()[0]

def insert_sensitive_data(id_analysis: int, data: str, type: str):
    db = get_db()
    id_type = db.execute('\
        select id_data_type from data_type where type_name = ?;',
        [type]
    ).fetchone()[0]
    db.execute('\
        insert into sensitive_data (data, id_analysis, id_data_type)\
        values (?, ?, ?);',
        [data, id_analysis, id_type]
    )
    return db.commit()

def get_all_information_employee(parameter: str):
    db = get_db()
    query = f'select {parameter} from employee;'
    return db.execute(query).fetchall()

def get_all_data_type():
    db = get_db()
    return db.execute('\
        select * from data_type;\
    ').fetchall()

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None: db.close()