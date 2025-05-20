from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from import_service import import_courses_from_excel

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    professor = Column(String, nullable=False)
    ects = Column(Float, nullable=False)
    study_hours = Column(Float, nullable=True)

# Database setup
DATABASE_URL = "sqlite:///academic_weapon.db"  # If the file does not exist, SQLAlchemy will create it automatically.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    file_path = "ceid_courses.xlsx"  
    import_courses_from_excel(file_path)

