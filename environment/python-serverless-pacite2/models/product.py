from decimal import Decimal
import json
from gateways.dynamodb import DynamoDBGateway
from gateways.sqs import SQSGateway
from gateways.s3 import S3Gateway
from utils.helpers import generate_code, DecimalEncoder

class ProductModel:
    
    def __init__(self):
        self.table_name = "products-pacite2"
        self.dynamodb = DynamoDBGateway(self.table_name)
        self.sqs = SQSGateway("products-sqs-pacite2")
        self.s3 = S3Gateway("products-bucket-pacite2")
    
    def get_all(self):
        return self.dynamodb.scan()
    
    def _validate_product(self, product):
        required_keys = ["product_id", "product_name", "price", "quantity"]
        return all(key in product for key in required_keys)
    
    def _prepare_for_db(self, product):
        if "price" in product and not isinstance(product["price"], Decimal):
            try:
                product["price"] = Decimal(str(product["price"]))
            except:
                pass
                
        if "quantity" in product and not isinstance(product["quantity"], Decimal):
            try:
                product["quantity"] = Decimal(str(product["quantity"]))
            except:
                pass
        return product
            
    def get_one(self, product_id):
        import boto3
        from boto3.dynamodb.conditions import Key

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table_name)

        response = table.get_item(Key={"product_id": product_id})
        return response.get("Item")
        
    def get_by_name(self, product_name):
        import boto3
        from boto3.dynamodb.conditions import Attr
    
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table_name)
    
        response = table.scan(
            FilterExpression=Attr("product_name").eq(product_name)
        )
    
        items = response.get("Items", [])
        return items[0] if items else None
        
    def purchase_product(self, product_id, purchase_quantity):
        import boto3
        from boto3.dynamodb.conditions import Key
    
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table_name)
    
        # Get the current stock
        response = table.get_item(Key={"product_id": product_id})
        item = response.get("Item")
    
        if not item:
            return {"status": "error", "message": "Product not found"}
    
        current_stock = int(item["quantity"])
    
        if purchase_quantity > current_stock:
            return {"status": "error", "message": "Not enough stock available"}
    
        new_stock = current_stock - purchase_quantity
    
        table.update_item(
            Key={"product_id": product_id},
            UpdateExpression="SET quantity = :new_quantity",
            ExpressionAttributeValues={":new_quantity": new_stock}
        )
    
        return {"status": "success", "message": "Purchase successful", "remaining_stock": new_stock}



    
