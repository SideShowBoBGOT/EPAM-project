from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql/company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from project.models.comp import Employees, Departments
from project.service.db_methods import avg_salaries, add_emp, add_dnt, find_emp, change_emp, change_dnt, del_dnt, \
    del_emp




@app.route('/')
def index():
    """
    Function returning the template of the main page
    :return: the template of the main page
    """
    return render_template('index.html')


@app.route('/departments', methods=['POST', 'GET'])
def departments_page():
    """
    Function working on departments page:
        1) adding new departments if method "POST" received
        2) showing the table of the departments
    :return: the template of the departments page
    """
    departments = Departments.query.all()
    employees = Employees.query.all()
    dnt_salary = avg_salaries(departments, employees)
    if request.method == 'POST':
        add_dnt()
        return redirect('/departments')
    return render_template('departments.html', departments=departments, dnt_salary=dnt_salary)


@app.route('/employees', methods=['POST', 'GET'])
def employees_page():
    """
    Function working on employees page:
        1) adding new employees
        2) Finding employees by dates of birth
    :return: the template of the employees page
    """

    departments = Departments.query.all()
    employees = Employees.query.all()
    if request.method == 'POST':
        if 'department' in request.form.keys() and 'name' in request.form.keys() \
                and 'birth_date' in request.form.keys() and 'salary' in request.form.keys():
            add_emp()
            return redirect('/employees')
        elif 'From' in request.form.keys() and 'To' in request.form.keys():
            departments, employees = find_emp(departments, employees)
            return render_template('employees.html', employees=employees, departments=departments)
    return render_template('employees.html', employees=employees, departments=departments)


@app.route('/departments/<int:id>/del')
def delete_dnt(id):
    """
    Function deleting specific department by its id
    :param id: id of the specific department a user wants to delete
    :return: redirects user to the departments page
    """
    employees = Employees.query.all()
    del_dnt(employees, id)
    return redirect('/departments')


@app.route('/employees/<int:id>/del')
def delete_emp(id):
    """
    Function deleting specific employee by its id
    :param id: id of the specific employee a user wants to delete
    :return: redirects to the employees page
    """
    del_emp(id)
    return redirect('/employees')


@app.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
def edit_emp(id):
    """
    Function editing information about specific employee
    :param id: id of the specific employee a user wants to change information about
    :return: return template of the departments page or redirects to employees page
    """
    print()
    departments = Departments.query.all()
    employees = Employees.query.all()
    if request.method == 'POST':
        if 'department' in request.form.keys() and 'name' in request.form.keys() \
                and 'birth_date' in request.form.keys() and 'salary' in request.form.keys():
            change_emp(id)
            return redirect('/employees')

    return render_template('employees.html', id=id, departments=departments, employees=employees)


@app.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
def edit_dnt(id):
    """
    Function editing information about specific departments
    :param id:  id of the specific department
    :return: the template of the employees page or redirects to departments
    """
    departments = Departments.query.all()
    employees = Employees.query.all()
    dnt_salary = avg_salaries(departments, employees)
    if request.method == 'POST':
        if 'department' in request.form.keys():
            change_dnt(employees, id)
            return redirect('/departments')
    return render_template('departments.html', id=id, departments=departments, dnt_salary=dnt_salary)


if __name__ == '__main__':
    app.run(debug=True)
