# AI Pull Request Reviewer

An automated, agentic code reviewer built for **Track B: Developer Productivity Tools**.

It automatically inspects pull request diffs on GitHub, parses modified lines, and posts actionable, structured code quality and security feedback directly into the PR thread using free LLM backends.

---

## Key Features

* **Diff Analysis Skill**: Parses incoming pull request patch payloads into structured file hunks.
* **AI PR Reviewer Agent**: Evaluates modified lines for bugs, unhandled exceptions, raw debug logs, and exposed secrets.
* **Inline GitHub Comments**: Posts line-specific feedback directly onto the pull request diff.
* **Graceful Fallback**: Automatically posts a high-level summary comment if line matching fails, with logged failure details.
* **Free-Tier Compatible**: Built to run seamlessly on free-tier LLM endpoints like NVIDIA Build and Google AI Studio.

---

## Architecture & Non-Negotiables Checkpoints

This repository satisfies all **5 Non-Negotiable Entry Gate Criteria**:

1. **`ARCHITECTURE.md`**: System design, data model, and flow diagrams.
2. **`.clinerules` & `AGENTS.md`**: Agent constitution and operational rules.
3. **Working Code**: Runnable Python application driven by GitHub Actions.
4. **`AGENTS_AND_SKILLS.md`**: Complete registry documenting custom agents and skills.
5. **Green CI/CD Pipeline**: GitHub Actions workflow (`ci.yml`) running static code analysis and Pytest suite.

---

## Local Setup & Execution

### Prerequisites
* Python 3.11+
* Git

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

pip install -r requirements.txt
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GITHUB_TOKEN` | Yes | GitHub token with `pull-requests: write` permission |
| `NVIDIA_API_KEY` | Yes* | NVIDIA Build API key |
| `OPENAI_API_KEY` | Yes* | OpenAI-compatible API key (alternative) |
| `GEMINI_API_KEY` | Yes* | Google AI Studio API key (alternative) |
| `OPENAI_BASE_URL` | No | Custom LLM base URL (default: NVIDIA endpoint) |
| `LLM_MODEL` | No | Model name (default: `meta/llama-3.1-70b-instruct`) |

*At least one API key must be set.

### Running Tests
```bash
PYTHONPATH=. pytest tests/
```

### Running Linting
```bash
flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
```

---

## GitHub Actions Setup

1. Go to your repository **Settings → Secrets and variables → Actions**.
2. Add `NVIDIA_API_KEY` (or another supported key) as a repository secret.
3. The `GITHUB_TOKEN` is provided automatically by GitHub Actions.
4. Open a pull request — the reviewer will trigger automatically.
