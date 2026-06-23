"""
Observability: structured logging + OpenTelemetry tracing to Cloud Trace.

Call setup_telemetry() once at application startup. Subsequent calls are safe.
"""

import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from config import APP_NAME, LOG_LEVEL

_tracer: trace.Tracer | None = None


def setup_telemetry() -> trace.Tracer:
    """Initialise structured logging and Cloud Trace tracing. Idempotent.

    Returns:
        A named OpenTelemetry Tracer for the application.
    """
    global _tracer
    if _tracer is not None:
        return _tracer

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    exporter = CloudTraceSpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    _tracer = trace.get_tracer(APP_NAME)
    return _tracer


def trace_agent_call(tracer: trace.Tracer, agent_name: str, user_id: str, session_id: str):
    """Context manager: wraps an agent invocation in a named trace span."""
    return tracer.start_as_current_span(
        f"agent.{agent_name}",
        attributes={
            "agent.name": agent_name,
            "user.id":    user_id,
            "session.id": session_id,
            "app.name":   APP_NAME,
            "cloud":      "gcp",
        },
    )
