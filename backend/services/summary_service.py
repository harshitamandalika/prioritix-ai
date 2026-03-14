import json
from typing import Dict, Any
from services.llm_client import client, GEMINI_MODEL

SYSTEM_PROMPT = """
You are a product feedback analyst.

Your job is to summarize processed app review insights for product and engineering teams.

Return:
1. executive_summary
2. top_pain_points
3. urgent_issues
4. recommended_priorities

Keep the response concise, practical, and business-focused.
Avoid making up facts that are not supported by the provided data.
"""


def generate_feedback_summary(summary_input: Dict[str, Any]) -> str:
    prompt = f"""
Analyze the following processed review data and write a clear product feedback summary.

Data:
{json.dumps(summary_input, indent=2)}

Please include:
- Executive summary
- Top recurring pain points
- Most urgent issues
- Recommended product priorities
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
        },
    )

    return response.text


def generate_structured_feedback_summary(summary_input: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
Analyze the following processed review data and return a JSON object with exactly these keys:
- executive_summary
- top_pain_points
- urgent_issues
- recommended_priorities

Rules:
- top_pain_points must be a list of short strings
- urgent_issues must be a list of short strings
- recommended_priorities must be a list of short strings

Data:
{json.dumps(summary_input, indent=2)}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
        },
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "executive_summary": response.text,
            "top_pain_points": [],
            "urgent_issues": [],
            "recommended_priorities": [],
        }