from typing import List, Annotated, Dict
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from openai import OpenAI
import json
from github_launch import get_issue_details, get_comments, get_all_issues
import os
from s3 import get_state, save_state, create_patch
from fastapi.middleware.cors import CORSMiddleware
import requests
from fork_repo import fork_repository

client = OpenAI()
FALLBACK_REPO = "brendanm12345/wordle"
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


class GitHubIssue(BaseModel):
    title: str
    body: str
    url: str
    playbook: str = None


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# @app.post('/repository')
# def set_repository(repository: str):
#     state = get_state()
#     state['repository'] = repository
#     all_issues = get_all_issues(repository)
#     state['links'] = all_issues
#     save_state(state)
    # return 'ok'

FALLBACK_URLS = [
    "https://github.com/brendanm12345/wordle/issues/4",
    "https://github.com/brendanm12345/wordle/issues/3",
    "https://github.com/brendanm12345/wordle/issues/2",
    "https://github.com/brendanm12345/wordle/issues/1"
]


@app.post("/repository/")
async def repository(repository: str = FALLBACK_REPO):
    state = get_state()
    state['repository'] = repository
    issue_urls = get_all_issues(repository)
    issues = [issue_to_basemodel(issue) for issue in issue_urls]
    try:
        prompt = "\n".join(
            [f"{i + 1}: Title: {issue.title}, Body: {issue.body}, URL: {issue.url}" for i,
                issue in enumerate(issues)]
        )
        messages = [
            {"role": "system",
                "content": "You are a GitHub issue ranker, skilled in prioritizing issues based on their difficulty. Easiest issues should come first, and order them from easiest to hardest. You only output JSON with no explanation or preamble. Example of response: [\"https://example.com/url1\", \"https://example.com/url2\", ...]. Only output the JSON, nothing else."},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0,
        )
        ranked_issues_json = response.choices[0].message.content.strip()
        ranked_issues = json.loads(ranked_issues_json)
        state['issues'] = [{"url": issue, "playbook": None}
                           for issue in ranked_issues]  # Updated structure
        save_state(state)
        return ranked_issues
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def issue_to_basemodel(issue_url):
    title, body = get_issue_details(issue_url, os.getenv('GITHUB_API_KEY'))
    return GitHubIssue(title=title, body=body, url=issue_url)


@app.get('/instructions.devin.md')
async def get_starting_prompt() -> str:
    try:
        with open('child_prompt.devin.md', 'r') as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Prompt file not found")


@app.get('/instructions/parent')
async def orchestrate() -> str:
    state = get_state()
    if 'repository' not in state or not state['repository']:
        return 'No repository set. Please poll this endpoint again to re-try.'
    if 'issues' not in state or not state['issues']:
        return 'No issues set. Please poll this endpoint again to re-try.'
    return """
    Repeat this process 3 times. Open a new tab to https://preview.devin.ai. Type the following text into the textbox: "Open https://d3n.fly.dev/instructions.devin.md and follow instructions" and hit enter. Do NOT visit this link yourself. Only type it into the chat box and hit enter.
    """


@app.post('/reset')
async def reset():
    state = get_state()
    state['issues'] = []
    state['repository'] = ''
    state['failures'] = []
    state['successes'] = []
    save_state(state)
    return 'ok'


@app.get('/rank-issues/pop')
async def get_next_issue() -> dict:
    state = get_state()
    if state['issues']:
        current_issue = state['issues'].pop(0)
        save_state(state)
        issue_title, issue_details = get_issue_details(
            current_issue['url'], os.getenv('GITHUB_API_KEY'))
        forked_repo = fork_repository(
            state['repository'], 'akshgarg7', os.getenv('GITHUB_API_KEY'))
        return {
            "title": issue_title,
            "issue details": issue_details,
            "forked repo": forked_repo
        }
    else:
        raise HTTPException(status_code=404, detail="No more issues :)")

@app.get('/rank-issues/peek')
async def peek_next_issue() -> str:
    state = get_state()
    if state['issues']:
        return state['issues'][0]['url']
    else:
        raise HTTPException(status_code=404, detail="No more issues :(")


@app.post('/success')
async def success(issue: Annotated[str, Body()], description: Annotated[str, Body()], pr_link: Annotated[str, Body()]):
    url = "https://interactify.email/api/internal/email?from=soham"
    headers = {'Content-Type': 'application/json'}
    requests.post(url, headers=headers, data=json.dumps({
        "subject": f"Success: {issue}",
        "body": description + "<br/><br/>" + pr_link,
        "timeout": 10
    }))
    state = get_state()
    state['successes'].append(issue)
    save_state(state)
    return 'ok'


@app.post('/failure')
async def failure(issue: Annotated[str, Body()], playbook_used: Annotated[str, Body()], suspected_reason: Annotated[str, Body()]):
    failure = {
        "issue": issue,
        "playbook_used": playbook_used,
        "suspected_reason": suspected_reason
    }
    state = get_state()
    state['failures'].append(failure)
    save_state(state)
    return 'ok'


@app.get('/retry')
async def get_next_failure(): 
    state = get_state()
    
    if len(state['failures']) == 0: 
        raise HTTPException(status_code=404, detail='No more failed tasks! Please call this endpoint again to check again.')

    next_failure = state['failures'].pop(0)

    save_state(state)

    return next_failure


@app.post('/add_retry/{info}')
def add_retry(info: List[str]):
    # Ensure orchestrator creates a list info consisting of the url (idx 0) and the revised playbook (idx 1)
    state = get_state()
    
    issue = {'url': info[0], 'playbook': info[1]}
    state['issues'].append(issue)

    save_state()

    return 'ok'
