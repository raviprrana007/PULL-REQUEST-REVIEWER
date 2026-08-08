# Custom Agents and Custom Skills Registry

## Custom Agent
- **Name**: `PRReviewerAgent`
- **Location**: `src/agents/pr_reviewer.py`
- **Description**: Handles context construction, communicates with LLM providers using structured JSON schemas, and posts reviews via PyGithub.

## Custom Skill
- **Name**: `DiffAnalyzer`
- **Location**: `src/skills/diff_analyzer.py`
- **Description**: Parses raw unified git diffs into structured file-by-file hunk objects containing added line references.
