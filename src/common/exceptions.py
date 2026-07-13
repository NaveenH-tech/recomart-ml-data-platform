class PipelineException(Exception):
    """Base exception."""


class ValidationException(PipelineException):
    """Validation errors."""


class IngestionException(PipelineException):
    """Ingestion errors."""
