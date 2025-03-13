import boto3

class DynamoDBGateway:
    
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
        self.table = self.dynamodb.Table(table_name)
    
    def scan(self):
        response = self.table.scan()
        return response.get('Items', [])
    
    def get_item(self, key):
        response = self.table.get_item(Key=key)
        return response.get('Item')
    
    def put_item(self, item):
        return self.table.put_item(Item=item)
    
    def delete_item(self, key):
        return self.table.delete_item(Key=key)