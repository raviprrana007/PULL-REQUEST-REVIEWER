# System Architecture - AI Pull Request Reviewer

## Overview
An automated PR Reviewer designed for Track B (Developer Productivity Tools). It intercepts GitHub pull request events, parses modified diff hunks, and uses LLM backends to post actionable code feedback.

## Tech Stack
- **Language**: Python 3.11+
- **LLM Provider**: NVIDIA Build API / Google AI Studio (OpenAI Compatible)
- **GitHub SDK**: PyGithub
- **Data Validation**: Pydantic v2
- **Testing**: Pytest & GitHub Actions CI

## System Flow
1. **Trigger**: `pull_request` event fires GitHub Action (`pr_reviewer.yml`).
2. **Skill Layer (`diff_analyzer.py`)**: Fetches PR payload and filters out removed files/non-patch hunks.
3. **Agent Layer (`pr_reviewer.py`)**: Validates API key at startup, formats prompt, enforces output schemas, and invokes LLM endpoint.
4. **Action**: Posts inline diff reviews (with correct `side: RIGHT` field) or falls back to issue comments if line matching fails, logging the failure reason.
