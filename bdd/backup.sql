PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE DOCUMENT(
   id_document INTEGER CONSTRAINT pk_document PRIMARY KEY AUTOINCREMENT,
   title VARCHAR(50),
   path VARCHAR(50),
   type VARCHAR(10),
   date_creation DATETIME,
   date_update DATETIME
);
INSERT INTO DOCUMENT VALUES(1,'RapportIP.xlsx','files/documents/RapportIP.xlsx','.xlsx','2025-01-07 16:40:38','2025-01-07 16:40:38');
INSERT INTO DOCUMENT VALUES(2,'doc_sans_info.txt','files/documents/doc_sans_info.txt','.txt','2025-01-07 16:41:41','2025-01-07 16:41:41');
INSERT INTO DOCUMENT VALUES(3,'t.docx','files/documents/t.docx','.docx','2025-01-07 16:42:41','2025-01-07 16:42:41');
INSERT INTO DOCUMENT VALUES(4,'message.txt','files/documents/message.txt','.txt','2025-01-07 16:42:54','2025-01-07 16:42:54');
INSERT INTO DOCUMENT VALUES(5,'Rapport_Financier_Projet_NovaTrack_Final.pdf','files/documents/Rapport_Financier_Projet_NovaTrack_Final.pdf','.pdf','2025-01-07 16:43:10','2025-01-07 16:43:10');
INSERT INTO DOCUMENT VALUES(6,'LOG_Chap1.pdf','files/documents/LOG_Chap1.pdf','.pdf','2025-01-07 16:43:37','2025-01-07 16:43:37');
CREATE TABLE LOCATION(
   id_location INTEGER CONSTRAINT pk_location PRIMARY KEY AUTOINCREMENT,
   location_name VARCHAR(50)
);
INSERT INTO LOCATION VALUES(1,'Afrique du Nord');
INSERT INTO LOCATION VALUES(2,'Afrique du Sud');
INSERT INTO LOCATION VALUES(3,'Antarctique');
INSERT INTO LOCATION VALUES(4,'Amérique latine');
INSERT INTO LOCATION VALUES(5,'Amérique du Nord');
INSERT INTO LOCATION VALUES(6,'Asie');
INSERT INTO LOCATION VALUES(7,'Europe Centrale');
INSERT INTO LOCATION VALUES(8,'Europe de Ouest');
INSERT INTO LOCATION VALUES(9,'Europe de Est');
INSERT INTO LOCATION VALUES(10,'Moyen-Orient');
CREATE TABLE DEPARTMENT(
   id_department INTEGER CONSTRAINT pk_department PRIMARY KEY AUTOINCREMENT,
   department_name VARCHAR(50)
);
INSERT INTO DEPARTMENT VALUES(1,'Communication');
INSERT INTO DEPARTMENT VALUES(2,'Finance');
INSERT INTO DEPARTMENT VALUES(3,'Informatique');
INSERT INTO DEPARTMENT VALUES(4,'Juridique');
INSERT INTO DEPARTMENT VALUES(5,'Logistique');
INSERT INTO DEPARTMENT VALUES(6,'Marketing');
INSERT INTO DEPARTMENT VALUES(7,'Production');
INSERT INTO DEPARTMENT VALUES(8,'Ressources humaines');
INSERT INTO DEPARTMENT VALUES(9,'Service client');
CREATE TABLE ANALYSIS_REPORT(
   id_analysis INTEGER CONSTRAINT pk_analysis PRIMARY KEY AUTOINCREMENT,
   title VARCHAR(50),
   date_analysis DATETIME,
   id_document INTEGER NOT NULL,
   CONSTRAINT fk_document_analysis FOREIGN KEY(id_document)
      REFERENCES DOCUMENT(id_document)
);
INSERT INTO ANALYSIS_REPORT VALUES(1,'Analysis for document 1','2025-01-07 12:34:56',1);
INSERT INTO ANALYSIS_REPORT VALUES(2,'Analysis for document 2','2025-01-07 14:23:45',2);
INSERT INTO ANALYSIS_REPORT VALUES(3,'Analysis for document 3','2025-01-07 16:12:34',3);
INSERT INTO ANALYSIS_REPORT VALUES(4,'Analysis for document 4','2025-01-07 18:01:23',4);
INSERT INTO ANALYSIS_REPORT VALUES(5,'Analysis for document 5','2025-01-07 19:50:12',5);
INSERT INTO ANALYSIS_REPORT VALUES(6,'Analysis for document 6','2025-01-07 21:39:01',6);
CREATE TABLE DATA_TYPE(
   id_data_type INTEGER CONSTRAINT pk_data_type PRIMARY KEY AUTOINCREMENT,
   type_name VARCHAR(50),
   algorithm_name VARCHAR(100),
   parameter VARCHAR(300)
);
INSERT INTO DATA_TYPE VALUES(1,'Address','Personal information','address');
INSERT INTO DATA_TYPE VALUES(2,'Credit card','Algorithm de Luhn',NULL);
INSERT INTO DATA_TYPE VALUES(3,'Email','Regex','\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b');
INSERT INTO DATA_TYPE VALUES(4,'Ip address','Regex','\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b');
INSERT INTO DATA_TYPE VALUES(5,'Phone','Phonenumbers',NULL);
INSERT INTO DATA_TYPE VALUES(6,'Date','Regex','\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|\d{2,4}[-/.]\d{1,2}[-/.]\d{1,2})\b');
INSERT INTO DATA_TYPE VALUES(7,'Iban','Regex','\b[a-z]{2}[0-9]{2}(?:[ ]*[A-Z0-9]{4}){3,7}\b');
INSERT INTO DATA_TYPE VALUES(8,'Last name','Personal information','lastname');
INSERT INTO DATA_TYPE VALUES(9,'First name','Personal information','firstname');
INSERT INTO DATA_TYPE VALUES(10,'SSN','Regex','\b[12]\s?[0-9]{2}\s?(?:0[1-9]|1[0-2])\s?(?:2[AB]|[0-9]{2})\s?[0-9]{3}\s?[0-9]{3}\s?[0-9]{2}\b');
CREATE TABLE SENSITIVE_DATA(
   id_sensitive_data INTEGER CONSTRAINT pk_sensitive_data PRIMARY KEY AUTOINCREMENT,
   data TEXT,
   id_analysis INTEGER NOT NULL,
   id_data_type INTEGER NOT NULL,
   CONSTRAINT fk_analysis_sensitive_data FOREIGN KEY(id_analysis)
      REFERENCES ANALYSIS_REPORT(id_analysis),
   CONSTRAINT fk_data_type_sensitive_data FOREIGN KEY(id_data_type)
      REFERENCES DATA_TYPE(id_data_type)
);
INSERT INTO SENSITIVE_DATA VALUES(1,'Nevsky Ave 32-34, St Petersburg, Russie',1,1);
INSERT INTO SENSITIVE_DATA VALUES(2,'192.168.1.100',1,4);
INSERT INTO SENSITIVE_DATA VALUES(3,'192.168.1.1',1,4);
INSERT INTO SENSITIVE_DATA VALUES(4,'192.168.1.150',1,4);
INSERT INTO SENSITIVE_DATA VALUES(5,'192.168.1.200',1,4);
INSERT INTO SENSITIVE_DATA VALUES(6,'192.168.1.50',1,4);
INSERT INTO SENSITIVE_DATA VALUES(7,'2025-01-07',1,6);
INSERT INTO SENSITIVE_DATA VALUES(8,'2025-01-07',1,6);
INSERT INTO SENSITIVE_DATA VALUES(9,'2025-01-07',1,6);
INSERT INTO SENSITIVE_DATA VALUES(10,'2025-01-07',1,6);
INSERT INTO SENSITIVE_DATA VALUES(11,'2025-01-07',1,6);
INSERT INTO SENSITIVE_DATA VALUES(12,'exemple@mailfictif.com',3,3);
INSERT INTO SENSITIVE_DATA VALUES(13,'contact@exemplefictif.com',3,3);
INSERT INTO SENSITIVE_DATA VALUES(14,'192.168.0.123',3,4);
INSERT INTO SENSITIVE_DATA VALUES(15,'+33612345678',3,5);
INSERT INTO SENSITIVE_DATA VALUES(16,'+33123456789',3,5);
INSERT INTO SENSITIVE_DATA VALUES(17,'fr76 3008 7890 0183 3784 1350',3,7);
INSERT INTO SENSITIVE_DATA VALUES(18,'De Lacroix',3,8);
INSERT INTO SENSITIVE_DATA VALUES(19,'Antoine',3,9);
INSERT INTO SENSITIVE_DATA VALUES(20,'exemple@mailfictif.com',4,3);
INSERT INTO SENSITIVE_DATA VALUES(21,'contact@exemplefictif.com',4,3);
INSERT INTO SENSITIVE_DATA VALUES(22,'192.168.0.123',4,4);
INSERT INTO SENSITIVE_DATA VALUES(23,'+33612345678',4,5);
INSERT INTO SENSITIVE_DATA VALUES(24,'+33123456789',4,5);
INSERT INTO SENSITIVE_DATA VALUES(25,'fr76 3008 7333 4803 1739 7689',4,7);
INSERT INTO SENSITIVE_DATA VALUES(26,'De Lacroix',4,8);
INSERT INTO SENSITIVE_DATA VALUES(27,'Antoine',4,9);
INSERT INTO SENSITIVE_DATA VALUES(28,'finance@novatrack.com',5,3);
INSERT INTO SENSITIVE_DATA VALUES(29,'+33612345678',5,5);
INSERT INTO SENSITIVE_DATA VALUES(30,'pierre-adrien.tahay@univ-lorraine.fr',6,3);
CREATE TABLE EMPLOYEE(
   id_employee INTEGER CONSTRAINT pk_employee PRIMARY KEY AUTOINCREMENT,
   firstname VARCHAR(50),
   lastname VARCHAR(50),
   birthday DATE,
   address VARCHAR(50),
   mail VARCHAR(50),
   phone VARCHAR(10),
   score INTEGER,
   password VARCHAR(20),
   id_location INTEGER NOT NULL,
   id_department INTEGER NOT NULL,
   CONSTRAINT fk_location_employee FOREIGN KEY(id_location)
      REFERENCES LOCATION(id_location),
   CONSTRAINT fk_department_employee FOREIGN KEY(id_department)
      REFERENCES DEPARTMENT(id_department)
);
INSERT INTO EMPLOYEE VALUES(1,'Antoine','De Lacroix','2002-12-27','2 rue Sainte-Victoire, 13006 Marseille, France','antoine.delacroix@gmail.com','0744564213',NULL,'password',1,1);
INSERT INTO EMPLOYEE VALUES(2,'Marie','Dubois','1995-04-12','15 avenue des Champs, 54840 Gondreville, France','marie.dubois@gmail.com','0654789321',NULL,'securepass',2,2);
INSERT INTO EMPLOYEE VALUES(3,'Alibaba','Ben Ahmed','1988-07-30','10 place des Palmiers, 83420 La Croix-Valmer, France','alibaba.benahmed@gmail.com','0789456123',NULL,'pass1234',6,3);
INSERT INTO EMPLOYEE VALUES(4,'Sophia','Lopez','1990-09-05','25 Centro, 28004 Madrid, Espagne','sophia.lopez@gmail.com','0623789456',NULL,'sophia2023',4,6);
INSERT INTO EMPLOYEE VALUES(5,'John','Smith','1985-11-20','89 E 42nd St, New York, NY 10017, États-Unis','john.smith@gmail.com','0712345678',NULL,'mypassword',5,9);
INSERT INTO EMPLOYEE VALUES(6,'Hiroshi','Tanaka','1992-03-14','10 rue Félix Éboué, 13002 Marseille, France','hiroshi.tanaka@gmail.com','0801234567',NULL,'tanaka2024',6,7);
INSERT INTO EMPLOYEE VALUES(7,'Anna','Ivanova','1998-08-22','Piazza Cenni 1, 80137 Napoli NA, Italie','anna.ivanova@gmail.com','0899456234',NULL,'ivanova98',9,8);
INSERT INTO EMPLOYEE VALUES(8,'Fatima','El Fassi','1993-01-17','64 avenue Simon Bolivar, 75019 Paris, France','fatima.elfassi@gmail.com','0754678921',NULL,'fatima123',1,4);
INSERT INTO EMPLOYEE VALUES(9,'Carlos','Martinez','1987-06-02','Avenida Las Flores 20, Lima 15419, Pérou','carlos.martinez@gmail.com','0678945123',NULL,'carlos1987',4,10);
INSERT INTO EMPLOYEE VALUES(10,'Elena','Petrova','1999-05-29','Nevsky Ave 32-34, St Petersburg, Russie','elena.petrova@gmail.com','0812345678',NULL,'elena99',8,5);
CREATE TABLE produces(
   id_employee INTEGER,
   id_document INTEGER,
   CONSTRAINT pk_produces PRIMARY KEY(id_employee, id_document),
   CONSTRAINT fk_employee_produces FOREIGN KEY(id_employee)
      REFERENCES EMPLOYEE(id_employee),
   CONSTRAINT fk_document_produces FOREIGN KEY(id_document)
      REFERENCES DOCUMENT(id_document)
);
INSERT INTO produces VALUES(1,1);
INSERT INTO produces VALUES(1,2);
INSERT INTO produces VALUES(2,3);
INSERT INTO produces VALUES(2,4);
INSERT INTO produces VALUES(2,5);
INSERT INTO produces VALUES(2,6);
CREATE TABLE finds(
   id_location INTEGER,
   id_department INTEGER,
   CONSTRAINT pk_finds PRIMARY KEY(id_location, id_department),
   CONSTRAINT fk_location_finds FOREIGN KEY(id_location)
      REFERENCES LOCATION(id_location),
   CONSTRAINT fk_department_finds FOREIGN KEY(id_department)
      REFERENCES DEPARTMENT(id_department)
);
INSERT INTO finds VALUES(1,1);
INSERT INTO finds VALUES(1,2);
INSERT INTO finds VALUES(1,6);
INSERT INTO finds VALUES(1,8);
INSERT INTO finds VALUES(1,9);
INSERT INTO finds VALUES(2,3);
INSERT INTO finds VALUES(2,5);
INSERT INTO finds VALUES(2,7);
INSERT INTO finds VALUES(2,9);
INSERT INTO finds VALUES(3,7);
INSERT INTO finds VALUES(4,1);
INSERT INTO finds VALUES(4,5);
INSERT INTO finds VALUES(4,6);
INSERT INTO finds VALUES(4,9);
INSERT INTO finds VALUES(5,2);
INSERT INTO finds VALUES(5,3);
INSERT INTO finds VALUES(5,4);
INSERT INTO finds VALUES(5,6);
INSERT INTO finds VALUES(5,9);
INSERT INTO finds VALUES(6,2);
INSERT INTO finds VALUES(6,3);
INSERT INTO finds VALUES(6,5);
INSERT INTO finds VALUES(6,7);
INSERT INTO finds VALUES(6,8);
INSERT INTO finds VALUES(7,2);
INSERT INTO finds VALUES(7,3);
INSERT INTO finds VALUES(7,4);
INSERT INTO finds VALUES(7,7);
INSERT INTO finds VALUES(7,9);
INSERT INTO finds VALUES(8,1);
INSERT INTO finds VALUES(8,2);
INSERT INTO finds VALUES(8,3);
INSERT INTO finds VALUES(8,6);
INSERT INTO finds VALUES(8,8);
INSERT INTO finds VALUES(9,3);
INSERT INTO finds VALUES(9,4);
INSERT INTO finds VALUES(9,7);
INSERT INTO finds VALUES(9,9);
INSERT INTO finds VALUES(10,2);
INSERT INTO finds VALUES(10,3);
INSERT INTO finds VALUES(10,5);
INSERT INTO finds VALUES(10,8);
INSERT INTO finds VALUES(10,9);
CREATE TABLE links(
   id_department INTEGER,
   id_access INTEGER,
   CONSTRAINT pk_links PRIMARY KEY(id_department, id_access),
   CONSTRAINT fk_department_links FOREIGN KEY(id_department)
      REFERENCES DEPARTMENT(id_department),
   CONSTRAINT fk_access_links FOREIGN KEY(id_access)
      REFERENCES ACCESS(id_access)
);
INSERT INTO links VALUES(1,1);
INSERT INTO links VALUES(1,9);
INSERT INTO links VALUES(1,14);
INSERT INTO links VALUES(2,2);
INSERT INTO links VALUES(2,6);
INSERT INTO links VALUES(2,14);
INSERT INTO links VALUES(3,1);
INSERT INTO links VALUES(3,9);
INSERT INTO links VALUES(3,13);
INSERT INTO links VALUES(4,1);
INSERT INTO links VALUES(4,7);
INSERT INTO links VALUES(5,1);
INSERT INTO links VALUES(5,7);
INSERT INTO links VALUES(5,14);
INSERT INTO links VALUES(7,1);
INSERT INTO links VALUES(8,1);
INSERT INTO links VALUES(8,9);
INSERT INTO links VALUES(8,14);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('LOCATION',10);
INSERT INTO sqlite_sequence VALUES('DEPARTMENT',9);
INSERT INTO sqlite_sequence VALUES('DATA_TYPE',10);
INSERT INTO sqlite_sequence VALUES('EMPLOYEE',10);
INSERT INTO sqlite_sequence VALUES('DOCUMENT',6);
INSERT INTO sqlite_sequence VALUES('ANALYSIS_REPORT',6);
INSERT INTO sqlite_sequence VALUES('SENSITIVE_DATA',30);
COMMIT;
