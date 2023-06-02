from flask import Flask, request, jsonify
from models import db, students_table, marks_table
from urllib.parse import quote_plus
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:%s@localhost/stud'% quote_plus('vinomaddy@27')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/api/student/add/', methods=['POST'])
def add_student():
    roll_number = request.json['roll_number']
    name = request.json['name']
    dob = request.json['dob']
    student = students_table(roll_no=roll_number, name=name, dob=dob)
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'student added successfully'})

@app.route('/api/student/<int:pk>/', methods=['GET'])
def get_student(pk):
    student = students_table.query.get(pk)
    if not student:
        return jsonify({'message': 'student not found'})
    student_data = {
        'id': student.id,
        'roll_number': student.roll_no,
        'name': student.name,
        'dob': student.dob.strftime('%Y-%m-%d')
    }
    return jsonify(student_data)

@app.route('/api/students/', methods=['GET'])
def all_students():
    stud = students_table.query.all() 
    result = []
    for student in stud:
        student_data = {}
        student_data['id'] = student.id
        student_data['roll_number'] = student.roll_no
        student_data['name'] = student.name
        student_data['dob'] = student.dob.strftime('%Y-%m-%d')
        result.append(student_data)
    return jsonify(result)

@app.route('/api/student/<int:pk>/add-mark/', methods= ['POST'])
def add_marks(pk):
    marks = request.json['marks'] 
    stud = marks_table(marks= marks, student_id=pk)
    db.session.add(stud)
    db.session.commit()
    return jsonify({'message': 'student marks added successfully'})


@app.route('/api/student/<int:pk>/mark/', methods=['GET'])
def get_student_marks(pk):
    student = students_table.query.get(pk)
    if not student:
        return jsonify({'message': 'student not found'})
    marks = marks_table.query.filter_by(student_id=student.id).all()
    marks_data = []
    for mark in marks:
        mark_data = {
            'id': mark.id,
            'marks': mark.marks
        }
        marks_data.append(mark_data)
    return jsonify({'student_id': student.id, 'marks': marks_data})

@app.route('/api/student/results/', methods=['GET'])
def get_results():
    studen = students_table.query.all()
    result = {
        'S grade': [],
        'A grade': [],
        'B grade': [],
        'C grade': [],
        'D grade': [],
        'E grade': [],
        'F grade': []
    }
    pass_count = 0
    total_students = len(studen)
    for student in studen:
        marks = marks_table.query.filter_by(student_id=student.id).first()
        if marks:
            if 91 <= marks.marks <= 100:
                result['S grade'].append(student.id)
            elif 81 <= marks.marks <= 90:
                result['A grade'].append(student.id)
            elif 71 <= marks.marks <= 80:
                result['B grade'].append(student.id)
            elif 61 <= marks.marks <= 70:
                result['C grade'].append(student.id)
            elif 51 <= marks.marks <= 60:
                result['D grade'].append(student.id)
            elif 50 <= marks.marks <= 55:
                result['E grade'].append(student.id)
            elif marks.marks < 50:
                result['F grade'].append(student.id)
                pass_count -= 1
            pass_count += 1

    pass_percentage = (pass_count / total_students) * 100
    result['Pass Percentage'] = pass_percentage
    return jsonify(result)

with app.app_context():
    if __name__ == '__main__':
        app.run(debug=True)
        db.create_all()