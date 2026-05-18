from fastapi import BackgroundTasks

from src.models.schemas import AnalyzeRequest, AnalyzeResponse


def _prepare_background_sync(payload: AnalyzeRequest) -> None:
    # Placeholder for future Analytics/Core Business integration.
    _ = payload


def analyze_image(payload: AnalyzeRequest, background_tasks: BackgroundTasks) -> AnalyzeResponse:
    background_tasks.add_task(_prepare_background_sync, payload)

    return AnalyzeResponse(
        detected=True,
        object="person",
        confidence=0.95,
        risk_level="medium",
    )
