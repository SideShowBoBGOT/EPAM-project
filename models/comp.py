try:
    from project.proj import db
except:
    from __main__ import db



class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.id
