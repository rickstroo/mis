from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from collections import OrderedDict
from io import StringIO
app = Flask(__name__)

wsgi_app = app.wsgi_app

url = "http://hackathon.siim.org/fhir/Patient"
urlv = "http://hackathon.siim.org/fhir/Immunization"
API_ENDPOINT = "http://hackathon.siim.org/fhir/Patient"
API_KEY = "c16ba109-3189-4c74-a013-479b1b00bfd4"
HEADERS = {'content-type': 'application/json', 'apikey': API_KEY}

full_name = {}
@app.route('/search', methods = ["GET", "POST"])
def search(): #searching for patients in FHIR server
    if request.method == "POST":
        req = request.form
        fullname = req.get("name")
        first, last = fullname.split(" ", 1)
        full_name['f'] = first
        full_name['l'] = last
        return redirect(url_for('immunization'))
    return render_template("search.html")

@app.route('/immunization', methods = ["GET", "POST"])
def immunization(): #creating Immunization Resource from user input
    response = getPatientResourceByName(url, HEADERS, full_name['f'], full_name['l'])
    patients = ''
    json_data = json.loads(response.text)
    patients = json_data['entry']
    d = {}
    for patient in patients: #incase there is more than one patient resource outputted
        resource = patient['resource']
        nameList = resource['name']
        idd = resource['id'] #need to use this
        d['given'] = nameList[1]['given'][0]
        d['family'] = nameList[0]['family']
        dob = resource['birthDate']
        d['birthtime'] = dob
        gender = resource['gender']
        d['gender'] = gender
        address = resource['address'][0]['line'][0]
        d['address'] = address
        state = resource['address'][0]['state']
        d['state'] = state
        city = resource['address'][0]['city']
        d['city'] = city
        zip = resource['address'][0]['postalCode']
        d['postalcode'] = zip
        #print(dict['birthtime'])#printed out on command line for checks


    ###########

    ###########

    return render_template("immunization.html", fname = d['given'], lname = d['family'],address=d['address'], city=d['city'],
                                       state=d['state'],
                                       postalcode=d['postalcode'],
                                       birthtime=d['birthtime'],
                                       gender=d['gender'])


def getPatientResourceByName(url, headers, fname, lname):
    data = {'Accept': 'application/json'}
    url+=("/?"+"given"+"="+fname+ "&"+"family"+"="+lname)
    response = requests.get(url=url, headers=headers)
    return response


def postNewImmunization(urlv, headers, payload):
    response = requests.post(url=urlv,headers=headers,data=payload)
    return response
#response = postNewImmunization(url, HEADERS, payload)
#print(response.text, ": ", response.status_code)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)

