class MetricsCollection(object):
    def __init__(self):
        self._metrics = {}

    def get_metric(self, name, constructor):
        if name not in self._metrics:
            self._metrics[name] = constructor(name)

        return self._metrics[name]

    def add_metric(self, metric):
        self._metrics.append(metric)

    def metrics(self):
        for metric in self._metrics.itervalues():
            for mv in metric.metrics():
                yield mv

    def remove_metric(self, metric):
        self._metrics.remove(metric)


metrics_collection = MetricsCollection()
