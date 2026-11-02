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
        self.connector.publish(metrics)


# 5. DECORATOR: wrap storage to add logging without editing storage itself.
# NON-IDEAL: duplicate logging code in every concrete storage implementation.
class LoggingStorage(Storage):
    def __init__(self, wrapped: Storage):
        self.wrapped = wrapped

    def save(self, metric):
        print("Logging: starting save")
        self.wrapped.save(metric)
        print("Logging: save completed")


class CountingStorage(Storage):
    def __init__(self, wrapped: Storage):
        self.wrapped = wrapped
        self.save_count = 0

    def save(self, metric):
        self.wrapped.save(metric)
        self.save_count += 1  # count only successful returns
        print("Successful saves:", self.save_count)


# 6. SINGLETON: one instance per class within this Python process.
# CAUTION: global state complicates tests; this simple example is not
# thread-safe and does not create a singleton across multiple processes.
class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance


# 7. BUILDER: construct a configuration step by step.
# NON-IDEAL: a constructor with many positional optional arguments is hard
# to read. This is a simple fluent builder-style API.
class InferenceConfigBuilder:
    def __init__(self):
        self.model = None
        self.batch_size = 1
        self.gpu_count = 1

    def set_model(self, model):
        self.model = model
        return self

    def set_batch_size(self, batch_size):
        if batch_size < 1:
            raise ValueError("batch_size must be positive")
        self.batch_size = batch_size
        return self

    def set_gpu_count(self, gpu_count):
        if gpu_count < 1:
            raise ValueError("gpu_count must be positive")
        self.gpu_count = gpu_count
        return self

    def build(self):
        if not self.model:
            raise ValueError("model is required")
        return {
            "model": self.model,
            "batch_size": self.batch_size,
            "gpu_count": self.gpu_count,
        }


def main():
    print("\n1. STRATEGY")
    MetricsService(PostgreSQLStorage()).record({"cpu": 75})
    MetricsService(MongoDBStorage()).record({"gpu": 90})

    print("\n2. FACTORY")
    storage = StorageFactory.create("postgres")
    MetricsService(storage).record({"memory": 60})

    print("\n3. OBSERVER")
    events = MetricPublisher()
    events.subscribe(EmailAlert())
    events.subscribe(AuditLogger())
    events.publish({"gpu": 95})

    print("\n4. ADAPTER")
    BIPublisher(TableauAdapter(TableauSDK())).publish({"revenue": 100000})

    print("\n5. DECORATOR")
    wrapped = CountingStorage(LoggingStorage(PostgreSQLStorage()))
    wrapped.save({"cpu": 80})

    print("\n6. SINGLETON")
    config1 = AppConfig()
    config2 = AppConfig()
    print("Same instance:", config1 is config2)

    print("\n7. BUILDER")
    inference_config = (InferenceConfigBuilder()
                        .set_model("Llama")
                        .set_batch_size(32)
                        .set_gpu_count(4)
                        .build())
    print(inference_config)


if __name__ == "__main__":
    main()
