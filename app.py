#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "buscarAtractivos":
        return {}
 #   datoingresdo = makeYqlQuery(req)
 #   if buscasitur is None:
 #       return{}
    datoingresado = "parque solano"
    urlsitur = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?search="
    quitar_espacios = datoingresado.replace(" ", "%20")
    data = json.loads(urlopen(urlsitur + quitar_espacios).read())#en esta se obtiene todo el contenido... equivale a data
    testproceso = data[0].get('slug')
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    global city
    global city2
    city = parameters.get("atractivos")
    city2 = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
    if city is None:
        return None

    return city


def makeWebhookResult(data):
    buscasitur = "parque solano"
    urlsitur = "http://situr.boyaca.gov.co/wp-json/wp/v2/atractivo_turistico?search="
    buscasitur_sin_espacio = buscasitur.replace(" ", "%20")
    leer = json.loads(urlopen(urlsitur + buscasitur_sin_espacio).read())
    test = leer[0].get('slug')
    nombre_atractivo = leer[0]['title']['rendered']
    descripcion_atractivo = leer[0]['excerpt']['rendered']
    url_atractivo = leer[0].get('link')

    mahoobox = " hola mundo dato ingresado: "
    datoapi = (json.dumps(item, indent=4))

    # print(json.dumps(item, indent=4))

#    speech = "Hoy Mauricio in " + location.get('city') + ": " + condition.get('text') + ", SI ENTENDIO LA TEMPERATURA " + condition.get('temp') + " " + units.get('temperature')
    speech = "Mira, encontré esta información sobre  " + nombre_atractivo + ": " + descripcion_atractivo + "        Si quieres ver más info visita:  "  + url_atractivo + city

    print("Response:")
    print(speech)
  #  print(salidapruebas)

    return {
        "speech": speech,
 #       "salidapruebas": salidapruebas
        "displayText": speech,
       # "data": data,
       # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')