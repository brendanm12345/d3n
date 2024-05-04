import boto3
import json
import hashlib

s3 = boto3.client('s3')


def get_state():
    try:
        obj = s3.get_object(Bucket='soham-govande', Key='d3n/state.json')
        return json.loads(obj['Body'].read().decode('utf-8'))
    except Exception as e:
        print(e)
        return {
            'repository': 'https://github.com/brendanm12345/wordle',
            'issues': [],
            'successes': [],
            'failures': []
        }


def save_state(state):
    s3.put_object(Body=json.dumps(state), Bucket='soham-govande',
                  Key='d3n/state.json', ContentType='text/plain')


def create_patch(patch: str):
    # md5 hash of the patch
    patch_hash = hashlib.md5(patch.encode('utf-8')).hexdigest()
    # save the patch to s3
    s3.put_object(Body=patch, Bucket='soham-govande',
                  Key=f'd3n/{patch_hash}.patch', ContentType='text/plain')
    return 'https://soham-govande.s3.amazonaws.com/d3n/' + patch_hash + '.patch'
