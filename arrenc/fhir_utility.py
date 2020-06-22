import requests

URL = "http://hackathon.siim.org/fhir/Patient"
API_ENDPOINT = "http://hackathon.siim.org/fhir/Patient"
API_KEY = "d5e7be37-a348-4669-b024-6bd2005c1292"
HEADERS = {'content-type' : 'application/json', 'apikey' : API_KEY}

def getPatientResourceByField(field, value, url=URL, headers=HEADERS):
    data = {'Accept' : 'application/json'}
    url += ("/?" + field + "=" + value)
    response = requests.get(url=url, headers=headers)
    
    return response.json()

def getNameFromPatient(patient_info):
    # put this in try block, there's liable to be times where it won't work
    return patient_info['entry'][0]['resource']['name'][0]['given'][0]

def getIdFromPatient(patient_info):
    return patient_info['id']