from abc import ABC, abstractmethod

# 1. ABSTRACTION: Define the strict contract
class TelemetryExporter(ABC):
    
    @abstractmethod
    def export(self, data: dict) -> None:
        """Every exporter must implement this method, but the parent doesn't care how."""
        pass

    def validate(self, data: dict) -> bool:
        """Concrete method: Shared utility logic inherited by everyone."""
        return bool(data)


# 2. INHERITANCE: DatadogExporter inherits from TelemetryExporter
class DatadogExporter(TelemetryExporter):
    
    # 3. METHOD OVERRIDING: Providing the specific "how" for Datadog
    def export(self, data: dict) -> None:
        if self.validate(data):
            print(f"Sending metrics to Datadog API: {data}")


class CloudWatchExporter(TelemetryExporter):
    
    # 3. METHOD OVERRIDING: Providing the specific "how" for AWS
    def export(self, data: dict) -> None:
        if self.validate(data):
            print(f"Pushing logs to AWS CloudWatch: {data}")


# 4. POLYMORPHISM IN ACTION
def process_telemetry(exporter: TelemetryExporter, batch_data: dict):
    # This function doesn't know (or care) if it's Datadog or CloudWatch. 
    # It just calls .export() and relies on polymorphism to run the right version.
    exporter.export(batch_data)

# Usage:
exporters = [DatadogExporter(), CloudWatchExporter()]
sample_data = {"cpu_usage": 84.2, "status": "healthy"}

for exp in exporters:
    process_telemetry(exp, sample_data)
