"""
Module contains functions to work with DB( CRUD operations ).

Functions:
    add_user(login, password)
    add_emp(name, department, salary, birth_date)
    add_dnt(department)
    change_emp(id, name, department, salary, birth_date)
    change_user(id, login, password)
    change_dnt(id, department)
    del_user(id)
    del_dnt(id)
    del_emp(id)
"""
from .service_employees import add_emp, change_emp, del_emp
from .service_departments import add_dnt, change_dnt, del_dnt
from .service_user import add_user, change_user, del_user







