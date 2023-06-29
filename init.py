from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('postgresql+psycopg2://postgres:markspassword@localhost:5432/postgres')
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250))
    students = relationship('Student', backref='group')

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250))
    group_id = Column(Integer(), ForeignKey('groups.id'))
    marks = relationship('Mark', backref='student')

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250))
    subjects = relationship('Subject', backref='teacher')

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer(), primary_key=True)
    name = Column(String(250))
    teacher_id = Column(Integer(), ForeignKey('teachers.id'))
    marks = relationship('Mark', backref='subject')

class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer(), primary_key=True)
    student_id = Column(Integer(), ForeignKey("students.id"))
    subject_id = Column(Integer(), ForeignKey("subjects.id"))
    mark = Column(Integer())
    mark_date = Column(Date())


Base.metadata.create_all(engine)
Base.metadata.bind = engine
