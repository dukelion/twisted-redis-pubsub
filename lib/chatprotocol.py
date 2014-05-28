__author__ = 'dukelion'

from twisted.internet.protocol import Protocol
from txsockjs.utils import broadcast
from twisted.python import log


class ChatProtocol(Protocol):
    def connectionMade(self):
        if not hasattr(self.factory, "transports"):
            self.factory.transports = set()
        self.factory.transports.add(self.transport)

    def dataReceived(self, data):
        log.msg("received: " + data.__str__())
        broadcast(data, self.factory.transports)

    def connectionLost(self, reason):
        self.factory.transports.remove(self.transport)

