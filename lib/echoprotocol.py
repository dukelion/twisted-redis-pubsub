__author__ = 'dukelion'
from twisted.internet.protocol import Factory, Protocol


class EchoProtocol(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)
