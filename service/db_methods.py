from flask import request
import datetime

try:
    from project.proj import db, Employees, Departments
except:
    from __main__ import db, Employees, Departments


def avg_salaries(departments, employees):
    """
    Function calculating average salary of every department
    :param departments: list of departments in the db
    :param employees: list of employees in the db
    :return: dnt_salary: the dictionary of names of departments as keys and average salaries as values
    """
    dnt_salary = {}
    for dnt in departments:
        dnt_salary[dnt.department] = []
    for emp in employees:
        for dnt in departments:
            if emp.department == dnt.department:
                dnt_salary[dnt.department].append(emp.salary)
    for dnt_name in dnt_salary:
        avg_salary = None
        if dnt_salary[dnt_name]:
            avg_salary = 0
            for salary in dnt_salary[dnt_name]:
                avg_salary += salary
            avg_salary /= len(dnt_salary[dnt_name])
            dnt_salary[dnt_name] = round(avg_salary, 3)
        else:
            avg_salary = 'No employees'
            dnt_salary[dnt_name] = avg_salary

    return dnt_salary


def add_emp():
    """
    Function adding new employee to specific department
    :return: None
    """
    try:
        name = request.form['name']
        department = request.form['department']
        salary = int(request.form['salary'])
        birth_date = datetime.datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
        if salary >= 0:
            emp = Employees(name=name, department=department, birth_date=birth_date, salary=salary)

            db.session.add(emp)
            db.session.commit()
    except:
        print('Error working with db')
    return None


def add_dnt():
    """
    Function adding new department to the db
    :return: None
    """
    department = request.form['department']
    is_already_exists = False
    if department:
        for dnt in Departments.query.all():
            if dnt.department == department:
                is_already_exists = True
                break
        if not is_already_exists:
            new_dnt = Departments(department=department)
            try:
                db.session.add(new_dnt)
                db.session.commit()
            except:
                print('Error working with db')
    return None



def find_emp(departments, employees):
    """
    Function finding employee between a certain period of time
    :param departments: list of departments in the db
    :param employees: list of employees in the db
    :return: if no errors : list of employees born on certain date ,
            else: unchanged list of employees
    """
    try:
        from_date = datetime.datetime.strptime(request.form['From'], '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(request.form['To'], '%Y-%m-%d').date()
        sorted_employees = []
        if to_date >= from_date:
            for emp in employees:
                if from_date <= emp.birth_date <= to_date:
                    sorted_employees.append(emp)
            return departments, sorted_employees
        else:
            return departments, employees
    except:
        return departments, employees


def change_emp(id):
    """
    Function changing employee`s information
    :param id: id of the employee a user wants to change
    :return: None
    """
    try:
        name = request.form['name']
        department = request.form['department']
        salary = int(request.form['salary'])
        birth_date = datetime.datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
        if salary >= 0:
            emp = Employees.query.get_or_404(id)
            emp.name = name
            emp.department = department
            emp.salary = salary
            emp.birth_date = birth_date

            db.session.commit()
    except:
        print('Error working with db')
    return None

def change_dnt(employees, id):
    """
    Function changing information of department
    :param employees: list of employees in the db
    :param id: id of the department a user wants to change
    :return: None
    """

    dnt = Departments.query.get_or_404(id)
    new_name_dnt = request.form['department']
    is_already_exists = False
    if new_name_dnt:
        for d in Departments.query.all():
            if d.department == new_name_dnt and d.id != dnt.id:
                is_already_exists = True
                break
        if not is_already_exists:
            try:
                for emp in employees:
                    if emp.department == dnt.department:
                        emp.department = new_name_dnt
                dnt.department = new_name_dnt

                db.session.commit()
            except:
                print('Error working with db')
    return None

def del_dnt(employees, id):
    dnt = Departments.query.get_or_404(id)
    try:
        db.session.delete(dnt)
        for emp in employees:
            if emp.department == dnt.department:
                db.session.delete(emp)
        db.session.commit()
    except:
        print('Error working with db')
    return None

def del_emp(id):
    emp = Employees.query.get_or_404(id)
    try:
        db.session.delete(emp)
        db.session.commit()
    except:
        print('Error working with db')
    return None