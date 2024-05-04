from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from openai import OpenAI
import json
from github_launch import get_issue_details, get_comments

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


ranked_urls = {}
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
            {"role": "system", "content": "You are a GitHub issue ranker, skilled in prioritizing issues based on their importance. You only output JSON with no explanation or preamble."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )

        ranked_issues_json = response.choices[0].message.content.strip()
        ranked_issues = json.loads(ranked_issues_json)

        print(ranked_issues)

        ranked_urls = {str(i+1): issue['url']
                       for i, issue in enumerate(ranked_issues['ranked_issues'])}
        
        # currently adding repeat urls to the dictionary
        return ranked_urls
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/instructions')
async def get_starting_prompt() -> str:
    with open('child_prompt.md', 'r') as file:
        return file.read()
    raise HTTPException(status_code=404, detail="Prompt file not found")

@app.get('/rank-issues/top')
async def get_next_issue() -> str:
    if not ranked_urls:
        raise HTTPException(status_code=404, detail="No items stored")
    id, link = ranked_urls[0]
    del ranked_urls[id]
    return RedirectResponse(link)
