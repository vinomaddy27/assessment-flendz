from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class students_table(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    roll_no = db.Column(db.String(50), unique=True, nullable =False)
    name = db.Column(db.String(255), nullable = False )
    dob = db.Column(db.Date , nullable = False)
    marks = db.relationship('marks_table', backref='students_table', lazy=True)

    def  __init__(self, dob, name, roll_no):
        self.dob = dob
        self.name = name
        self.roll_no = roll_no
    

class marks_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students_table.id'), nullable=False)
    marks = db.Column(db.Integer)

    def __init__(self, student_id, marks):
        self.student_id = student_id
        self.marks = marks
