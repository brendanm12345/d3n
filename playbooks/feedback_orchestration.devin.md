Follow this Playbook: Closing out issues on github.

## Procedure
0. Create a file log.txt, where you record everything that you do, including code execution, terminal commands, and reasoning. 
1. Open https://d3n.fly.dev/rank-issues/pop. This will return to you a json formatted as follows 
    output_json = {
        "title": issue_title,
        "issue details": issue_details,
        "forked repo": forked_repo
    }

    - First, clone the repository using gh repo clone. 
    - Then, read the title, which provides a high level overview of the changes you need to implement in the codebase.
    - Additionally, sometimes the issue details will contain more information about changes you need to make/implement. 

2. Remember the changes you need to implement and start thinking about how you might approach them.
3. Create an outline of steps you would need to do in order to fix the issue.
4. Execute the task.
5. If the task is successful, make a pull request on the PR. Additionally, also query the API endpoint by making a post request to https://d3n.fly.dev/success with the following JSON body: { "issue": "[issue link]", "description": "[description of the task you did] }
6. If you encounter any installation issues, pip install those packages.
7. If unsuccessful, make a post request to now make a post request to d3n.fly.dev/failure/ and pass in the issue url, the playbook used, and your reasoning for everything that went wrong.
8. If successful, create a pull request for the forked repository to show what you changed.
9. go back to task 1.
