#!/usr/bin/env node
// 
// Author: Guillaume Gagnon
// Licence: Apache 2.0
//
// Extract all payloads included in the Covid QR provided by the Quebec government (Preuve/passeport de vaccination)
// Note: The public key do not seems to be provided by the government at this point.
//       Hence, it is not possible to validate QR authenticity at the time being.
//       Public keys should be available here later on:
//       https://covid19.quebec.ca/PreuveVaccinaleApi/issuer/.well-known/jwks.json

// This script has been built using this very nice and detailed HOWTO:
// https://github.com/dvci/health-cards-walkthrough/blob/main/SMART%20Health%20Cards.ipynb
//
// Also, more info about the SMART Health Cards Framework can be found here:
// https://smarthealth.cards/


const fs = require('fs');
var jsQR = require('jsqr');
var PNG = require('pngjs').PNG;
var jose = require('node-jose');
var base64url = require("base64url");
var zlib = require("zlib");


// Extract RAW QR from picture
imageData = PNG.sync.read(fs.readFileSync('./QR.png'))
const scannedQR = jsQR(new Uint8ClampedArray(imageData.data.buffer), imageData.width, imageData.height)
console.log("RAW QR DATA:")
console.log(scannedQR.data)
console.log("")


// Extract JWS
const scannedJWS = scannedQR
    .chunks
    .filter(chunk => chunk.type === "numeric")[0] // Grab the numeric chunk
    .text.match(/(..?)/g) // Split into groups of 2 numeric characters each of which represent a single JWS char
    .map(num => String.fromCharCode(parseInt(num, 10) + 45)).join('') // Convert from numeric encoding to JWS
console.log("JWS DATA:")
console.log(scannedJWS)
console.log("")


// Extract JWS Header
JWSHeaders = base64url.decode(scannedJWS.split(".")[0])
console.log("JWS HEAD:")
console.log(JWSHeaders)
console.log("")


// Extract payload
JWSPayload = scannedJWS.split(".")[1]
const payload = Buffer.from(JWSPayload, "base64");
zlib.inflateRaw(payload, function (err, decompressedResult) {
    scannedResult = decompressedResult.toString("utf8");
    console.log(scannedResult)
    //const entries = JSON.parse(scannedResult) // Uncomment this bloc if you want to "beautify" the json output
    //    .vc.credentialSubject.fhirBundle.entry
    //    .map(entry => console.log(JSON.stringify(entry, null, 2)))
});
