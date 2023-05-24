##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: notifier.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Alberto Villalpando Cardona
# Version: 4.0.0 Mayo 2023
# Descripción:
#
#   Esta clase define el suscriptor que recibirá mensajes desde el distribuidor de mensajes
#   y lo notificará a un(a) enfermero(a) én particular para la atención del adulto mayor en
#   cuestión
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
#           |       on_message()     |  - self: definición de   |  - envía a través de  |
#           |                        |    la instancia de la    |    telegram los datos |
#           |                        |    clase                 |    del adulto mayor   |
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
import telepot

from stomp import ConnectionListener

class Notifier(ConnectionListener):
    def __init__(self):
        self.topic = '/topic/notifier'
        self.token = ""  # Set your Telegram bot token here
        self.chat_id = ""  # Set your Telegram chat ID here

    def queue(self):
        print("Inicio de gestión de notificaciones...")
        print()
        self.subscribe(destination=self.topic, on_message=self.on_message)

    def subscribe(self, destination, on_message):
        conn = stomp.Connection(host_and_ports=[('localhost', 61613)])
        conn.set_listener('', Notifier())
        conn.connect()
        conn.subscribe(destination=destination, id=1, ack='auto')
        while True:
            time.sleep(1)

    def on_message(self, message):
        print("enviando notificación de signos vitales...")
        if self.token and self.chat_id:
            body = message.body
            data = json.loads(body)
            message = f"ADVERTENCIA!!!\n[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}...\nssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}"
            bot = telepot.Bot(self.token)
            bot.sendMessage(self.chat_id, message)
        sys.stdout.flush()

if __name__ == '__main__':
    notifier = Notifier()
    notifier.queue()