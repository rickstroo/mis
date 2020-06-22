from flask import Flask, render_template, request, redirect, url_for, abort, make_response
from fhir_utility import *

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/getUser', methods=['POST', 'GET'])
def getUser():

    if request.method == 'POST':

        user_id = request.form['patient_id']
        patient_info = getPatientResourceByField('_id', user_id)

        patient_name = getNameFromPatient(patient_info)
        patient_id = getIdFromPatient(patient_info)

        resp = make_response(redirect('/makeAppointment'))
        resp.set_cookie('patient_name', patient_name)
        resp.set_cookie('patient_id', patient_id)
        return resp

    else:
        return render_template('getUser.html')

@app.route('/makeAppointment', methods=['POST', 'GET'])
def makeAppointment():

    if request.method == 'POST':

        resp = make_response(redirect('/madeAppointment'))

        day = request.form['day']
        time = request.form['time']
        resp.set_cookie('day', day)
        resp.set_cookie('time', time)

        return resp

    else:
        name = request.cookies.get('patient_name')

        # need function in fhir_utility to find available days/times by searching
        # appointments in fhir
        times = ['7:00AM', '7:30AM', '8:00AM', '8:30AM', '9:00AM',
                '9:30AM', '10:00AM', '10:30AM', '11:00AM', '11:30AM',
                '12:00PM', '12:30PM', '1:00PM', '1:30PM', '2:00PM',
                '2:30PM', '3:00PM', '3:30PM', '4:00PM', '4:30PM',
                '5:00PM', '5:30PM']
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        return render_template('makeAppointment.html', name=name,
                                times=times, days=days)

@app.route('/madeAppointment')
def madeAppointment():

    # Need function in fhir_utility to post this appointment to fhir
    name = request.cookies.get('patient_name')
    day = request.cookies.get('day')
    time = request.cookies.get('time')

    # Probably want an actual html page for this
    return('Appointment for ' + str(name) + ' on ' + str(day) + 
            ' at ' + str(time) + '\nThank you. Test')

if __name__ == "__main__":
    app.run(debug=True)