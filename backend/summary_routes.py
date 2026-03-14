from fastapi import APIRouter, HTTPException
from summary_schema import SummaryRequest, SummaryResponse
from services.review_service import get_reviews_for_summary
from services.analytics_service import build_summary_input
from services.summary_service import (
    generate_feedback_summary,
    generate_structured_feedback_summary,
)

router = APIRouter(prefix="/summary", tags=["summary"])


@router.post("/", response_model=SummaryResponse)
async def summarize_feedback(request: SummaryRequest):
    try:
        reviews = get_reviews_for_summary(max_reviews=request.max_reviews)

        if not reviews:
            raise HTTPException(status_code=404, detail="No reviews found for summarization.")

        summary_input = build_summary_input(
            reviews=reviews,
            include_sample_reviews=request.include_sample_reviews
        )

        summary_text = generate_feedback_summary(summary_input)
        structured_summary = generate_structured_feedback_summary(summary_input)

        return SummaryResponse(
            summary=summary_text,
            structured_summary=structured_summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))