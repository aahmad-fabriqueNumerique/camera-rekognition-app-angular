import json
import boto3

s3_resource = boto3.resource('s3',region_name='eu-west-1',
                    aws_access_key_id="YOUR_ACCESS_KEY_ID",
                    aws_secret_access_key="YOUR_SECRET_ACCESS_KEY")
bucket_name = "terega-test-image"

def lambda_handler(event, context):
    res = []
    bucket = s3_resource.Bucket(bucket_name)
    for obj_version in bucket.object_versions.all():
        res.append({
                    'Key': obj_version.object_key,
                    'VersionId': obj_version.id
                    })
    print(res)
    if len(res) > 0:
        bucket.delete_objects(Delete={'Objects': res})
    
    return res