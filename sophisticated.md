Playbook: Checking cognition's follower count on twitter

## Procedure
1. Push a get request to localhost:3000/tasks/get
2. The get request will return a url containing the github issue I want you to work on. 
3. Read the issue and understand everything that you have to do for it. 
4. Create an outline of steps you would need to do in order to fix the issue. 
5. Execute the task. 
6. If the task is successful make a post request to localhost:3000/tasks/push_successful with the issue id. 
7. If unsuccessful, create a new plan and try to execute the task again. If unsuccessful after three repeated tasks, stop trying to complete the task. 
8. Once you finish tasks 1-7, go back to task 1 to request a new task from localhost:3000/tasks/get.