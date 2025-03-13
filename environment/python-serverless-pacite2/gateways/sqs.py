import boto3

class SQSGateway:
    
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.sqs = boto3.resource('sqs', region_name='us-east-2')
        self.queue = self.sqs.get_queue_by_name(QueueName=queue_name)
    
    def send_message(self, message_body):
        response = self.queue.send_message(MessageBody=message_body)
        return response
    
    def receive_messages(self, max_messages=10, wait_time=10):
        return self.queue.receive_messages(
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time
        )
    
    def delete_message(self, message):
        message.delete()