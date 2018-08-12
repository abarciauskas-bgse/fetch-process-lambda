import parallel_wget
import boto3
import json
import os

process_function = open('process_function.txt').read().replace('\n', '')
process_files = __import__(process_function)

client = boto3.client('s3')

def lambda_handler(event, context):
    config = event['config']
    # Return a list of files
    try:
        parallel_wget.parallel_wget(
           host=config['provider']['host'],
           path=config['collection']['provider_path'],
           files=event['input']
        )
        result_files = process_files()
        # Upload to S3
        # TODO: make this configurable
        dest_bucket = config['buckets']['public']
        # TODO: make this configurable
        file_prefix = 'processed_data/'
        for file in  result_files:
          res = client.put_object(
            Bucket = dest_bucket,
            Key = '{0}{1}'.format(file_prefix, file),
            Body = open(file, 'r').read())
    except Exception as err:
        print('caught error:')
        print(err)
    print('processing complete')
    return {'messsage': 'processing complete'}
