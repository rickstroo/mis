import requests
import json
import os

PATIENT_URL = "http://hackathon.siim.org/fhir/Patient"
APPOINTMENT_URL = "http://hackathon.siim.org/fhir/Appointment"
API_ENDPOINT = "http://hackathon.siim.org/fhir/Patient"
API_KEY = "d5e7be37-a348-4669-b024-6bd2005c1292"
HEADERS = {'content-type' : 'application/json', 'apikey' : API_KEY}

# Refer to jupyter notebook for explanation
DELTA_DICT = {'Adams': 0.032165097394510025,
                'Ashland': 0.0665122199592668,
                'Barron': 0.03311215090231546,
                'Bayfield': 0.09857657417289219,
                'Brown': 0.05980365963803776,
                'Buffalo': 0.05100934153565733,
                'Burnett': 0.053863546991742034,
                'Calumet': 0.011996543392187722,
                'Chippewa': 0.025286415711947625,
                'Clark': 0.05524532486735673,
                'Columbia': 0.02327622120376135,
                'Crawford': 0.05716336211353529,
                'Dane': 0.02641650373342455,
                'Dodge': 0.06650489123830358,
                'Door': 0.03147153686358831,
                'Douglas': 0.033210863433409586,
                'Dunn': 0.02491885321665654,
                'Eau Claire': 0.01638550941344388,
                'Florence': 0.112566290062255,
                'Fond du Lac': 0.026372599325612072,
                'Forest': 0.26003957363051683,
                'Grant': 0.05190021890589149,
                'Green': 0.02947149547803618,
                'Green Lake': 0.022355813829503645,
                'Iowa': 0.04304713519616144,
                'Iron': 0.13266316710411197,
                'Jackson': 0.06568277133965227,
                'Jefferson': 0.017243841281646195,
                'Juneau': 0.034835383625421115,
                'Kenosha': 0.02416917833703846,
                'Kewaunee': 0.025795546823837587,
                'La Crosse': 0.02074196011879507,
                'Lafayette': 0.06539484477279517,
                'Langlade': 0.06814652473387602,
                'Lincoln': 0.035508519462798045,
                'Manitowoc': 0.013860862061080398,
                'Marathon': 0.02695582564466525,
                'Marinette': 0.05424620893081804,
                'Marquette': 0.04119484447951602,
                'Menominee': 0.07809783795588557,
                'Milwaukee': 0.0264432592436206,
                'Monroe': 0.03431392026724099,
                'Oconto': 0.04026270264687563,
                'Oneida': 0.04117760100982622,
                'Outagamie': 0.018252082570108866,
                'Ozaukee': 0.007456543807638005,
                'Pepin': 0.031944367942715504,
                'Pierce': 0.02413437732855803,
                'Polk': 0.035420720201158044,
                'Portage': 0.03754340566511883,
                'Price': 0.09298591549295776,
                'Racine': 0.038638668145328355,
                'Richland': 0.03580693637851972,
                'Rock': 0.04136376598003035,
                'Rusk': 0.08856985475569346,
                'Sauk': 0.024623041120147862,
                'Sawyer': 0.09875023998603717,
                'Shawano': 0.0371805356230548,
                'Sheboygan': 0.012961529585287238,
                'St. Croix': 0.019569124597890356,
                'Taylor': 0.061574825253347565,
                'Trempealeau': 0.06191045587336097,
                'Vernon': 0.032424793550924105,
                'Vilas': 0.04407807056813679,
                'Walworth': 0.036069914800397354,
                'Washburn': 0.050806934795079355,
                'Washington': 0.011714204144240936,
                'Waukesha': 0.014374429700059163,
                'Waupaca': 0.031491297980976066,
                'Waushara': 0.04265529109305026,
                'Winnebago': 0.020189836645470277,
                'Wood': 0.015530130504799731}

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

def getInfectionsPrevented(county):
    return (DELTA_DICT[county])