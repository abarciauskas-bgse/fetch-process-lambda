import parallel_wget
import boto3
import json
import os
from run_cumulus_task import run_cumulus_task
import traceback

process_function = open('process_function.txt').read().replace('\n', '')
process_files = __import__(process_function)

client = boto3.client('s3')

def task(event, context):
    try:
        config = event['config']
        files = list(filter(lambda f: config['file_includes'] in f, config['files']))
        parallel_wget.parallel_wget(
           host=config['host'],
           path=config['path'],
           files=files
        )
        # Process files should always return a list of files
        result_files = process_files.process_files()
        print(json.dumps(result_files, indent=2))
        # Upload to S3
        # TODO: make this configurable
        dest_bucket = config['buckets']['public']['name']
        # TODO: make this configurable
        file_prefix = 'processed_data/'
        for file in  result_files:
          res = client.put_object(
            Bucket = dest_bucket,
            Key = '{0}{1}'.format(file_prefix, file.split('/')[-1]),
            Body = open(file, 'r').read())
    except Exception as err:
        print('caught error:')
        traceback.print_tb(err.__traceback__)
        raise err
    print('processing complete')
    return {'messsage': 'processing complete'}

def lambda_handler(event, context):
    return run_cumulus_task(task, event, context)

