from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_1():
    """ Знайти 5 студентів із найбільшим середнім балом з усіх предметів """
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result


def select_2(discipline_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета """
    r = session.query(Discipline.name,
                      Student.fullname,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Student.id, Discipline.name) \
        .order_by(desc('avg_grade')) \
        .limit(1).all()
    return r


def select_3(discipline_id):
    """Знайти середній бал у групах з певного предмета """
    r = session.query(Discipline.name,
                      Group.name,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Group) \
        .join(Discipline) \
        .filter(Discipline.id == discipline_id) \
        .group_by(Group.id, Discipline.name) \
        .order_by(Group.id) \
        .all()
    return r


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок) """
    r = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')).select_from(Grade).all()
    return r


def select_5():
    """Знайти які курси читає певний викладач """
    r = session.query(Teacher.fullname,
                      Discipline.name,
                      ) \
        .select_from(Discipline) \
        .join(Teacher) \
        .order_by(Teacher.fullname) \
        .all()
    return r


def select_6(group_id):
    """Знайти список студентів у певній групі """
    r = session.query(Group.name,
                      Student.fullname,
                      ) \
        .select_from(Student) \
        .join(Group) \
        .filter(Group.id == group_id) \
        .order_by(Student.fullname) \
        .all()
    return r


def select_7(group_id, discipline_id):
    """Знайти оцінки студентів у окремій групі з певного предмета """
    r = session.query(Student.fullname,
                      Group.name,
                      Discipline.name,
                      Grade.grade,
                      Grade.date_of
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group) \
        .filter(and_(Group.id == group_id), (Discipline.id == discipline_id)) \
        .order_by(Student.fullname) \
        .all()
    return r


def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів """
    r = session.query(Teacher.fullname,
                      Discipline.name,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(Teacher.id == teacher_id) \
        .group_by(Discipline.name, Teacher.fullname) \
        .all()
    return r


def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент """
    r = session.query(Student.fullname,
                      Discipline.name,
                      Grade.date_of
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .filter(Student.id == student_id) \
        .order_by(Discipline.name) \
        .all()
    return r


def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач """
    r = session.query(Discipline.name,
                      Student.fullname,
                      Teacher.fullname,
                      Grade.date_of
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(and_(Student.id == student_id), (Teacher.id == teacher_id)) \
        .order_by(Discipline.name) \
        .all()
    return r


def select_11(student_id, teacher_id):
    """Середній бал, який певний викладач ставить певному студентові """
    r = session.query(Teacher.fullname,
                      Student.fullname,
                      Discipline.name,
                      func.round(func.avg(Grade.grade), 2).label('avg_grade')
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Teacher) \
        .filter(and_(Student.id == student_id), (Teacher.id == teacher_id)) \
        .group_by(Discipline.name, Teacher.fullname, Student.fullname) \
        .all()
    return r


def select_12(discipline_id, group_id):
    subquery = (select(Grade.date_of).join(Student).join(Group).where(
        and_(Grade.discipline_id == discipline_id, Group.id == group_id)
    ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    r = session.query(Discipline.name,
                      Student.fullname,
                      Group.name,
                      Grade.date_of,
                      Grade.grade
                      ) \
        .select_from(Grade) \
        .join(Student) \
        .join(Discipline) \
        .join(Group)\
        .filter(and_(Discipline.id == discipline_id, Group.id == group_id, Grade.date_of == subquery)) \
        .order_by(desc(Grade.date_of)) \
        .all()
    return r


if __name__ == '__main__':
    print(select_1())
    print(select_2(1))
    print(select_3(3))
    print(select_4())
    print(select_5())
    print(select_6(2))
    print(select_7(1, 2))
    print(select_8(3))
    print(select_9(2))
    print(select_10(2, 3))
    print(select_11(2, 1))
    print(select_12(1, 2))
