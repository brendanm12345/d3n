import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

# read file .openaikey
key = open(".openaikey", "r").readline()
client = OpenAI(api_key=key)

app = FastAPI()

class GitHubIssue(BaseModel):
    title: str
    body: str
    url: str


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


ranked_urls = {}

class GitHubIssue(BaseModel):
    title: str
    body: str
    url: str


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.post("/rank-issues/")
async def rank_issues(issues: List[GitHubIssue]):
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
    

@app.get('/rank-issues/top')
async def get_next_issue() -> str:
    if not ranked_urls:
        raise HTTPException(status_code=404, detail="No items stored")
    id, link = ranked_urls[0]
    del ranked_urls[id]
    return link