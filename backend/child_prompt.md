Follow this Playbook: Closing out issues on github.

## Procedure

1. Open https://d3n.fly.dev/rank-issues/pop. It will redirect you to a GitHub issue website. If it gives you a 404 / no issue/items found, then congrats! You are ALL done. Skip the rest of the steps and await further user input.
2. Read the issue and understand everything that you have to do for it.
3. Understand the rest of the codebase by reading about it from the website.
4. Create an outline of steps you would need to do in order to fix the issue.
5. Execute the task.
6. If the task is successful make a post request to https://d3n.fly.dev/success with the following JSON body: { "issue": "[issue link]", "description": "[description of the task you did]" }
7. If you encounter any installation issues, pip install those packages.
8. If unsuccessful, create a new plan and try to execute the task again. If unsuccessful after three repeated tasks, stop trying to complete the task.
9. Once you finish tasks 1-7, go back to task 1.
