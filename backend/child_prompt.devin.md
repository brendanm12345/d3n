Follow this Playbook: Closing out issues on github.

## Procedure

1. Open https://d3n.fly.dev/rank-issues/pop.

   - First, clone the repository using gh repo clone.
   - Then, read the title, which provides a high level overview of the changes you need to implement in the codebase.
   - Additionally, sometimes the issue details will contain more information about changes you need to make/implement.

2. Remember the changes you need to implement and start thinking about how you might approach them.
3. Create an outline of steps you would need to do in order to fix the issue.
4. Execute the task.
5. If the task is successful make a post request to https://d3n.fly.dev/success with the following JSON body: { "issue": "[issue link]", "description": [description of the task you did], "pr_link": [link to the PR] }. If it fails, make a post request to https://d3n.fly.dev/failure with the following JSON body: { "issue": "[issue link]", "suspected_reason": [why you think the task failed]
6. If you encounter any installation issues, pip install those packages.
7. If unsuccessful, create a new plan and try to execute the task again. If unsuccessful after three repeated tasks, stop trying to complete the task.
8. Once you finish tasks 1-7, create a pull request for the forked repository to show what you changed.
9. go back to task 1.
