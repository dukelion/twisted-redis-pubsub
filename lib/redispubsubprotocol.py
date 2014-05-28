__author__ = 'dukelion'
from twisted.internet.protocol import Protocol
import txredisapi as redis
from twisted.python import log


class RedisPubSubProtocol(redis.SubscriberProtocol):
    def connectionMade(self):
        log.msg("Connected to redis\n\
        use the redis client to send messages:\n\
        $ redis-cli publish chattopic.huii hello world\n")
        self.psubscribe("chattopic.*")
        self.continueTrying = True


    def messageReceived(self, pattern, channel, message):
        log.msg("pattern=%s, channel=%s message=%s" % (pattern, channel, message))

    def connectionLost(self, reason):
        log.msg("lost redis connection:", reason)