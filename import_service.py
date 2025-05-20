import pandas as pd
from sqlalchemy.orm import Session
from database import Course, SessionLocal

def import_courses_from_excel(file_path):
    """Import courses from an Excel file into the database."""
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Ensure the required columns exist
    required_columns = ['course_name', 'department', 'semester', 'professor', 'ects', 'study_hours']
    if not all(column in df.columns for column in required_columns):
        raise ValueError(f"The Excel file must contain the following columns: {', '.join(required_columns)}")

    # Open a database session
    session = SessionLocal()
    try:
        # Iterate through the rows and add them to the database
        for _, row in df.iterrows():
            course = Course(
                course_name=row['course_name'],
                department=row['department'],
                semester=int(row['semester']),
                professor=row['professor'],
                ects=float(row['ects']),
                study_hours=float(row['study_hours'])
            )
            session.add(course)
        session.commit()
        print("Courses imported successfully!")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()