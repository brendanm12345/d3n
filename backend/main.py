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

@app.post('/repository')
def set_repository(repository: str):
    state = get_state()
    state['repository'] = repository
    save_state(state)
    return 'ok'

FALLBACK_URLS = [
    "https://github.com/brendanm12345/wordle/issues/4",
    "https://github.com/brendanm12345/wordle/issues/3",
    "https://github.com/brendanm12345/wordle/issues/2",
    "https://github.com/brendanm12345/wordle/issues/1"
]

@app.post("/rank-issues/")
async def rank_issues(issue_urls: List[str] = FALLBACK_URLS):
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
        state = get_state()
        state['links'] = ranked_issues
        save_state(state)
        return 'ok'
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))



def issue_to_basemodel(issue_url):
    title, full_string = get_issue_details(issue_url, os.getenv('GITHUB_API_KEY'))
    return GitHubIssue(title=title, body=full_string, url=issue_url)


@app.get('/instructions.devin.md')
async def get_starting_prompt() -> str:
    try: 
        with open('child_prompt.md', 'r') as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Prompt file not found")

@app.get('/rank-issues/top')
async def get_next_issue() -> str:
    state = get_state()
    # Remove the first line
    if len(state['links']) > 0:
        link = state['links'].pop(0)
    else:
        raise HTTPException(status_code=404, detail="No more data :(")
    
    save_state(state)    
    return RedirectResponse(url=link)

@app.get('/rank-issues/peek')
async def peek_next_issue() -> str:
    state = get_state() 
    
    if len(state['links']) > 0: 
        return state['links'][0]
    else: 
        raise HTTPException(status_code=404, detail="No more data :(")

