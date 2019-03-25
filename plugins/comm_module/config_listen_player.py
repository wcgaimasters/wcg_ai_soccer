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
        if (s == 'True' or s == 'true' or s == 'TRUE'):
            return True
        elif (s == 'False' or s == 'false' or s == 'FALSE'):
            return False
        else:			
            raise ValueError
    
    def onMessage(self, payload, isBinary):

        info = json.loads(payload.decode('utf8'))
        with open('/home/wcg/wcg_ai_soccer/config.json', 'r') as config_file:
            data = json.load(config_file)
            data['rule']['game_time'] = int(info['rule']['game_time'])
            data['rule']['deadlock'] = self.str_to_bool(info['rule']['deadlock'])
            data['team_a']['name'] = info['team_a']['name']
            data['team_a']['executable'] = info['team_a']['executable']
            data['team_b']['name'] = info['team_b']['name']
            data['team_b']['executable'] = info['team_b']['executable']
            data['tool']['repeat'] = self.str_to_bool(info['tool']['repeat'])
            data['tool']['record'] = self.str_to_bool(info['tool']['record']) 
        with open('/home/wcg/wcg_ai_soccer/config.json', 'w') as config_file:
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

    print("Listening to config requests...")
    reactor.listenTCP(9001, factory)
    reactor.run()
