"""
Module manages database schema changes.
Functions:
    avg_salaries(departments, employees)
    find_emp(from_date, to_date)
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from models.employees import Employees


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


def find_emp(from_date, to_date):
    """
    Function finding employee between a certain period of time
    :param from_date: beginning of the period
    :param to_date: end of the period
    :return: if no errors sorted employees,
            else all employees
    """
    sorted_employees = []
    for emp in Employees.query.all():
        if from_date <= emp.birth_date <= to_date:
            sorted_employees.append(emp)
    return sorted_employees
