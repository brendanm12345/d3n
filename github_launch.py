
import requests
import os 
GITHUB_API_KEY = os.getenv('GITHUB_API_KEY')

def get_comments(url, access_token):
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    comments = []
    
    while url:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            page_comments = response.json()
            comments.extend(page_comments)
            
            # Check if there is a next page of comments
            next_url = response.links.get('next', {}).get('url')
            url = next_url
        else:
            print(f'Error: {response.status_code}')
            break
    
    return comments

# GitHub API endpoint for the specific issue
# issue_url = 'https://api.github.com/repos/arviz-devs/arviz/issues/2345'
issue_url = 'https://github.com/brendanm12345/wordle/issues/4'

def get_issue_details(issue_url, access_token):
    # take the github url and appent api. to the beginning
    issue_url = issue_url.replace('github.com', 'api.github.com/repos')
    # Retrieve the issue details
    response = requests.get(issue_url, headers={'Authorization': f'token {access_token}'})
    full_string = ""

    if response.status_code == 200:
        print(response)
        issue_data = response.json()

        title = issue_data['title']
    
        # Extract the issue description
        description = issue_data['body']
        if description is None:
            description = ''
        full_string += description + '\n'
    
        # Extract the reactions
        reactions = issue_data['reactions']
    
        # Retrieve the comments recursively
        comments_url = issue_data['comments_url']
        comments = get_comments(comments_url, access_token)
    
        for comment in comments:
            if comment['body'] is not None:
                full_string += comment['body'] + '\n'

    else:
        print(f'Error: {response.status_code}')
    return title, full_string

if __name__ == '__main__':
    issue_details = get_issue_details(issue_url, GITHUB_API_KEY)
    print(issue_details)
# issue_details = get_issue_details(issue_url, GITHUB_API_KEY)
# print(issue_details)