import requests
import json
import os

PATIENT_URL = "http://hackathon.siim.org/fhir/Patient"
APPOINTMENT_URL = "http://hackathon.siim.org/fhir/Appointment"
API_ENDPOINT = "http://hackathon.siim.org/fhir/Patient"
API_KEY = "d5e7be37-a348-4669-b024-6bd2005c1292"
HEADERS = {'content-type' : 'application/json', 'apikey' : API_KEY}

def getPatientResourceByField(field, value, url=PATIENT_URL, headers=HEADERS):
    data = {'Accept' : 'application/json'}
    url += ("/?" + field + "=" + value)
    response = requests.get(url=url, headers=headers)
    
    return response.json()

def getNameFromPatient(patient_info):
    # put this in try block, there's liable to be times where it won't work
    return patient_info['entry'][0]['resource']['name'][0]['given'][0]

def getIdFromPatient(patient_info):
    return patient_info['id']

def postAppointment(patient_id, name, county, time, day, url=APPOINTMENT_URL):

    # Put County name in description
    payload = str("{\"resourceType\": \"Appointment\",\r\n \"id\": \"examp" + 
            "le\",\r\n \"status\": \"booked\",\r\n \"description\": \"Covid-19 Immunization, " +
            str(county) + "\",\r\n \"start\": \"" + str(getDateTime(time,day)) + "\",\r\n \"c" +
            "reated\": \"2020-12-10\",\r\n \"participant\": [{\"actor\": {\"reference\": \"Patient/" +
            str(patient_id) + "\",\r\n    \"display\": \"" + str(name) + "\"},\r\n   \"req" +
            "uired\": \"required\",\r\n   \"status\": \"accepted\"}]}")

    response = requests.request("POST", url, headers=HEADERS, data=payload)

    return payload

# Everything down here is real bad, don't look at it
def getAppointments(printable=True):

    response = requests.request("GET", APPOINTMENT_URL, headers=HEADERS)

    appts_json = response.json()

    appts_info = []

    days = {0 : 'Monday',
            1 : 'Tuesday',
            2 : 'Wednesday' ,
            3 : 'Thursday',
            4 : 'Friday'}

    if appts_json['entry'] == []:
        return appts_json

    # Catch case of no appointments
    for appt in appts_json['entry']:
        if printable:
            appts_info.append('Name : ' + str(appt['resource']['participant'][0]['actor']['display']) +
                            ', County : ' + str(appt['resource']['description'][23:]) +
                            ', Day : ' + str(days[int(appt['resource']['start'][9])]) + 
                            ', Time : ' + str(appt['resource']['start'][11:16]))
        else:
            appts_info.append([appt['resource']['participant'][0]['actor']['display'],
                                appt['resource']['description'][23:],
                                days[int(appt['resource']['start'][9])],
                                appt['resource']['start'][11:16]])

    return appts_info

def getDateTime(time, day):

    if day == 'Monday':
        return ('2020-12-10T' + str(time) + ':00Z')
    if day == 'Tuesday':
        return ('2020-12-11T' + str(time) + ':00Z')
    if day == 'Wednesday':
        return ('2020-12-12T' + str(time) + ':00Z')
    if day == 'Thursday':
        return ('2020-12-13T' + str(time) + ':00Z')
    if day == 'Friday':
        return ('2020-12-14T' + str(time) + ':00Z')

def getOpenAppointments(day):

    response = requests.request("GET", APPOINTMENT_URL, headers=HEADERS)
    json_appts = response.json()

    filled_appts = []

    days = {'Monday' : 0,
            'Tuesday' : 1,
            'Wednesday' : 2,
            'Thursday' : 3,
            'Friday' : 4}

    times = ['07:00', '07:30', '08:00', '08:30', '09:00',
                '09:30', '10:00', '10:30', '11:00', '11:30',
                '12:00', '12:30', '13:00', '13:30', '14:00',
                '14:30', '15:00', '15:30', '16:00', '16:30',
                '17:00', '17:30']
    
    # Catch case where there are no appointments, among potential others
    try:
        for entry in json_appts['entry']:
            appt_datetime = entry['resource']['start']

            if int(appt_datetime[9]) == int(days[day]):
                filled_appts.append(appt_datetime[11:16])

    except:
        return times

    for appt in filled_appts:
        times.remove(appt)
    
    return times