from sqlalchemy import func, desc
from init import session, Group, Student, Teacher, Subject, Mark

def select_1():
    return session.query(Student.name, func.round(func.avg(Mark.mark), 2).label('average_mark'))\
        .select_from(Mark).join(Student).group_by(Student.id).order_by(desc('average_mark')).limit(5).all()

def select_2(subject):
    return session.query(Student.name, func.round(func.avg(Mark.mark), 2).label('average_mark'))\
        .select_from(Mark).join(Student).join(Subject).group_by(Student.id)\
        .filter(Subject.name==subject).order_by(desc('average_mark')).limit(1).all()

def select_3(subject):
    return session.query(Group.name, func.round(func.avg(Mark.mark), 2).label('average_mark'))\
        .select_from(Mark).join(Student).join(Group).join(Subject).group_by(Group.id)\
        .filter(Subject.name==subject).order_by(desc('average_mark')).all()

def select_4():
    return session.query(func.round(func.avg(Mark.mark), 2)).select_from(Mark).all()

def select_5(teacher):
    return session.query(Subject.name).select_from(Subject).join(Teacher)\
        .group_by(Subject.id).filter(Teacher.name == teacher).all()

def select_6(group):
    return session.query(Student.name).select_from(Student).join(Group)\
        .group_by(Student.id).filter(Group.name == group).all()

def select_7(group, subject):
    return session.query(Student.name, Mark.mark).select_from(Mark).join(Student)\
        .join(Group).join(Subject).group_by(Mark.id, Student.name)\
        .filter(Group.name==group, Subject.name==subject).all()

def select_8(teacher):
    return session.query(func.round(func.avg(Mark.mark) ,2)).select_from(Mark).join(Subject)\
        .join(Teacher).group_by(Teacher.id).filter(Teacher.name==teacher).all()

def select_9(student):
    return session.query(Subject.name).select_from(Mark).join(Subject).join(Student)\
        .group_by(Subject.id).filter(Student.name == student).all()

def select_10(student, teacher):
    return session.query(Subject.name).select_from(Mark).join(Subject).join(Student)\
        .join(Teacher).group_by(Subject.id).filter(Student.name == student, Teacher.name == teacher).all()