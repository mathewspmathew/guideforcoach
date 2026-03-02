"""
Router: /pipeline
Exposes endpoints to trigger the ML pipeline (data processing + model training).
"""
from fastapi import APIRouter, HTTPException
from api.schemas import PipelineRunResponse
from main_pipeline import run_pipeline

router = APIRouter(prefix="/pipeline", tags=["Pipeline"])


@router.post("/run", response_model=PipelineRunResponse, summary="Run the ML pipeline")
def run_pipeline_endpoint():
    """
    Triggers the full Moneyball pipeline:
    1. Load & clean data
    2. Train the similarity model
    3. Run a sanity-check inference

    This is a blocking call — it may take a minute depending on dataset size.
    """
    try:
        run_pipeline()
        return PipelineRunResponse(
            status="success",
            message="Pipeline completed successfully. Model is ready for inference.",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
