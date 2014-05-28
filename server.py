__author__ = 'dukelion'


from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.web import resource, server, static
from twisted.application import service, internet
from txsockjs.factory import SockJSResource
from os.path import realpath, dirname
from twisted.python import log
from sys import stdout
import txredisapi as redis

from lib import EchoProtocol, ChatProtocol, RedisPubSubProtocol
log.startLogging(stdout)


class RedisFactory(redis.SubscriberFactory):
    # SubscriberFactory is a wrapper for the ReconnectingClientFactory
    maxDelay = 120
    continueTrying = True
    protocol = RedisPubSubProtocol

redisClientApp = service.Application("subscriber")
srv = internet.TCPClient("127.0.0.1", 6379, RedisFactory())
srv.setServiceParent(redisClientApp)
srv.startService()

index = dirname(realpath(__file__)) + "/html/"
root = static.File(index)

#log.msg(index)
root.putChild("chat", SockJSResource(Factory.forProtocol(ChatProtocol)))

site = server.Site(root)

reactor.listenTCP(8080, site)
reactor.run()