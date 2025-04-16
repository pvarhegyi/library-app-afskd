import os
from fastapi import FastAPI
from models.base import Base
from db.database import engine
from routers import books_api, borrowers_api
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

exporter = ConsoleMetricExporter()
reader = PeriodicExportingMetricReader(exporter)

resource = Resource(attributes={"service.name": "library-api"})
provider = MeterProvider(resource=resource, metric_readers=[reader])

metrics.set_meter_provider(provider)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library API",
    description="Simple library management system with books and borrowers.",
    version="1.0.0",
)

# Routerek regisztrálása
app.include_router(books_api.router, prefix="/api")
app.include_router(borrowers_api.router, prefix="/api")

FastAPIInstrumentor.instrument_app(app)
