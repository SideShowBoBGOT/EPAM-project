"""
Module contains functions to work with Departments DB( CRUD operations ).

Functions:
    add_dnt(department)
    change_dnt(id, department)
    del_dnt(id)
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from f_logger import logger
from application import db
from models.employees import Employees
from models.departments import Departments


def add_dnt(department):
    """
    Function adding new department to the db
    :param department: name of new department
    :return: None
    """
    try:
        dnt = Departments(department=department)
        db.session.add(dnt)
        db.session.commit()
    except:
        logger.warning('DB can`t add department')
    return None


def change_dnt(id, department):
    """
    Function changing information of department

    :param id: id of the department a user wants to change
    :return: None
    """
    try:
        employees = Employees.query.all()
        dnt = Departments.query.get(id)

        for emp in employees:
            if emp.department == dnt.department:
                emp.department = department
        dnt.department = department
        db.session.commit()
    except:
        logger.warning('DB can`t change department data')
    return None


def del_dnt(id):
    """
    Function deleting department from db
    :param id: if of the department
    :return: None
    """
    dnt = Departments.query.get(id)
    employees = Employees.query.all()
    try:
        db.session.delete(dnt)
        for emp in employees:
            if emp.department == dnt.department:
                db.session.delete(emp)
        db.session.commit()
    except:
        logger.warning('DB can`t delete department')
    return None
