from abc import ABC, abstractmethod


# 1. STORAGE ABSTRACTION
class Storage(ABC):

    @abstractmethod
    def save(self, metric):
        pass

    @abstractmethod
    def get_all(self):
        pass


# 2. STORAGE IMPLEMENTATIONS
class PostgreSQLStorage(Storage):

    def __init__(self):
        self.metrics = []

    def save(self, metric):
        self.metrics.append(metric)
        print("Saved metric to PostgreSQL")

    def get_all(self):
        return list(self.metrics)


class MongoDBStorage(Storage):

    def __init__(self):
        self.metrics = []

    def save(self, metric):
        self.metrics.append(metric)
        print("Saved metric to MongoDB")

    def get_all(self):
        return list(self.metrics)


# 3. BI CONNECTOR ABSTRACTION
class BIConnector(ABC):

    @abstractmethod
    def publish(self, metrics):
        pass


# 4. BI CONNECTOR IMPLEMENTATIONS
class TableauConnector(BIConnector):

    def publish(self, metrics):
        print("Publishing to Tableau:", metrics)


class PowerBIConnector(BIConnector):

    def publish(self, metrics):
        print("Publishing to Power BI:", metrics)


# 5. METRICS SERVICE
class MetricsService:

    def __init__(self, storage: Storage, bi: BIConnector):
        self.storage = storage
        self.bi = bi

    def record_metric(self, name, value):
        metric = {
            "name": name,
            "value": value
        }

        self.storage.save(metric)

    def publish_metrics(self):
        metrics = self.storage.get_all()
        self.bi.publish(metrics)


# 6. OBJECT CREATION
storage = PostgreSQLStorage()
bi = TableauConnector()

service = MetricsService(storage, bi)

service.record_metric("CPU Usage", 75)
service.record_metric("Memory Usage", 60)

service.publish_metrics()


# 7. SWITCH IMPLEMENTATIONS
storage2 = MongoDBStorage()
bi2 = PowerBIConnector()

service2 = MetricsService(storage2, bi2)

service2.record_metric("GPU Usage", 90)
service2.publish_metrics()
