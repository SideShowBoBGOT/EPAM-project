from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models.comp import Employees, Departments

def avg_salaries(departments, employees):
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
        else:
            avg_salary = 'No employees'
        dnt_salary[dnt_name] = round(avg_salary, 3)
    return dnt_salary

def add_employee(departments, employees):
    try:
        name = request.form['name']
        department = request.form['department']
        salary = int(request.form['salary'])
        birth_date = datetime.datetime.strptime(request.form['birth_date'], '%Y-%m-%d')

        emp = Employees(name=name, department=department, birth_date=birth_date, salary=salary)

        try:
            db.session.add(emp)
            db.session.commit()
            departments = Departments.query.all()
            employees = Employees.query.all()
            return render_template('employees-general.html', employees=employees, departments=departments)
        except:
            'Error'
            return render_template('employees-general.html', employees=employees, departments=departments)
    except:
        return render_template('employees-general.html', employees=employees, departments=departments)
def change_emp(departments, employees, id):
    try:
        emp = Employees.query.get_or_404(id)
        emp.name = request.form['name']
        emp.department = request.form['department']
        emp.salary = int(request.form['salary'])
        emp.birth_date = datetime.datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
        try:
            db.session.commit()
            return render_template('employees-general.html', employees=employees, departments=departments)
        except:
            return render_template('employees-general.html', employees=employees, departments=departments)
    except:
        return render_template('employees-general.html', employees=employees, departments=departments)
def find_employee(departments, employees):
    try:
        from_date = datetime.datetime.strptime(request.form['From'], '%Y-%m-%d').date()
        to_date = datetime.datetime.strptime(request.form['To'], '%Y-%m-%d').date()
        sorted_employees = []
        if to_date >= from_date:
            for emp in employees:
                if from_date <= emp.birth_date <= to_date:
                    sorted_employees.append(emp)
            return render_template('employees-general.html', employees=sorted_employees, departments=departments)
        else:
            error = 'Choose correct dates'
            return render_template('employees-general.html', employees=employees, departments=departments)
    except:
        return render_template('employees-general.html', employees=employees, departments=departments)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/departments', methods=['POST', 'GET'])
def departments_page():
    departments = Departments.query.all()
    employees = Employees.query.all()
    dnt_salary = avg_salaries(departments, employees)
    if request.method == 'POST':
        department = request.form['department']
        if department:
            dnt = Departments(department=department)
            try:
                db.session.add(dnt)
                db.session.commit()
                departments = Departments.query.all()
                dnt_salary = avg_salaries(departments, employees)
                return render_template('departments.html', departments=departments, dnt_salary=dnt_salary)
            except:
                'Error'
                return render_template('departments.html', departments=departments, dnt_salary=dnt_salary)
        else:
            return render_template('departments.html', departments=departments, dnt_salary=dnt_salary)
    return render_template('departments.html', departments=departments, dnt_salary=dnt_salary)

@app.route('/employees', methods=['POST', 'GET'])
def employees_page():
    departments = Departments.query.all()
    employees = Employees.query.all()
    if request.method == 'POST':
        if 'department' in request.form.keys() and 'name' in request.form.keys()\
        and 'birth_date' in request.form.keys() and 'salary' in request.form.keys():
            templ = add_employee(departments, employees)
            return templ
        elif 'From' in request.form.keys() and 'To' in request.form.keys():
            templ = find_employee(departments, employees)
            return templ
        else:
            return render_template('employees-general.html', employees=employees, departments=departments)
    else:
        departments = Departments.query.all()
        employees = Employees.query.all()
        return render_template('employees-general.html', employees=employees, departments=departments)
@app.route('/departments/<int:id>/del')
def delete_dnt(id):
    employees = Employees.query.all()
    dnt = Departments.query.get_or_404(id)
    try:
        db.session.delete(dnt)
        for emp in employees:
            if emp.department == dnt.department:
                db.session.delete(emp)
        db.session.commit()
        return redirect('/departments')
    except:
        return redirect('/departments')
@app.route('/employees/<int:id>/del')
def delete_emp(id):
    emp = Employees.query.get_or_404(id)
    try:
        db.session.delete(emp)
        db.session.commit()
        return redirect('/employees')
    except:
        return redirect('/employees')
@app.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
def edit_emp(id):
    departments = Departments.query.all()
    employees = Employees.query.all()
    if request.method == 'POST':
        if 'department' in request.form.keys() and 'name' in request.form.keys() \
                and 'birth_date' in request.form.keys() and 'salary' in request.form.keys():
            templ = change_emp(departments, employees, id)
            return templ
        else:
            return render_template('employees-general.html', id=id, departments=departments, employees=employees)
    return render_template('employees-general.html', id=id, departments=departments, employees=employees)
if __name__ == '__main__':
    app.run(debug=True)
