from typing import List, Annotated
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from openai import OpenAI
import json
from github_launch import get_issue_details, get_comments, get_all_issues
import os
from s3 import get_state, save_state
from fastapi.middleware.cors import CORSMiddleware
import requests

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
async def repository(repository=FALLBACK_URL):
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
        state = get_state()
        state['links'] = ranked_issues
        save_state(state)
        return ranked_issues
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


def issue_to_basemodel(issue_url):
    title, full_string = get_issue_details(
        issue_url, os.getenv('GITHUB_API_KEY'))
    return GitHubIssue(title=title, body=full_string, url=issue_url)


@app.get('/instructions.devin.md')
async def get_starting_prompt() -> str:
    try:
        with open('child_prompt.md', 'r') as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Prompt file not found")


@app.get('/instructions/parent')
async def orchestrate() -> str:
    state = get_state()
    if 'repository' not in state or len(state['repository']) == 0:
        return 'No repository set. Please poll this endpoint again in 10 seconds to re-try.'
    if 'links' not in state or len(state['links']) == 0:
        return 'No links set. Please poll this endpoint again in 10 seconds to re-try.'
    return """
    Repeat this process 3 times. Open a new tab. Type the following text into the textbox: "Open https://d3n.fly.dev/instructions.devin.md and follow instructions" and hit enter. Do NOT visit this link yourself. Only type it into the chat box and hit enter.
    """

@app.post('/reset')
async def reset():
    state = get_state()
    state['links'] = []
    state['repository'] = ''
    save_state(state)
    return 'ok'

@app.get('/rank-issues/pop')
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


@app.post('/success')
async def success(issue: Annotated[str, Body()], description: Annotated[str, Body()]):

    url = "https://interactify.email/api/internal/email?from=soham"
    headers = {'Content-Type': 'application/json'}
    data = {
        "subject": f"Success: {issue}",
        "body": description,
        "timeout": 1
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    return 'ok'
