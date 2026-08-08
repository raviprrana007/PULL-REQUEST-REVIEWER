import pytest
from src.agents.pr_reviewer import ReviewComment, ReviewResponse


def test_pydantic_schema():
    comment = ReviewComment(path="src/main.py", line=12, body="Avoid raw print statements.")
    response = ReviewResponse(comments=[comment])

    assert len(response.comments) == 1
    assert response.comments[0].path == "src/main.py"
    assert response.comments[0].line == 12
    assert response.comments[0].body == "Avoid raw print statements."


def test_review_response_empty_comments():
    response = ReviewResponse(comments=[])
    assert response.comments == []


def test_review_comment_fields():
    comment = ReviewComment(path="src/skills/diff_analyzer.py", line=5, body="Missing return type hint.")
    assert comment.path == "src/skills/diff_analyzer.py"
    assert comment.line == 5
    assert comment.body == "Missing return type hint."
