from github import Github
import os

gh = Github(os.getenv("GITHUB_TOKEN"))

def post_review_comments(repo_name, pr_number, comments):
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    review_comments = []
    for c in comments:
        review_comments.append({
            "path": c["path"],
            "position": c["position"],
            "body": c["body"]
        })

    pr.create_review(
        body="🤖 Automated AI Code Review",
        event="COMMENT",
        comments=review_comments
    )
