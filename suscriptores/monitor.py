##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: monitor.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Alberto Villalpando Cardona
# Version: 4.0.0 Mayo 2023
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y los mostrará al área interesada para su monitoreo continuo
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
#           |       on_message()     |  - self: definición de   |  - muetra en pantalla |
#           |                        |    la instancia de la    |    los datos del      |
#           |                        |    clase                 |    adulto mayor       |
#           |                        |  - message: contenido    |    recibidos desde el |
#           |                        |    del mensaje recibido  |    distribuidor de    |
#           |                        |                          |    mensajes           |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import json
import time
import stomp
import sys

from stomp import ConnectionListener

class Monitor(ConnectionListener):
    def __init__(self):
        self.topic = '/topic/monitor'

    def queue(self):
        print("Inicio de monitoreo de signos vitales...")
        print()
        self.subscribe(destination=self.topic, on_message=self.on_message)

    def subscribe(self, destination, on_message):
        conn = stomp.Connection(host_and_ports=[('localhost', 61613)])
        conn.set_listener('', Monitor())
        conn.connect()  
        conn.subscribe(destination=destination, id=1, ack='auto')
        while True:
            time.sleep(1)

    def on_message(self, message):
        body = message.body
        data = json.loads(body)
        print("ADVERTENCIA!!!")
        print(f"[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}... con wearable {data['wearable']['id']}")
        print(f"ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        print()
        sys.stdout.flush()

if __name__ == '__main__':
    monitor = Monitor()
    monitor.queue()