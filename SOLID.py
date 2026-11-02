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

