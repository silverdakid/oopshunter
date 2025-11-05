from datetime import datetime
import sqlite3
from flask import g



DATABASE = 'bdd/oopshunter.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def get_analysis_with_details(db, analysis_id):
    cursor = db.cursor()
    
    analysis_query = """
    SELECT ar.id_analysis, ar.title, ar.date_analysis,
           d.id_document, d.title, d.type,
           e.firstname, e.lastname
    FROM ANALYSIS_REPORT ar, DOCUMENT d, produces p, EMPLOYEE e
    WHERE ar.id_document = d.id_document
    AND d.id_document = p.id_document
    AND p.id_employee = e.id_employee
    AND ar.id_analysis = ?
    """

    leaks = """
    SELECT dt.type_name, sd.data
    FROM SENSITIVE_DATA sd, DATA_TYPE dt
    WHERE sd.id_data_type = dt.id_data_type
    AND sd.id_analysis = ?
    """
    
    try:
        cursor.execute(analysis_query, (analysis_id,))
        analysis_data = cursor.fetchone()
        
        if not analysis_data:
            return None
            
        cursor.execute(leaks, (analysis_id,))
        leaks = cursor.fetchall()
        
        analysis_result = {
            'document': {
                'title': analysis_data[4],
                'type': analysis_data[5],
                'author': f"{analysis_data[6]} {analysis_data[7]}"
            },
            'analysis': {
                'title': analysis_data[1],
                 'date': analysis_data[2]
            },
            'leaks': [
                {
                    'type': leak[0],
                    'data': leak[1]
                }
                for leak in leaks
            ]
        }
        
        return analysis_result
        
    except Exception as e:
        print(f"Erreur lors de la récupération de l'analyse: {e}")
        return None
    
def get_all_analysis(db):
    cursor = db.cursor()
    
    query = """
       SELECT 
    ar.id_analysis,
    ar.title,
    ar.date_analysis, 
    d.title as document_title,
    COUNT(sd.id_sensitive_data) as sensitive_data_counted
    FROM ANALYSIS_REPORT ar
    LEFT JOIN DOCUMENT d ON ar.id_document = d.id_document
    LEFT JOIN SENSITIVE_DATA sd ON sd.id_analysis = ar.id_analysis
    GROUP BY ar.id_analysis, ar.title, ar.date_analysis, d.title
    ORDER BY ar.date_analysis DESC
    """
    
    try:
        cursor.execute(query)
        analyses = cursor.fetchall()
        
        return [{
            'title': analysis[1],
            'date_analysis': analysis[2],
            'document_title': analysis[3],
            'sensitive_data_counted': analysis[4],
            'id': analysis[0]
        } for analysis in analyses]
        
    except Exception as e:
        print(f"Erreur lors de la récupération des analyses: {e}")
        return []
    
def delete_analysis(db, analysis_id):
    cursor = db.cursor()
    
    try:
        cursor.execute("""
            DELETE FROM SENSITIVE_DATA
            WHERE id_analysis = ?
        """, (analysis_id,))
        
        cursor.execute("""
            DELETE FROM ANALYSIS_REPORT
            WHERE id_analysis = ?
        """, (analysis_id,))
        
        db.commit()
        return True
        
    except Exception as e:
        print(f"Erreur lors de la suppression de l'analyse: {e}")
        db.rollback()
        return False

def get_last_analysis_id(db, document_id):
    cursor = db.cursor()
    
    query = """
        SELECT id_analysis
        FROM ANALYSIS_REPORT
        WHERE id_document = ?
        ORDER BY date_analysis DESC
        LIMIT 1
    """
    
    try:
        cursor.execute(query, (document_id,))
        result = cursor.fetchone()
        
        return result[0] if result else None
        
    except Exception as e:
        print(f"Erreur lors de la récupération de la dernière analyse: {e}")
        return None
    
