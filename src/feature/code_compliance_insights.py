import os
import json
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github import Github
from openai import OpenAI

app = FastAPI()

class ComplianceRule(BaseModel):
    id: str
    description: str
    severity: str

class ComplianceInsight(BaseModel):
    rule_id: str
    file_path: str
    line_number: int
    description: str

class CodeComplianceInsights:
    def __init__(self, github_token: str, openai_api_key: str):
        self.github = Github(github_token)
        self.openai = OpenAI(openai_api_key)

    def analyze_code(self, repository: str, commit_hash: str) -> List[ComplianceInsight]:
        # Get the commit and repository from GitHub
        repo = self.github.get_repo(repository)
        commit = repo.get_commit(commit_hash)

        # Get the files changed in the commit
        files = commit.files

        # Initialize the list of compliance insights
        insights = []

        # Loop through each file
        for file in files:
            # Get the file contents
            file_contents = repo.get_file_contents(file.filename, commit_hash).content

            # Decode the file contents
            file_contents = file_contents.decode('utf-8')

            # Split the file contents into lines
            lines = file_contents.split('\n')

            # Loop through each line
            for i, line in enumerate(lines):
                # Check for compliance issues
                compliance_issues = self.check_compliance(line)

                # Loop through each compliance issue
                for issue in compliance_issues:
                    # Create a compliance insight
                    insight = ComplianceInsight(
                        rule_id=issue['rule_id'],
                        file_path=file.filename,
                        line_number=i + 1,
                        description=issue['description']
                    )

                    # Add the insight to the list
                    insights.append(insight)

        return insights

    def check_compliance(self, line: str) -> List[Dict]:
        # Define the compliance rules
        rules = [
            {
                'id': 'COMPLIANCE-1',
                'description': 'Hardcoded credentials',
                'pattern': r'password\s*=\s*["\'].*["\']'
            },
            {
                'id': 'COMPLIANCE-2',
                'description': 'Insecure deserialization',
                'pattern': r'pickle\s*.\s*load'
            }
        ]

        # Initialize the list of compliance issues
        issues = []

        # Loop through each rule
        for rule in rules:
            # Check if the line matches the rule pattern
            if re.search(rule['pattern'], line):
                # Create a compliance issue
                issue = {
                    'rule_id': rule['id'],
                    'description': rule['description']
                }

                # Add the issue to the list
                issues.append(issue)

        return issues

# Create an instance of the CodeComplianceInsights class
compliance_insights = CodeComplianceInsights(
    github_token=os.environ['GITHUB_TOKEN'],
    openai_api_key=os.environ['OPENAI_API_KEY']
)

# Define the API endpoint
@app.post("/compliance_insights")
async def get_compliance_insights(repository: str, commit_hash: str):
    # Analyze the code
    insights = compliance_insights.analyze_code(repository, commit_hash)

    # Return the insights
    return insights