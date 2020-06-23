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

        resp = make_response(redirect('/getCounty'))
        resp.set_cookie('patient_name', patient_name)
        resp.set_cookie('patient_id', patient_id)
        return resp

    else:
        return render_template('getUser.html')

@app.route('/getCounty', methods=['GET', 'POST'])
def getCounty():

    if request.method == 'POST':
        
        resp = make_response(redirect('/getDay'))
        county = request.form['county']
        resp.set_cookie('county', county)

        return resp
    else:
        name = request.cookies.get('patient_name')

        counties = ['Adams', 'Ashland', 'Barron', 'Bayfield', 'Brown', 'Buffalo', 'Burnett',
                    'Calumet', 'Chippewa', 'Clark', 'Columbia', 'Crawford', 'Dane', 'Dodge',
                    'Door', 'Douglas', 'Dunn', 'Eau Claire', 'Florence', 'Fond du Lac', 'Forest',
                    'Grant', ' Green', 'Green Lake', 'Iowa', 'Iron', 'Jackson', 'Jefferson', 
                    'Juneau', 'Kenosha', 'Kewaunee', 'La Crosse', 'Lafayette', 'Langlade',
                    'Lincoln', ' Manitowoc', 'Marathon', ' Marinette', 'Marquette', 'Menonminee',
                    'Milwaukee', 'Monroe', 'Oconto', 'Oneida', 'Outagamie', 'Ozaukee', 'Pepin',
                    'Pierce', 'Polk', 'Portage', 'Price', 'Racine', 'Richland', 'Rock', 'Rusk',
                    'Sauk', 'Sawyer', 'Shawano', 'Sheboygan', 'St. Croix', 'Taylor', 'Trempealeau',
                    'Vernon', 'Vilas', 'Walworth', 'Washburn', 'Washinton', 'Waukesha', 'Waupaca',
                    'Waushara', 'Winnebago', 'Wood']

        return render_template('getCounty.html', name=name, counties=counties)

@app.route('/getDay', methods=['GET', 'POST'])
def getDay():
    if request.method == 'POST':
        
        resp = make_response(redirect('/getTime'))
        day = request.form['day']
        resp.set_cookie('day', day)

        return resp
    else:
        name = request.cookies.get('patient_name')

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

        return render_template('getDay.html', name=name, days=days)

@app.route('/getTime', methods=['GET', 'POST'])
def getTime():
    if request.method == 'POST':
        
        resp = make_response(redirect('/madeAppointment'))
        time = request.form['time']
        resp.set_cookie('time', time)

        return resp
    else:
        name = request.cookies.get('patient_name')
        day = request.cookies.get('day')

        times = getOpenAppointments(day)

        return render_template('getTime.html', name=name, times=times)

@app.route('/madeAppointment')
def madeAppointment():

    patient_id = request.cookies.get('patient_id')
    county = request.cookies.get('county')
    name = request.cookies.get('patient_name')
    day = request.cookies.get('day')
    time = request.cookies.get('time')

    postAppointment(patient_id, name, county, time, day)

    # Probably want an actual html page for this
    return('Appointment for ' + str(name) + ' in ' + str(county) + ' on ' + str(day) + 
            ' at ' + str(time) + '. You are preventing ' + str(getInfectionsPrevented(county)) + 
            ' infections per day(?). Thank you.')

@app.route('/viewAppointments')
def viewAppointments():

    appts = getAppointments()
    return render_template('viewAppointments.html', appts=appts)


if __name__ == "__main__":
    app.run(debug=True)