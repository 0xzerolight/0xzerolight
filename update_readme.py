#!/usr/bin/env python3
"""Regenerate the project table in README.md from the GitHub API."""
import json
import os
import urllib.request

USER = "0xzerolight"
SKIP = {USER, "anki_miner_assets"}
README = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
START, END = "<!-- projects:start -->", "<!-- projects:end -->"


def fetch_repos():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/repos?type=owner&per_page=100",
        headers={"Accept": "application/vnd.github+json"},
    )
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def render(repos):
    rows = ["| Project | Description | Language | ★ |", "|---|---|---|---|"]
    for r in sorted(repos, key=lambda r: (-r["stargazers_count"], r["name"])):
        desc = (r["description"] or "").replace("|", "\\|")
        rows.append(
            f"| [{r['name']}]({r['html_url']}) | {desc} | {r['language'] or ''} | {r['stargazers_count']} |"
        )
    return "\n".join(rows)


def main():
    repos = [
        r for r in fetch_repos()
        if not r["fork"] and not r["archived"] and r["name"] not in SKIP
    ]
    with open(README) as f:
        text = f.read()
    start = text.index(START) + len(START)
    end = text.index(END)
    with open(README, "w") as f:
        f.write(text[:start] + "\n" + render(repos) + "\n" + text[end:])


if __name__ == "__main__":
    main()
