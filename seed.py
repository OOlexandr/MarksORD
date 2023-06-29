from faker import Faker
from random import randint
import datetime
from multiprocessing import Process, Event, Manager
import init

fake = Faker()
n_groups = 3
groups = ['AD-101', 'AD-102', 'AD-103']
n_students = randint(30, 50)
n_subjects = 5
subjects = ["linear algebra", "calculus", "statistics", "language", "physics"]
n_teachers = randint(3, 5)
n_marks = 20

def random_date():
    end_date = datetime.date.today()
    start_date = datetime.date(end_date.year, 1, 1)
    diff = end_date - start_date
    return start_date + datetime.timedelta(days=randint(1, diff.days))

def writing_in_database(groups_prepared, students_prepared, teachers_prepared, subjects_prepared, marks_prepared, data):
    session = init.session
    groups_prepared.wait()
    for i in range(n_groups):
        g = init.Group(name=data["groups"][i])
        session.add(g)
        session.commit()
        
    students_prepared.wait()
    for i in data["students"]:
        st = init.Student(name=i[0], group_id=i[1])
        session.add(st)
        session.commit()

    teachers_prepared.wait()
    for i in data["teachers"]:
        t = init.Teacher(name=i[0])
        session.add(t)
        session.commit()

    subjects_prepared.wait()
    for i in data["subjects"]:
        sub = init.Subject(name=i[0], teacher_id=i[1])
        session.add(sub)
        session.commit()

    marks_prepared.wait()
    for i in data["marks"]:
        m = init.Mark(student_id=i[0], subject_id=i[1], mark=i[2], mark_date=i[3])
        session.add(m)
        session.commit()
        

def preparing_data(groups_prepared, students_prepared, teachers_prepared, subjects_prepared, marks_prepared, data):
    for i in range(n_groups):
        data["groups"].append(groups[i])
    groups_prepared.set()

    for i in range(n_students):
        data["students"].append((fake.name(), randint(1, n_groups)))
    students_prepared.set()

    for i in range(n_teachers):
        data["teachers"].append((fake.name(),))
    teachers_prepared.set()
    
    for i in range(n_subjects):
        data["subjects"].append((subjects[i], randint(1, n_teachers)))
    subjects_prepared.set()
    
    for s in range(1, n_students+1):
        for i in range(n_marks):
            data["marks"].append((s, randint(1, n_subjects), randint(1, 100), random_date()))
    marks_prepared.set()

def main():
    groups_prepared = Event()
    students_prepared = Event()
    teachers_prepared = Event()
    subjects_prepared = Event()
    marks_prepared = Event()

    man = Manager()
    data = man.dict()
    data["groups"] = man.list()
    data["students"] = man.list()
    data["teachers"] = man.list()
    data["subjects"] = man.list()
    data["marks"] = man.list()

    writing = Process(target=writing_in_database,
                        args=(groups_prepared, students_prepared, teachers_prepared, subjects_prepared, marks_prepared, data))
    preparing = Process(target=preparing_data,
                        args=(groups_prepared, students_prepared, teachers_prepared, subjects_prepared, marks_prepared, data))

    writing.start()
    preparing.start()

    preparing.join()
    writing.join()

if __name__ == '__main__':
    main()