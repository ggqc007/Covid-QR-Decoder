# Covid Passport Decoder #

Extract all payloads included in the Covid QR provided by the Quebec government (Preuve/passeport de vaccination) 

**Note:** The public key does not seem to be provided by the government at this point.
Hence, it is not possible to validate QR authenticity at the time being. (Although some of the code is provided in the Python version)

Public keys *should* be available here later: 
[https://covid19.quebec.ca/PreuveVaccinaleApi/issuer/.well-known/jwks.json](https://covid19.quebec.ca/PreuveVaccinaleApi/issuer/.well-known/jwks.json)

More info about the SMART Health Cards Framework can be found here:
[https://smarthealth.cards/](https://smarthealth.cards/)

---

# This repo contains two versions #
## JavaScript: ##
1. cd CovidQR-JS/
2. npm install
3. Edit the path to your .png QR image in the script
4. ./covid-qr-decode.js


## Python: ##
1. cd CovidQR-Py/
2. pip install python-jose pyzbar (this will install some dependencies)
3. Edit the path to your .png QR image in the script
4. ./covid-qr-decode.py

# Sample payload #
> {"kid":"SOME-KEY-ID","zip":"SOME-ZIP","alg":"ES256"}

>{
  "resource": {
    "resourceType": "Patient",
    "name": [
      {
        "family": [
          "NAME"
        ],
        "given": [
          "SURNAME"
        ]
      }
    ],
    "birthDate": "1900-01-01",
    "gender": "SEX"
  }
}
{
  "resource": {
    "resourceType": "Immunization",
    "vaccineCode": {
      "coding": [
        {
          "system": "http://hl7.org/fhir/sid/cvx",
          "code": "208"
        }
      ]
    },
    "patient": {
      "reference": "resource:0"
    },
    "lotNumber": "SOME-LOT-NUMBER",
    "status": "Completed",
    "occurrenceDateTime": "2021-04-01T04:00:00+00:00",
    "location": {
      "reference": "resource:0",
      "display": "VACCINATION-SITE"
    },
    "protocolApplied": {
      "doseNumber": 1,
      "targetDisease": {
        "coding": [
          {
            "system": "http://browser.ihtsdotools.org/?perspective=full&conceptId1=840536004",
            "code": "840536004"
          }
        ]
      }
    },
    "note": [
      {
        "text": "PB COVID-19"
      }
    ]
  }
}



