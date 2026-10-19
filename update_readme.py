#!/usr/bin/env python3
"""Refresh the ⭐ star count on each README line that links a GitHub repo."""
import json
import os
import re
import urllib.request

README = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
REPO = re.compile(r"github\.com/([\w.-]+)/([\w.-]+)")
STAR = re.compile(r"⭐️? *\d*")


def stars(owner, name):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{name}",
        headers={"Accept": "application/vnd.github+json"},
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["stargazers_count"]


def refresh(line):
    repo = REPO.search(line)
    if not repo or not STAR.search(line):
        return line
    return STAR.sub(f"⭐ {stars(*repo.groups())}", line, count=1)


def main():
    with open(README) as f:
        text = "".join(refresh(line) for line in f)
    with open(README, "w") as f:
        f.write(text)


if __name__ == "__main__":
    main()
