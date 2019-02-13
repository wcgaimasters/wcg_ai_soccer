#!/usr/bin/python3

# Author(s): Luiz Felipe Vecchietti, Chansol Hong
# Maintainer: Chansol Hong (cshong@rit.kaist.ac.kr)
# Description: Communication Module to Simulator Instance

import sys
import json

import argparse

from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory

from twisted.python import log
from twisted.internet import reactor

class SimulatorClientProtocol(WebSocketClientProtocol):

    #def onConnect(self, response):
        #print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        #print("WebSocket connection open.")

        self.sendMessage(self.factory.command.encode('utf8'))

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Error: Binary message received: {0} bytes".format(len(payload)))
        else:
            print(payload.decode('utf8').rstrip('\n'))
            sys.__stdout__.flush()

    def onClose(self, wasClean, code, reason):
        #print("WebSocket connection closed: {0}".format(reason))
        if reactor.running:
            reactor.stop()

class SimulatorClientFactory(WebSocketClientFactory):
    
    def __init__(self, url, command):
        WebSocketClientFactory.__init__(self, url)
        self.command = command

if __name__ == '__main__':

    try:
        unicode
    except NameError:
        # Define 'unicode' for Python 3
        def unicode(s, *_):
            return s

    def to_unicode(s):
        return unicode(s, "utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("executable", type=to_unicode)
    parser.add_argument("server_ip", type=to_unicode)
    parser.add_argument("port", type=to_unicode)
    parser.add_argument("realm", type=to_unicode)
    parser.add_argument("key", type=to_unicode)
    parser.add_argument("datapath", type=to_unicode)

    args = parser.parse_args()

    # Player and Simulator IPs received as env. parameters
    with open('ips.json', 'r') as ips_file:
        data = json.load(ips_file)
    
    if (args.datapath == "examples/team_a_data"):
        player_ip = data['ips']['player_a_ip']
    elif (args.datapath == "examples/team_b_data"):
        player_ip = data['ips']['player_b_ip']
    else:
        print("Error")
        sys.exit(1)
    simulator_ip = data['ips']['simulator_ip']
    
    command = args.executable + " " + simulator_ip + " " + \
              args.port + " " + args.realm + " " +  args.key + " " + \
              args.datapath
    
    #log.startLogging(sys.stdout)
    
    factory = SimulatorClientFactory(u"ws://127.0.0.1:9000", command)
    factory.protocol = SimulatorClientProtocol

    reactor.connectTCP(player_ip, 9000, factory)
    reactor.run()
