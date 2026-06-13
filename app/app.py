import os
import datetime
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure Database - fallback to SQLite if PostgreSQL URL is not provided (for local testing)
# In production/k8s, DATABASE_URL should be set to: postgresql://user:password@postgres-service:5432/attendance_db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///attendance.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), nullable=False)
    attendance_percentage = db.Column(db.String(50), nullable=True, default='N/A')
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Ensure tables are created
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_name = request.form['student_name']
        student_id = request.form['student_id']
        attendance_percentage = request.form.get('attendance_percentage', 'N/A')
        
        if student_name and student_id:
            new_record = Attendance(
                student_name=student_name,
                student_id=student_id,
                attendance_percentage=attendance_percentage
            )
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('index'))
            
    records = Attendance.query.order_by(Attendance.timestamp.desc()).all()
    return render_template('index.html', records=records)

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
