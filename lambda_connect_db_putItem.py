# ===========
# DO NOT FORGET TO PUT " KINESIS DATA STREAM " AS A TRIGGER FOR THE FUNCTION
# ===========

import boto3
import datetime
import base64
import json

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    now = str(datetime.datetime.now())
    
    try:
        # connect to dynamoDb
        dynamo_db = boto3.resource('dynamodb',
                    region_name='us-east-1',
                    aws_access_key_id="YOUR_ACCESS_KEY_ID",
                    aws_secret_access_key="YOUR_SECRET_ACCESS_KEY")
        table = dynamo_db.Table('prestataire')
        
    
        
        # parse base64 data
        for record in event["Records"]:
            encoded = record["kinesis"]["data"]
            decoded = json.loads(base64.b64decode(encoded).decode("utf-8"))
            for faceSearchResponse in decoded["FaceSearchResponse"]:
                for matchedFaces in faceSearchResponse["MatchedFaces"]:
                    # parse data to dynamoDb item
                    data = {
                        'id' : now,
                        'FaceId': matchedFaces["Face"]["FaceId"],
                        'Confidence': str(matchedFaces["Face"]["Confidence"]),
                        'Similarity': str(matchedFaces["Similarity"]),
                        'ExternalImageId': matchedFaces["Face"]["ExternalImageId"],
                        'ImageId':matchedFaces["Face"]["ImageId"]
                    }
                    table.put_item(Item=data)
                   
                    
    #handle exception
    except Exception as e: 
        print(str(e))
