##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: record.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Alberto Villalpando Cardona
# Version: 4.0.0 Mayo 2023
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y los almacena en un archivo de texto que simula el expediente de los pacientes
#
#   Este archivo también define el punto de ejecución del Suscriptor
#
#   A continuación se describen los métodos que se implementaron en esta clase:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |       __init__()       |  - self: definición de   |  - constructor de la  |
#           |                        |    la instancia de la    |    clase              |
#           |                        |    clase                 |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       queue()          |  - self: definición de   |  - inicializa el      |
#           |                        |    la instancia de la    |    proceso de         |
#           |                        |    clase                 |    monitoreo de       |
#           |                        |                          |    signos vitales     |
#           +------------------------+--------------------------+-----------------------+
#           |       subscribe()      |  - self: definición de   |  - realiza la         |
#           |                        |    la instancia de la    |    suscripción en el  |
#           |                        |    clase                 |    distribuidor de    |
#           |                        |  - destination:          |    mensajes para      |
#           |                        |    ruta a la que         |    comenzar a recibir |
#           |                        |    el suscriptor está    |    mensajes           |
#           |                        |    interesado en recibir |                       |
#           |                        |    mensajes              |                       |
#           |                        |  - on_message: accion a  |                       |
#           |                        |    ejecutar al recibir   |                       |
#           |                        |    el mensaje desde el   |                       |
#           |                        |    distribuidor de       |                       |
#           |                        |    mensajes              |                       |
#           +------------------------+--------------------------+-----------------------+
#           |       on_message()     |  - self: definición de   |  - escribe los datos  |
#           |                        |    la instancia de la    |    del adulto mayor   |
#           |                        |    clase                 |    recibidos desde el |
#           |                        |  - message: contenido    |    distribuidor de    |
#           |                        |    del mensaje recibido  |    mensajes en un     |
#           |                        |                          |    archivo de texto   |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import json
import time
import stomp
import sys
import os

from stomp import ConnectionListener

class Record(ConnectionListener):
    def __init__(self):
        try:
            os.mkdir('records')
        except OSError as _:
            pass
        self.topic = '/topic/record'

    def queue(self):
        print("Esperando datos del paciente para actualizar expediente...")
        print()
        self.subscribe(destination=self.topic, on_message=self.on_message)

    def subscribe(self, destination, on_message):
        conn = stomp.Connection(host_and_ports=[('localhost', 61613)])
        conn.set_listener('', Record())
        conn.connect()
        conn.subscribe(destination=destination, id=1, ack='auto')
        while True:
            time.sleep(1)

    def on_message(self, message):
        print("datos recibidos, actualizando expediente del paciente...")
        body = message.body
        data = json.loads(body)
        record_file = open(f"./records/{data['ssn']}.txt", 'a')
        record_file.write(f"\n[{data['wearable']['date']}]: {data['name']} {data['last_name']}... ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        record_file.close()
        sys.stdout.flush()

if __name__ == '__main__':
    record = Record()
    record.queue()