import os
import subprocess
from openai import OpenAI
from github import Github

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def get_diff():
    subprocess.run(["git", "fetch", "origin", "main"], check=False)

    result = subprocess.run(
        ["git", "diff", "origin/main...HEAD"],
        capture_output=True,
        text=True,
    )

    return result.stdout[:12000]

def get_ai_review(diff):
    prompt = f"""
You are a senior DevSecOps code reviewer.

Review this pull request diff. Focus on:
- bugs
- security risks
- Docker issues
- Azure deployment issues
- CI/CD mistakes
- simple improvement suggestions

Keep feedback short and practical.

Diff:
{diff}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content

def post_pr_comment(review_text):
    github_token = os.environ["GITHUB_TOKEN"]
    repo_name = os.environ["REPO_NAME"]
    pr_number = int(os.environ["PR_NUMBER"])

    gh = Github(github_token)
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    body = f"""## AI PR Review

{review_text}
"""

    pr.create_issue_comment(body)

def main():
    diff = get_diff()

    if not diff.strip():
        print("No diff found to review.")
        return

    review = get_ai_review(diff)

    print("\nAI PR REVIEW:\n")
    print(review)

    post_pr_comment(review)
    print("Posted AI review comment to PR.")

if __name__ == "__main__":
    main()