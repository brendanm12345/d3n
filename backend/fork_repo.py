import os 
from github import Github
from dotenv import load_dotenv

os.environ.pop("GITHUB_API_KEY", None)
load_dotenv()

def fork_repository(original_repo, username, token):
    """
    Forks a given repository to the specified user's GitHub account.
    
    Args:
    original_repo (str): Full name of the repository to fork (e.g., 'octocat/Hello-World').
    username (str): GitHub username to which the repository will be forked.
    token (str): GitHub personal access token for authentication.

    Returns:
    str: URL of the forked repository.
    """
    # Authenticate with GitHub using the provided token
    g = Github(token)

    try:
        breakpoint()
        # Get the repository to fork
        repo = g.get_repo(original_repo)

        # Fork the repository to the user's account
        forked_repo = repo.create_fork()
        
        # Return the HTML URL of the forked repository
        return forked_repo.html_url
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage:
repo = 'arviz-devs/arviz'
print(os.getenv("GITHUB_API_KEY"))
print(fork_repository(repo, 'akshgarg7', os.getenv('GITHUB_API_KEY')))
