##!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
# Archivo: publicador.py
# Capitulo: Estilo Publica-Suscribe
# Autor(es): Alberto Villalpando Cardona
# Version: 4.0.0 Mayo 2023
# Descripción:
#
#   Este archivo define la conexión del publicador hacia el el distribuidor de mensajes
#
#   A continuación se describen los métodos que se implementaron en este archivo:
#
#                                             Métodos:
#           +------------------------+--------------------------+-----------------------+
#           |         Nombre         |        Parámetros        |        Función        |
#           +------------------------+--------------------------+-----------------------+
#           |        publish()       |  - queue: nombre de la   |  - publica el mensaje |
#           |                        |    ruta con la que se    |    en el distribuidor |
#           |                        |    vinculará el mensaje  |    de mensajes        |
#           |                        |    enviado               |                       |
#           |                        |  - data: mensaje que     |                       |
#           |                        |    será enviado          |                       |
#           +------------------------+--------------------------+-----------------------+
#
#-------------------------------------------------------------------------
import stomp
import sys

def publish(queue, data):
    conn = stomp.Connection(host_and_ports=[('localhost', 61613)])
    conn.connect()
    conn.send(body=data, destination=queue, headers={'persistent': 'true'}, wait=True)
    conn.disconnect()