"""
Module contains functions to work with Employees DB( CRUD operations ).

Functions:
    add_emp(name, department, salary, birth_date)
    change_emp(id, name, department, salary, birth_date)
    del_emp(id)
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from f_logger import logger
from application import db
from models.employees import Employees


def add_emp(name, department, salary, birth_date):
    """
    Function adding new employee to specific department
   :param name: employee`s name
   :param department: employee`s department
   :param salary: employee`s salary
   :param birth_date: employee`s birth_date
   :return: None
    """
    try:
        emp = Employees(name=name, department=department, birth_date=birth_date, salary=salary)
        db.session.add(emp)
        db.session.commit()
    except:
        logger.warning('DB can`t add employee')
    return None


def change_emp(id, name, department, salary, birth_date):
    """
    Function changing employee`s information
    :param id: id of th employee
    :param name: new employee`s name
    :param department: new employee`s department
    :param salary: new employee`s salary
    :param birth_date: new employee`s birth_date
    :return: None
    """
    try:
        emp = Employees.query.get(id)
        emp.name = name
        emp.department = department
        emp.salary = salary
        emp.birth_date = birth_date

        db.session.commit()
    except:
        logger.warning('DB can`t change employee`s data')
    return None


def del_emp(id):
    """
    Function deleting employee from db
    :param id: if of the employee
    :return: None
    """
    emp = Employees.query.get(id)
    try:
        db.session.delete(emp)
        db.session.commit()
    except:
        logger.warning('DB can`t delete employee')
    return None
