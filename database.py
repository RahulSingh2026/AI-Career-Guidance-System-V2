import sqlite3
import hashlib


DATABASE_NAME = "career.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Student table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            college TEXT,
            course TEXT,
            year TEXT
        )
    """)

    # Assessment history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            python INTEGER,
            mathematics INTEGER,
            data_analysis INTEGER,
            communication INTEGER,
            problem_solving INTEGER,
            web_development INTEGER,
            interest TEXT,
            recommended_career TEXT,
            match_score REAL,
            ml_prediction TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_student(name, email, password, college, course, year):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO students
            (name, email, password, college, course, year)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            hashed_password,
            college,
            course,
            year
        ))

        conn.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered."

    finally:
        conn.close()


def login_student(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT id, name, email, college, course, year
        FROM students
        WHERE email = ? AND password = ?
    """, (email, hashed_password))

    student = cursor.fetchone()

    conn.close()

    return student


def get_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, college, course, year
        FROM students
        WHERE id = ?
    """, (student_id,))

    student = cursor.fetchone()

    conn.close()

    return student


def save_assessment(
    student_id,
    python,
    mathematics,
    data_analysis,
    communication,
    problem_solving,
    web_development,
    interest,
    recommended_career,
    match_score,
    ml_prediction
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assessments
        (
            student_id,
            python,
            mathematics,
            data_analysis,
            communication,
            problem_solving,
            web_development,
            interest,
            recommended_career,
            match_score,
            ml_prediction
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_id,
        python,
        mathematics,
        data_analysis,
        communication,
        problem_solving,
        web_development,
        interest,
        recommended_career,
        match_score,
        ml_prediction
    ))

    conn.commit()
    conn.close()


def get_assessment_history(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            interest,
            recommended_career,
            match_score,
            ml_prediction
        FROM assessments
        WHERE student_id = ?
        ORDER BY id DESC
    """, (student_id,))

    history = cursor.fetchall()

    conn.close()

    return history