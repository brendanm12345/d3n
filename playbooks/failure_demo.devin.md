You are dealing with failures that were encountered from other devin runs. Make a get request to https://d3n.fly.dev/retry to figure out the url of the files, which failed. Also examine the failure_reason key for the issue object to extract the reason for the error. Use this to come up with a potential solution. Then, make a post request to https://d3n.fly.dev/add_retry to reschedule this job, making sure to pass in two arguments: {
        "issue": [insert issue url here],
        "new_plan": [insert the plan to resolve the issues here]: 
}