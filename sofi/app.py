from autobahn.asyncio.websocket import WebSocketServerFactory, WebSocketServerProtocol
import asyncio

import json
import webbrowser


class SofiEventProcessor(object):

   def process(self, socket, event):
      if event['event'] == 'init':
         if self.oninit:
            self.oninit(socket)


class SofiEventProtocol(WebSocketServerProtocol):
   processor = SofiEventProcessor()

   def onConnect(self, request):
      print("Client connecting: %s" % request.peer)

   def onOpen(self):
      print("WebSocket connection open")

   def onMessage(self, payload, isBinary):
      if isBinary:
         print("Binary message received: {} bytes".format(len(payload)))
      else:
         print("Text message received: {}".format(payload.decode('utf8')))
         body = json.loads(payload.decode('utf8'))

         if 'event' in body:
            self.processor.process(self, body)

   def onClose(self, wasClean, code, reason):
      print("WebSocket connection closed: {}".format(reason))


class SofiEventServer(object):
   def __init__(self, hostname=u"127.0.0.1", port=9000, processor=None):
      self.hostname = hostname
      self.port = port
      self.processor = processor

      factory = WebSocketServerFactory(u"ws://" + hostname + u":" + str(port))
      protocol = SofiEventProtocol
      protocol.processor = processor

      factory.protocol = protocol

      self.loop = asyncio.get_event_loop()
      self.server = self.loop.create_server(factory, '0.0.0.0', port)

   def start(self):
      self.loop.run_until_complete(self.server)

      try:
         webbrowser.open('file:///Users/cabkarian/apps/sofi/test.html')
         self.loop.run_forever()

      except KeyboardInterrupt:
         pass

      finally:
         self.server.close()
         self.loop.close()

   def __repr__(self):
      return "<EventServer(%s, %s)>" % (self.hostname, self.port)

   def __str__(self):
      return repr(self)
