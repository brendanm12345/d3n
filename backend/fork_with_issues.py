from github import Github
import os

def copy_issues(source_repo, destination_repo, token):
    """
    Copies issues from the source repository to the destination repository.

    Args:
    source_repo (str): Full name of the source repository (e.g., 'octocat/Hello-World').
    destination_repo (str): Full name of the destination repository (e.g., 'your_username/forked-repo').
    token (str): GitHub personal access token for authentication.
    """
    g = Github(token)

    # try:
    breakpoint()
    src = g.get_repo(source_repo)
    dest = g.get_repo(destination_repo)

    # Fetch issues from source repository
    issues = src.get_issues(state='all')  # Get both open and closed issues

    for issue in issues:
        # Check if the issue is not a pull request
        if not issue.pull_request:
            labels = [label.name for label in issue.labels]
            # Create the same issue in the destination repository
            dest.create_issue(
                title=issue.title,
                body=issue.body,
                labels=labels,
                assignee=issue.assignee.login if issue.assignee else None
            )
    print("Issues have been copied successfully.")
    # except Exception as e:
        # print(f"An error occurred: {str(e)}")

# Example usage:
repo = 'arviz-devs/arviz'
copy_issues(repo, 'akshgarg7', os.getenv('GITHUB_API_KEY'))