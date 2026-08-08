import os
import json
import sys
from dotenv import load_dotenv
load_dotenv()
from github import Github, GithubException, Auth
from src.skills.diff_analyzer import DiffAnalyzer
from src.agents.pr_reviewer import PRReviewerAgent


def main():
    github_token = os.getenv("GITHUB_TOKEN")
    event_path = os.getenv("GITHUB_EVENT_PATH")
    nvidia_api = os.getenv("NVIDIA_API_KEY")
    if not all([github_token, event_path]):
        print("Missing required environment variables: GITHUB_TOKEN, GITHUB_EVENT_PATH.")
        sys.exit(1)

    with open(event_path, "r") as f:
        event_data = json.load(f)

    if "pull_request" not in event_data:
        print("Not a pull request event. Exiting.")
        return

    pr_number = event_data["pull_request"]["number"]
    repo_name = event_data["repository"]["full_name"]

    auth = Auth.Token(github_token)
    gh = Github(auth=auth)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    head_commit = repo.get_commit(pr.head.sha)

    diff_payload = DiffAnalyzer.extract_patch_payload(pr.get_files())
    if not diff_payload.strip():
        print("No code changes detected.")
        return

    try:
        agent = PRReviewerAgent()
    except ValueError as e:
        print(f"Agent initialization failed: {e}")
        sys.exit(1)

    try:
        review_data = agent.review_diff(diff_payload)
    except Exception as e:
        print(f"Agent execution failed: {e}")
        sys.exit(1)

    if not review_data.comments:
        print("Code looks good!")
        return

    comments = [
        {
            "path": c.path,
            "line": c.line,
            "side": "RIGHT",
            "body": f"**AI Review:**\n\n{c.body}",
        }
        for c in review_data.comments
    ]

    try:
        pr.create_review(commit=head_commit, event="COMMENT", comments=comments)
        print("Posted inline review comments successfully!")
    except GithubException as e:
        print(f"Inline review failed ({e.status} {e.data}), falling back to issue comment.")
        fallback_body = "### AI Code Review Summary\n\n"
        for c in review_data.comments:
            fallback_body += f"- **`{c.path}` (Line {c.line}):** {c.body}\n"
        pr.create_issue_comment(fallback_body)
        print("Posted fallback summary comment.")


if __name__ == "__main__":
    main()
