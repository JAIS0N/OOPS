"""SOLID principles with realistic backend engineering examples.

Run: python solid_real_backend.py
All integrations are in-memory simulations, not real database/API calls.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Metric:
    name: str
    value: float


# S: SINGLE RESPONSIBILITY
# NON-IDEAL: changes to validation, storage, or BI publishing all change this class.
class BadMetricsServiceSRP:
    def record(self, name, value):
        if not name or value < 0:
            raise ValueError("Invalid metric")
        print("SQL INSERT:", name, value)
        print("Tableau API publish:", name, value)


# IDEAL: each component has one reason to change.
class MetricValidator:
    def validate(self, metric):
        if not metric.name or metric.value < 0:
            raise ValueError("Invalid metric")


class InMemoryMetricStorage:
    def __init__(self):
        self.metrics = []

    def save(self, metric):
        self.metrics.append(metric)

    def get_all(self):
        return list(self.metrics)


class ConsoleBIConnector:
    def publish(self, metrics):
        print("Published metrics:", metrics)


class GoodMetricsServiceSRP:
    def __init__(self, validator, storage, connector):
        self.validator = validator
        self.storage = storage
        self.connector = connector

    def record(self, metric):
        self.validator.validate(metric)
        self.storage.save(metric)

    def publish(self):
        self.connector.publish(self.storage.get_all())


# O: OPEN/CLOSED
# NON-IDEAL: every new BI provider forces edits to existing dispatch logic.
class BadBIPublisherOCP:
    def publish(self, provider, metrics):
        if provider == "tableau":
            print("Tableau:", metrics)
        elif provider == "powerbi":
            print("Power BI:", metrics)
        else:
            raise ValueError("Unknown provider")


# IDEAL: extend by implementing a new connector, without editing publisher.
class BIConnector(ABC):
    @abstractmethod
    def publish(self, metrics):
        pass


class TableauConnector(BIConnector):
    def publish(self, metrics):
        print("Tableau:", metrics)


class PowerBIConnector(BIConnector):
    def publish(self, metrics):
        print("Power BI:", metrics)


class SnowflakeConnector(BIConnector):
    def publish(self, metrics):
        print("Snowflake BI export:", metrics)


class GoodBIPublisherOCP:
    def __init__(self, connector: BIConnector):
        self.connector = connector

    def publish(self, metrics):
        self.connector.publish(metrics)


# L: LISKOV SUBSTITUTION
# NON-IDEAL: base storage promises save AND read, but write-only sink breaks read.
class BadStorageLSP:
    def save(self, metric):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError


class BadWriteOnlySink(BadStorageLSP):
    def save(self, metric):
        print("Queued:", metric)

    def get_all(self):
        raise RuntimeError("Write-only sink cannot read metrics")


# IDEAL: only advertise capabilities that implementations can honor.
class MetricWriter(ABC):
    @abstractmethod
    def save(self, metric):
        pass


class MetricReader(ABC):
    @abstractmethod
    def get_all(self):
        pass


class PostgreSQLStorage(MetricWriter, MetricReader):
    def __init__(self):
        self.metrics = []

    def save(self, metric):
        self.metrics.append(metric)

    def get_all(self):
        return list(self.metrics)


class KafkaMetricSink(MetricWriter):
    def __init__(self):
        self.events = []

    def save(self, metric):
        self.events.append(metric)


def persist_metric(writer: MetricWriter, metric):
    writer.save(metric)


def read_metrics(reader: MetricReader):
    return reader.get_all()


# I: INTERFACE SEGREGATION
# NON-IDEAL: read-only dashboards must implement irrelevant write/delete methods.
class BadMetricsRepositoryISP(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, metric):
        pass

    @abstractmethod
    def delete(self, name):
        pass


class BadReadOnlyDashboard(BadMetricsRepositoryISP):
    def read(self):
        return []

    def write(self, metric):
        raise NotImplementedError("Read-only dashboard")

    def delete(self, name):
        raise NotImplementedError("Read-only dashboard")


# IDEAL: narrow interfaces; dashboards only depend on reading.
class MetricsQuery(ABC):
    @abstractmethod
    def read(self):
        pass


class MetricsCommand(ABC):
    @abstractmethod
    def write(self, metric):
        pass


class Dashboard(MetricsQuery):
    def __init__(self, reader: MetricReader):
        self.reader = reader

    def read(self):
        return self.reader.get_all()


# D: DEPENDENCY INVERSION
# NON-IDEAL: business logic directly constructs concrete database/BI classes.
class BadMetricsServiceDIP:
    def __init__(self):
        self.storage = PostgreSQLStorage()
        self.bi = TableauConnector()

    def record(self, metric):
        self.storage.save(metric)

    def publish(self):
        self.bi.publish(self.storage.get_all())


# IDEAL: high-level service depends on abstract capabilities.
# Dependency injection: caller supplies the implementations.
# Inversion of control: caller decides which implementations to use.
class MetricsService:
    def __init__(self, writer: MetricWriter, reader: MetricReader,
                 connector: BIConnector, validator: MetricValidator):
        self.writer = writer
        self.reader = reader
        self.connector = connector
        self.validator = validator

    def record(self, metric):
        self.validator.validate(metric)
        self.writer.save(metric)

    def publish(self):
        self.connector.publish(self.reader.get_all())


if __name__ == "__main__":
    cpu = Metric("cpu_usage_percent", 75)
    gpu = Metric("gpu_usage_percent", 90)

    print("S: Single Responsibility")
    srp = GoodMetricsServiceSRP(MetricValidator(), InMemoryMetricStorage(), ConsoleBIConnector())
    srp.record(cpu)
    srp.publish()

    print("\nO: Open/Closed")
    GoodBIPublisherOCP(SnowflakeConnector()).publish([cpu])

    print("\nL: Liskov Substitution")
    postgres = PostgreSQLStorage()
    kafka = KafkaMetricSink()
    persist_metric(postgres, cpu)
    persist_metric(kafka, gpu)
    print("Readable metrics:", read_metrics(postgres))
    print("Queued events:", kafka.events)

    print("\nI: Interface Segregation")
    print("Dashboard:", Dashboard(postgres).read())

    print("\nD: Dependency Inversion")
    storage = PostgreSQLStorage()
    service = MetricsService(storage, storage, PowerBIConnector(), MetricValidator())
    service.record(cpu)
    service.record(gpu)
    service.publish()

    # Swap BI implementation without modifying MetricsService.
    alternate = MetricsService(storage, storage, TableauConnector(), MetricValidator())
    alternate.publish()
