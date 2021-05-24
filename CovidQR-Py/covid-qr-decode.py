#!/usr/bin/python3
#
# Author: Guillaume Gagnon
# Licence: Apache 2.0
#
# Extract all payloads included in the Covid QR provided by the Quebec government (Preuve/passeport de vaccination)
# Note: The public key does not seem to be provided by the government at this point.
#       Hence, it is not possible to validate QR authenticity at the time being. (Although code is provided)
#       Public keys *should* be available here later on:
#       https://covid19.quebec.ca/PreuveVaccinaleApi/issuer/.well-known/jwks.json

# More info about the SMART Health Cards Framework can be found here:
# https://smarthealth.cards/

from pyzbar.pyzbar import decode # Need to: pip install pyzbar
from PIL import Image
import re
from jose import jwk # Need to: pip install python-jose
from jose.utils import base64url_decode
import zlib

# Set path to the QR image
# TODO: Take as args?
QRImageFile = "./QR.png" 


# Load QR data 
decodedQR = decode(Image.open(QRImageFile))
QRData = decodedQR[0].data.decode("utf-8")  # Get first element (this library support multiple QR codes in a file)
print ("---- RAW QR DATA:")
print (QRData +" \n")


# Rebuild JWS token
QRNumericData = re.sub("[^0-9]", "", QRData)     # Only keep numeric values
QRNumericPairs = re.findall("..", QRNumericData) # Split into groups of 2 numeric characters each of which represent a single JWS char
JWSToken = ""
for n in QRNumericPairs:
    JWSToken += chr(int(n) + 45) # Recreate the JWS string
print ("---- JWS TOKEN:")
print (JWSToken +"\n")


# Extract JWS Content
header, payload, signature = JWSToken.rsplit('.')
print ("---- JWS HEADER:")
decHeader = base64url_decode(header.encode('utf-8'))
print (decHeader.decode('utf-8') +"\n")

print ("---- JWS PAYLOAD:")
decPayload = base64url_decode(payload.encode('utf-8'))
uncompressedPayload = zlib.decompress(decPayload,-15) # Inflate RAW (use no headers bytes)
print (uncompressedPayload.decode("utf-8") + "\n")

print ("---- JWS SIGNATURE (base64):")
print (signature + "\n")


# Verify JWS token signature 
# Note: commented for now. Will be fully implemented once the public keys are provided by the government
#hmac_key = {
#    "kid": "### INSERT KID FROM QR PAYLOAD HERE ###",
#    "alg": "ES256",
#    "kty": "EC",
#    "crv": "P-256",
#    "use": "sig",
#    "x": "### INSERT X MATCHING KID HERE ###",
#    "y": "### INSERT Y MATCHING KID HERE ###"
#}
#key = jwk.construct(hmac_key)
#
#signedMessage, encodedSignature = JWSToken.rsplit('.', 1)
#decoded_sig = base64url_decode(encodedSignature.encode('utf-8'))
#key.verify(signedMessage, decoded_sig)
