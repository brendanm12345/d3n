import boto3
import json

def get_state():
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket='soham-govande', Key='d3n-state.json')
        return json.loads(obj['Body'].read().decode('utf-8'))
    except Exception as e:
        print(e)
        return []

def save_state(state):
    s3 = boto3.client('s3')
    try:
        s3.put_object(Body=json.dumps(state), Bucket='soham-govande', Key='d3n-state.json')
    except Exception as e:
        print(e)
