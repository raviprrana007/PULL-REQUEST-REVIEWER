import os
import json
from openai import OpenAI
from pydantic import BaseModel, Field


class ReviewComment(BaseModel):
    path: str = Field(description="Exact file path")
    line: int = Field(description="Line number in the new file")
    body: str = Field(description="Comment explaining the bug or fix")


class ReviewResponse(BaseModel):
    comments: list[ReviewComment]


class PRReviewerAgent:
    """Custom Agent: Generates AI reviews using free OpenAI-compatible endpoints."""

    def __init__(self):
        self.api_key = (
            os.getenv("NVIDIA_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("GEMINI_API_KEY")
        )
        if not self.api_key:
            raise ValueError(
                "No API key found. Set NVIDIA_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY."
            )
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://integrate.api.nvidia.com/v1")
        self.model = os.getenv("LLM_MODEL", "meta/llama-3.1-70b-instruct")

    def review_diff(self, diff_payload: str) -> ReviewResponse:
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        prompt = f"""
You are a senior code reviewer. Review this diff and output valid JSON in this structure:
{{
  "comments": [
    {{"path": "exact/file/path.py", "line": 10, "body": "explanation"}}
  ]
}}

Rules:
1. ONLY comment on newly added lines (+).
2. Be polite, concise, and clear.

Code Change:
{diff_payload}
"""
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        if not response.choices or response.choices[0].message.content is None:
            raise ValueError("Empty or null response received from LLM.")

        raw_json = json.loads(response.choices[0].message.content)
        return ReviewResponse(**raw_json)
