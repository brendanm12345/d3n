from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from openai import OpenAI
import json
from github_launch import get_issue_details, get_comments
import os
from s3 import get_state, save_state

# read file .openaikey
client = OpenAI()

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

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
async def rank_issues(in_issue_urls: List[str]):
    if in_issue_urls and len(in_issue_urls) > 0:
        issue_urls = in_issue_urls
    else:
        issue_urls = [
            "https://github.com/brendanm12345/wordle/issues/4",
            "https://github.com/brendanm12345/wordle/issues/3",
            "https://github.com/brendanm12345/wordle/issues/2",
            "https://github.com/brendanm12345/wordle/issues/1"
        ]
    issues = [issue_to_basemodel(issue) for issue in issue_urls]
    try:
        prompt = "\n".join(
            [f"{i + 1}: Title: {issue.title}, Body: {issue.body}, URL: {issue.url}" for i,
                issue in enumerate(issues)]
        )

        messages = [
            {"role": "system", "content": "You are a GitHub issue ranker, skilled in prioritizing issues based on their difficulty. Easiest issues should come first, and order them from easiest to hardest. You only output JSON with no explanation or preamble. Example of response: [\"https://example.com/url1\", \"https://example.com/url2\", ...]. Only output the JSON, nothing else."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0,
        )

        ranked_issues_json = response.choices[0].message.content.strip()
        ranked_issues = json.loads(ranked_issues_json)
        save_state(ranked_issues)
        return 'ok'
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/instructions.devin.md')
async def get_starting_prompt() -> str:
    try: 
        with open('child_prompt.md', 'r') as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Prompt file not found")

@app.get('/rank-issues/top')
async def get_next_issue() -> str:
    all_links = get_state()
    # Remove the first line
    if len(all_links) > 0:
        link = all_links.pop(0)
    else:
        raise HTTPException(status_code=404, detail="No more data :(")
    
    save_state(all_links)    
    return RedirectResponse(url=link)
