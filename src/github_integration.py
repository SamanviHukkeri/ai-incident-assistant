import os

from github import Github
from dotenv import load_dotenv

load_dotenv()


class GitHubIntegration:

    def __init__(self):

        self.repo = None

        try:

            token = os.getenv("GITHUB_TOKEN")

            self.repo_name = os.getenv("GITHUB_REPO")

            if token and self.repo_name:

                self.github = Github(token)

                self.repo = self.github.get_repo(self.repo_name)

                print("GitHub integration initialized")

            else:

                print("GitHub environment variables not found")

        except Exception as e:

            print(f"GitHub initialization failed: {e}")

    def create_issue(self, analysis_result):

        if not self.repo:

            return None

        try:

            title = f"[AI Incident] {analysis_result['root_cause']}"

            body = f"""
# AI Incident Analysis

## Root Cause
{analysis_result['root_cause']}

## Severity
{analysis_result['severity']}

## Suggested Fixes
{chr(10).join(['- ' + x for x in analysis_result['suggested_fixes']])}

## Affected APIs
{chr(10).join(['- ' + x for x in analysis_result['affected_apis']])}
"""

            issue = self.repo.create_issue(
                title=title,
                body=body
            )

            return issue.html_url

        except Exception as e:

            print(f"GitHub issue creation failed: {e}")

            return None