#!/usr/bin/python3

# Author(s): Luiz Felipe Vecchietti, Chansol Hong
# Maintainer: Chansol Hong (cshong@rit.kaist.ac.kr)
# Description: Communication Module to Player Instance

import sys
import json

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

from twisted.python import log
from twisted.internet import reactor

class PlayerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def str_to_bool(self, s):
        if s == 'True':
            return True
        elif s == 'False':
            return False
        else:			
            raise ValueError
    
    def onMessage(self, payload, isBinary):

        command = payload.decode('utf8')
        info = command.split()
        with open('../../config.json', 'r') as config_file:
            data = json.load(config_file)
            data['tool']['record'] = self.str_to_bool(info[0])
            data['team_a']['name'] = info[1]
            data['team_b']['name'] = info[2]
        with open('../../config.json', 'w') as config_file:
            json.dump(data, config_file)
			
        # echo back message verbatim
        self.sendMessage("updated".encode('utf8'))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

if __name__ == '__main__':
    
    #log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9001")
    factory.protocol = PlayerProtocol
    factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9001, factory)
    reactor.run()
