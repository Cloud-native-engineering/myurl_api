from flask_sqlalchemy import SQLAlchemy
import boto3   

db = SQLAlchemy()

class QueueFeed:
    def __init__(self, queue_url, region_name='us-east-1'):
        self.sqs = boto3.client('sqs', region_name=region_name)
        self.queue_url = queue_url

    def send_message(self, action, original_url, short_url, is_verified):
        message_body = f"{{\"action\": \"{action}\", \"original_url\": \"{original_url}\", \"short_url\": \"{short_url}\", \"is_verified\": \"{is_verified}\"}}"
        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message_body
        )
        return response['MessageId']