import json
from models.product import ProductModel
from utils.helpers import DecimalEncoder

def handler(event, context):
    query_params = event.get("queryStringParameters", {}) or {}
    
    product_id = query_params.get("product_id")
    product_name = query_params.get("product_name")

    if not (product_id or product_name):
        return {
            "statusCode": 400,
            "body": json.dumps({"status": "error", "message": "Either product_id or product_name query parameter is required"})
        }

    product_model = ProductModel()
    item = None

    if product_id:
        item = product_model.get_one(product_id)
    elif product_name:
        item = product_model.get_by_name(product_name)

    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({"status": "error", "message": "Product not found"})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(item, cls=DecimalEncoder)
    }