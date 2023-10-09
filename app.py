from flask import Flask, request, render_template
from models import db, Appointment
from datetime import datetime  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/schedule', methods=['POST'])
def schedule_appointment():
    name = request.form.get('name')
    email = request.form.get('email')
    date_str = request.form.get('date')
    time_str = request.form.get('time')
    
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    time = datetime.strptime(time_str, '%H:%M').time()
    
    appointment = Appointment(name=name, email=email, date=date, time=time)
    db.session.add(appointment)
    db.session.commit()
    
    return "Appointment scheduled successfully!"

@app.route('/delete/<int:id>', methods=['GET'])
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return f"Appointment {id} deleted successfully!"
    else:
        return f"Appointment {id} not found."

@app.route('/')
def login():
    return render_template ('schedule_form.html')
    

@app.route('/appointments')
def view_appointments():
    appointments = Appointment.query.all()
    return render_template('appointment_list.html', appointments=appointments)
if __name__ == '__main__':
    app.run(debug=True)

