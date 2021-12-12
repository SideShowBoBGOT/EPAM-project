"""
Module contains class Employees for DB.

Classes:
    Employees(db.Model)
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from application import db


class Employees(db.Model):
    """
    Class is descendant of db.Model.
    It creates table Employees in db.
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id
