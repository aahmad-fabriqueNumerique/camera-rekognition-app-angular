# access denied
# Tgis problem is solved by attaching the appropriate policy to my user.
# IAM -> Users -> Username -> Permissions -> Attach policy.
# ===============
#  Do not forget to put the trigger of S3 bucket
# ===============
# """
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "s3:PutObject",
#                 "s3:GetObject",
#                 "s3:DeleteObject",
#                 "s3:ListBucket"
#             ],
#             "Resource": [
#                 "arn:aws:s3:::test"
#             ]
#         }
#     ]
# }

# """


import json
import boto3

client=boto3.client('rekognition',
                    region_name='us-east-1',
                   aws_access_key_id="YOUR_ACCESS_KEY_ID",
                    aws_secret_access_key="YOUR_SECRET_ACCESS_KEY")
bucket_name = "terega-test-image"

collection_id = "osmcollection"
                    
s3 = boto3.resource('s3',
                    region_name='us-east-1',
                    aws_access_key_id="YOUR_ACCESS_KEY_ID",
                    aws_secret_access_key="YOUR_SECRET_ACCESS_KEY")
response = []

invokeLambda = boto3.client('lambda', region_name='us-east-1',
                    aws_access_key_id="YOUR_ACCESS_KEY_ID",
                    aws_secret_access_key="YOUR_SECRET_ACCESS_KEY")
                    
def lambda_handler(event, context):
    
    for file in s3.Bucket(bucket_name).objects.all():
        split_photo= file.key.split('_')
        ex_image_id = split_photo[0]
        client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket_name,'Name':file.key}},
                                ExternalImageId=ex_image_id,
                                MaxFaces=4,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])
        response.append(ex_image_id)
        
    invokeLambda.invoke(FunctionName = 'osm-delete-objects-s3', InvocationType = 'RequestResponse', Payload = json.dumps(event))   

        
    return response 