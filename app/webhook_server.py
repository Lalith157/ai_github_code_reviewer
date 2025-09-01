from flask import Flask, request
import os
from app.ai_reviewer import review_pull_request
from app.github_commenter import post_review_comments

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def github_webhook():
    event = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event == "pull_request" and payload["action"] in ["opened", "synchronize"]:
        repo = payload["repository"]["full_name"]
        pr_number = payload["number"]
        comments = review_pull_request(repo, pr_number)
        post_review_comments(repo, pr_number, comments)

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(port=5000)
