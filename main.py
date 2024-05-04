from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from openai import OpenAI
import json
from github_launch import get_issue_details, get_comments
import os

# read file .openaikey
client = OpenAI()

app = FastAPI()

class GitHubIssue(BaseModel):
    title: str
    body: str
    url: str


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


ranked_urls = []
FALLBACK_URLS = [
    "https://github.com/brendanm12345/wordle/issues/4",
    "https://github.com/brendanm12345/wordle/issues/3",
    "https://github.com/brendanm12345/wordle/issues/2",
    "https://github.com/brendanm12345/wordle/issues/1"
]

class GitHubIssue(BaseModel):
    title: str
    body: str
    url: str


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

def issue_to_basemodel(issue_url):
    title, full_string = get_issue_details(issue_url, os.getenv('GITHUB_API_KEY'))
    return GitHubIssue(title=title, body=full_string, url=issue_url)

@app.post("/rank-issues/")
async def rank_issues(issue_urls: List[str]):
    # Ensure that file is cleared before populating with ranked urls 
    with open('links_state.txt', 'w') as file:
        file.write('')

    if not issue_urls:
        issue_urls = FALLBACK_URLS
        print(f"Warning: Defaulting to fallback urls")

    issues = [issue_to_basemodel(issue) for issue in issue_urls]
    try:
        prompt = "\n".join(
            [f"{i + 1}: Title: {issue.title}, Body: {issue.body}, URL: {issue.url}" for i,
                issue in enumerate(issues)]
        )

        messages = [
            {"role": "system", "content": "You are a GitHub issue ranker, skilled in prioritizing issues based on their importance. You only output JSON with no explanation or preamble. Example of response: [\"https://example.com/url1\", \"https://example.com/url2\", ...]. Only output the JSON, nothing else."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0,
        )

        ranked_issues_json = response.choices[0].message.content.strip()
        ranked_issues = json.loads(ranked_issues_json)

        # Write all the ranked urls to links_state.txt 
        ranked_urls = ranked_urls + ranked_issues
        with open('links_state.txt', 'w') as f: 
            for r in ranked_urls: 
                f.write(f'{r}\n')

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/instructions')
async def get_starting_prompt() -> str:
    try: 
        with open('child_prompt.md', 'r') as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Prompt file not found")

@app.get('/rank-issues/top')
async def get_next_issue() -> str:
    with open('links_state.txt', 'r') as file:
        all_links = file.readlines()

    # Remove the first line
    if len(all_links) > 0:
        link = all_links.pop(0)
    else:
        raise HTTPException(status_code=404, detail="No more data :(")

    # Write the remaining lines back to the file
    with open('links_state.txt', 'w') as file:
        file.writelines(all_links)
    
    return link
