__author__ = 'dukelion'

from sys import stdout

from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.web import server, static
from twisted.application import service, internet
from txsockjs.factory import SockJSResource
from os.path import realpath, dirname
from twisted.python import log
from txsockjs.utils import broadcast
import txredisapi as redis
from lib import ChatProtocol, RedisPubSubProtocol

log.startLogging(stdout)


class RedisFactory(redis.SubscriberFactory):
    # SubscriberFactory is a wrapper for the ReconnectingClientFactory
    maxDelay = 120
    continueTrying = True
    protocol = RedisPubSubProtocol


class ChatFactory(Factory):
    protocol = ChatProtocol

    def send_bcast(self, subscriber, message):
        message = "msg,{},{}".format(subscriber, message)
        if hasattr(self, 'transports'):
            log.msg("Sending " + message)
            broadcast(message, self.transports)


redisClientApp = service.Application("subscriber")

factory = RedisFactory()

srv = internet.TCPClient("127.0.0.1", 6379, factory)
srv.setServiceParent(redisClientApp)
srv.startService()

index = dirname(realpath(__file__)) + "/html/"
root = static.File(index)

chatFactory = ChatFactory()
RedisFactory.SocketFactory = chatFactory

root.putChild("chat", SockJSResource(chatFactory))
site = server.Site(root)

reactor.listenTCP(8080, site)
reactor.run()