from twisted.web.client import Agent

from bucky.metrics.meter import Meter

from instrumental.collection import metrics_collection


class InstrumentedAgent(object):
    measuredMethods = set([
        'GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'TRACE',
        'PATCH', 'DELETE', 'MOVE', 'CONNECT'
    ])

    _methodMetrics = {}

    def __init__(self, reactor, *args, **kwargs):
        self._metrics_collection = kwargs.pop('metrics_collection', metrics_collection)
        self._agent = Agent(reactor, *args, **kwargs)

        for method in self.measuredMethods:
            metricName = 'http.client.{0}-requests'.format(method)
            self._methodMetrics[method] = self._metrics_collection.get_metric(
                metricName,
                Meter
            )

        self._otherMethods = self._metrics_collection.get_metric('http.client.other-requests', Meter)

    def request(self, method, *args, **kwargs):
        metric = self._methodMetrics.get(method, self._otherMethods)

        def _update_metric(result):
            metric.update(1)
            return result

        d = self._agent.request(method, *args, **kwargs)
        d.addBoth(_update_metric)

        return d
