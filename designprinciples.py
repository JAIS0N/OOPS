
"""
MODULE 5: SOFTWARE DESIGN PRINCIPLES

1. DRY  - Don't Repeat Yourself
2. KISS - Keep It Simple, Stupid
3. YAGNI - You Aren't Gonna Need It
4. SoC  - Separation of Concerns

Each section contains:
- NON-IDEAL CODE
- IMPROVED CODE
- WHY THE IMPROVEMENT MATTERS
"""

from abc import ABC, abstractmethod


# ============================================================
# 1. DRY - DON'T REPEAT YOURSELF
# ============================================================

# NON-IDEAL: Same business rule duplicated in two classes.
# If tax changes, both classes must be updated.

class BadSalesService:
    def calculate_total(self, amount):
        tax = amount * 0.08
        return amount + tax


class BadBillingService:
    def generate_invoice(self, amount):
        tax = amount * 0.08
        return amount + tax


# IMPROVED: One authoritative implementation of the tax rule.

class TaxCalculator:
    TAX_RATE = 0.08

    def calculate_total(self, amount):
        return amount * (1 + self.TAX_RATE)


class SalesService:
    def __init__(self, calculator):
        self.calculator = calculator

    def calculate_total(self, amount):
        return self.calculator.calculate_total(amount)


class BillingService:
    def __init__(self, calculator):
        self.calculator = calculator

    def generate_invoice(self, amount):
        return self.calculator.calculate_total(amount)


def demo_dry():
    print("\n--- DRY ---")

    bad_sales = BadSalesService()
    bad_billing = BadBillingService()

    print("Non-ideal sales:", bad_sales.calculate_total(100))
    print("Non-ideal billing:", bad_billing.generate_invoice(100))

    calculator = TaxCalculator()

    sales = SalesService(calculator)
    billing = BillingService(calculator)

    print("Improved sales:", sales.calculate_total(100))
    print("Improved billing:", billing.generate_invoice(100))


# ============================================================
# 2. KISS - KEEP IT SIMPLE
# ============================================================

# NON-IDEAL: Unnecessary abstraction for a simple average.
# Four classes are used where one function is sufficient.

class CalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, data):
        pass


class AverageStrategy(CalculationStrategy):
    def calculate(self, data):
        return sum(data) / len(data)


class CalculationFactory:
    def create(self):
        return AverageStrategy()


class BadMetricsService:
    def __init__(self):
        self.strategy = CalculationFactory().create()

    def calculate(self, data):
        return self.strategy.calculate(data)


# IMPROVED: Simple function with input validation.

def calculate_average(data):
    if not data:
        raise ValueError("Data cannot be empty")

    return sum(data) / len(data)


def demo_kiss():
    print("\n--- KISS ---")

    bad_service = BadMetricsService()
    print("Overengineered:", bad_service.calculate([10, 20, 30]))

    print("Simple:", calculate_average([10, 20, 30]))


# ============================================================
# 3. YAGNI - YOU AREN'T GONNA NEED IT
# ============================================================

# NON-IDEAL:
# Building a complex factory for hypothetical integrations.
# Assume only Tableau is currently required.


class TableauConnector:
    def publish(self, metric):
        print("Tableau published:", metric)


class PowerBIConnector:
    def publish(self, metric):
        print("Power BI published:", metric)


class LookerConnector:
    def publish(self, metric):
        print("Looker published:", metric)


class FuturePlatformConnector:
    def publish(self, metric):
        print("Future platform published:", metric)


class UnnecessaryBIConnectorFactory:
    def create(self, connector_type):
        if connector_type == "tableau":
            return TableauConnector()

        elif connector_type == "powerbi":
            return PowerBIConnector()

        elif connector_type == "looker":
            return LookerConnector()

        elif connector_type == "future_platform":
            return FuturePlatformConnector()

        raise ValueError("Unknown connector")


# IMPROVED:
# Implement only the currently needed integration.
# Still allow dependency injection for easy testing.


class SimpleMetricsService:
    def __init__(self, connector):
        self.connector = connector

    def publish(self, metric):
        self.connector.publish(metric)


def demo_yagni():
    print("\n--- YAGNI ---")

    # Non-ideal: unnecessary factory and extra implementations
    factory = UnnecessaryBIConnectorFactory()
    connector = factory.create("tableau")
    connector.publish("revenue")

    # Improved: use only the required dependency
    service = SimpleMetricsService(TableauConnector())
    service.publish("revenue")


# ============================================================
# 4. SEPARATION OF CONCERNS (SoC)
# ============================================================

# NON-IDEAL:
# One class handles validation, calculation,
# persistence, and BI publishing.


class BadMetricsAPI:
    def handle_request(self, metric):

        # Concern 1: Validation
        if metric < 0:
            raise ValueError("Invalid metric")

        # Concern 2: Business logic
        result = metric * 1.1

        # Concern 3: Persistence
        print("Saving:", result)

        # Concern 4: BI publishing
        print("Publishing:", result)

        return result


# IMPROVED:
# Each class has a focused responsibility.


# Business logic and validation
class MetricCalculator:
    def calculate(self, value):
        if value < 0:
            raise ValueError("Invalid metric")

        return value * 1.1


# Persistence responsibility
class MetricRepository:
    def save(self, value):
        print("Saved:", value)


# BI integration responsibility
class BIConnector:
    def publish(self, value):
        print("Published:", value)


# Orchestration responsibility
class MetricsService:
    def __init__(self, calculator, repository, connector):
        self.calculator = calculator
        self.repository = repository
        self.connector = connector

    def record(self, value):

        # Delegate calculation
        result = self.calculator.calculate(value)

        # Delegate persistence
        self.repository.save(result)

        # Delegate BI publishing
        self.connector.publish(result)

        return result


# API layer responsibility
class MetricsAPI:
    def __init__(self, service):
        self.service = service

    def handle_request(self, value):
        return self.service.record(value)


def demo_soc():
    print("\n--- SEPARATION OF CONCERNS ---")

    bad_api = BadMetricsAPI()
    print("Non-ideal result:", bad_api.handle_request(100))

    calculator = MetricCalculator()
    repository = MetricRepository()
    connector = BIConnector()

    service = MetricsService(
        calculator,
        repository,
        connector
    )

    api = MetricsAPI(service)

    print("Improved result:", api.handle_request(100))


# ============================================================
# 5. RUN ALL EXAMPLES
# ============================================================

if __name__ == "__main__":
    demo_dry()
    demo_kiss()
    demo_yagni()
    demo_soc()


# ============================================================
# INTERVIEW REVISION
# ============================================================

# DRY:
# Avoid duplicated business knowledge.
# Centralize shared rules when they represent the same concern.

# KISS:
# Prefer simple solutions.
# Don't create unnecessary classes or abstractions.

# YAGNI:
# Don't implement speculative features.
# Build functionality when there is a real requirement.

# SEPARATION OF CONCERNS:
# Divide distinct responsibilities into focused components.
# Example: API -> Service -> Repository / BI Connector

# IMPORTANT:
# Good design balances these principles.
# Too many abstractions can violate KISS and YAGNI.
# Too few boundaries can violate DRY and SoC.
