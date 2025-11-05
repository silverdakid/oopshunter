# OopsHunter - Web Application for Data Leak Detection

## Project Context

It is important to note that **OopsHunter is a university project** carried out in a group as part of a first-year project at Telecom Nancy. The application was developed as a team, and tasks were distributed among the members.

My personal contribution focused on the following aspects:

*   **Authentication System**: Implementation of the login logic and route protection.
*   **Analysis Logic and Reports**: Development of the link between the backend and the frontend for processing analyses and displaying data leak reports.
*   **Database**: Participation in the design and integration of the database.
*   **Various Fixes**: Application of multiple corrections throughout the project to ensure its stability.

---

OopsHunter is a web application designed to help companies detect sensitive data leaks within their documents. Users can upload files in various formats (such as `.pdf`, `.xlsx`, `.txt`, `.docx`) and obtain detailed analysis reports with a single click.

The name "OopsHunter" comes from the idea of "hunting" (Hunter) for human errors ("Oops") that lead to the unintentional disclosure of confidential information.

## Features

*   **Document Analysis**: Detects a variety of sensitive data such as credit card numbers, phone numbers, email addresses, etc.
*   **Detailed Reports**: Generates clear reports indicating the type of data that has leaked and the exact data concerned.
*   **Analysis History**: Keeps a history of all analyses performed for easy tracking.
*   **Document Management**: Allows viewing, filtering, adding, and deleting uploaded documents.
*   **Admin Panel**: A section is dedicated to managing employee (user) information, with the ability to calculate a data leak risk score for each.

## Technical Explanations

### Backend

The application is developed with the **Flask** framework in Python. The project structure is organized into **Blueprints** to logically separate the different functionalities (authentication, document management, analyses, etc.). Database queries are isolated in a `queries/` directory and use the `sqlite3` module.

A simple authentication system based on Flask sessions and a `@login_required` decorator secures access to the different parts of the application.

### Database

We use **SQLite** as the database management system. The schema was designed to be flexible, notably thanks to a `DATA_TYPE` table that allows adding new types of data to search for (via regular expressions or keywords) without having to modify the application's source code.

### Detection Algorithms

To "hunt" for sensitive data, OopsHunter combines several techniques:

*   **Keyword Search**: Searches for known character strings (names, first names, etc.).
*   **Regular Expressions**: To identify specific data formats such as emails, IBANs, or social security numbers.
*   **Specialized Libraries**:
    *   `phonenumbers` for the detection and validation of phone numbers.
    *   The **Luhn** algorithm to validate the syntax of credit card numbers.
*   **OCR**: The `pytesseract` library is used to extract text from non-natively readable PDF files.

### Frontend

The user interface is built in **HTML** and styled with the **Bootstrap** framework for a simple and effective user experience.

## How to run the project

### 1. Prerequisites

*   Python 3.x
*   Pip
*   SQLite3
*   Tesseract OCR: Follow the [official documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html) to install it on your system.

### 2. Installation

Clone this repository and navigate into the project directory:

```bash
git clone https://github.com/silverdakid/oopshunter.git
cd oopshunter
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```
*On Windows, use `venv\Scripts\activate`.*

Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 3. Database

A database file `oopshunter.db` is provided for testing. If you need to (re)initialize the database, you can use the `backup.sql` file with the following command:

```bash
sqlite3 oopshunter.db < bdd/backup.sql
```

### 4. Launching the application

Launch the application with Flask:

```bash
flask --app index run
```

The application will then be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### 5. Usage

Once the application is launched, you can log in with the following test accounts:

*   **Account 1:**
    *   **Email**: `antoine.delacroix@gmail.com`
    *   **Password**: `password`
*   **Account 2:**
    *   **Email**: `marie.dubois@gmail.com`
    *   **Password**: `securepass`

You will then be able to:
1.  Add a document to analyze.
2.  Click on the "Analyze" button to start the detection.
3.  Consult the result of the analysis.
4.  View the history of previous analyses.
5.  Access the administration part to manage accounts and types of sensitive data.
