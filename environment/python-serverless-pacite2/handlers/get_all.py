import json
from models.product import ProductModel
from utils.helpers import DecimalEncoder

def handler(event, context):
    product_model = ProductModel()
    items = product_model.get_all()

    formatted_items = [
        {
            "status": "success",
            "product_id": item["product_id"],
            "product_name": item["product_name"],
            "price": item["price"],
            "quantity": item["quantity"]
        }
        for item in items
    ]

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(formatted_items, cls=DecimalEncoder)
    }
