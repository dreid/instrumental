import pprint

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from instrumental.client import InstrumentedAgent
from instrumental.collection import metrics_collection


def print_metrics():
    pprint.pprint([(mv.name, mv.value) for mv in metrics_collection.metrics()])

agent = InstrumentedAgent(reactor)

rlc = LoopingCall(agent.request, 'GET', 'http://localhost:8080')
mlc = LoopingCall(print_metrics)


def start():
    rlc.start(0.1)
    mlc.start(1)

reactor.callWhenRunning(start)

reactor.run()
