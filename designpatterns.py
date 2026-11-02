"""Seven OOP design patterns in one runnable Python file.
Backend examples are simulations; no external database or API is contacted.
Run: python design_patterns_backend.py
"""
from abc import ABC, abstractmethod


# 1. STRATEGY: interchange storage behavior without changing MetricsService.
# NON-IDEAL: a service with if/elif for every database grows whenever a new
# storage backend is introduced.
class Storage(ABC):
    @abstractmethod
    def save(self, metric):
        pass


class PostgreSQLStorage(Storage):
    def save(self, metric):
        print("PostgreSQL saved:", metric)


class MongoDBStorage(Storage):
    def save(self, metric):
        print("MongoDB saved:", metric)


class MetricsService:
    def __init__(self, storage: Storage):
        self.storage = storage  # HAS-A + dependency injection

    def record(self, metric):
        self.storage.save(metric)  # polymorphism + dynamic dispatch


# 2. SIMPLE FACTORY: centralize object creation.
# NON-IDEAL: repeat if/elif object creation across many callers.
class StorageFactory:
    @staticmethod
    def create(kind):
        if kind == "postgres":
            return PostgreSQLStorage()
        if kind == "mongo":
            return MongoDBStorage()
        raise ValueError("Unknown storage type: " + kind)


# 3. OBSERVER: notify registered listeners when a metric arrives.
# NON-IDEAL: MetricPublisher directly creates EmailAlert and AuditLogger.
class MetricPublisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, metric):
        for subscriber in self.subscribers:
            subscriber.update(metric)


class EmailAlert:
    def update(self, metric):
        print("Email alert:", metric)


class AuditLogger:
    def update(self, metric):
        print("Audit log:", metric)


# 4. ADAPTER: translate an external SDK's interface into our own.
# NON-IDEAL: business logic calls vendor-specific send_dataset() directly.
class TableauSDK:
    def send_dataset(self, dataset):
        print("Tableau SDK received:", dataset)


class BIConnector(ABC):
    @abstractmethod
    def publish(self, metrics):
        pass


class TableauAdapter(BIConnector):
    def __init__(self, sdk):
        self.sdk = sdk

    def publish(self, metrics):
        self.sdk.send_dataset(metrics)


class BIPublisher:
    def __init__(self, connector: BIConnector):
        self.connector = connector

    def publish(self, metrics):
