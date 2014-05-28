__author__ = 'dukelion'
import txredisapi as redis
from twisted.python import log

TOPIC = 'topic'


class RedisPubSubProtocol(redis.SubscriberProtocol):
    def connectionMade(self):
        log.msg("Connected to redis\n\
        use the redis client to send messages:\n\
        $ redis-cli publish " + TOPIC + ".huii hello world\n")
        self.psubscribe("topic.*")
        self.continueTrying = True

    def messageReceived(self, pattern, channel, message):
        subscriber = channel[len(TOPIC) + 1:]
        self.factory.SocketFactory.send_bcast(subscriber, message)
        log.msg("pattern=%s, channel=%s message=%s" % (pattern, channel, message))

    def connectionLost(self, reason):
        log.msg("lost redis connection:", reason)

