import json
from models.product import ProductModel
from utils.helpers import DecimalEncoder

def handler(event, context):
    body = json.loads(event.get("body", "{}"))
    
    product_id = body.get("product_id")
    product_name = body.get("product_name")
    purchase_quantity = body.get("quantity")

    if not (product_id or product_name) or purchase_quantity <= 0:
        return {
            "statusCode": 400,
            "body": json.dumps({"status": "error", "message": "Either product ID or product name required, and purchase quantity must be positive"})
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

    actual_product_id = item["product_id"]
    result = product_model.purchase_product(actual_product_id, purchase_quantity)

    return {
        "statusCode": 200 if result["status"] == "success" else 400,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result, cls=DecimalEncoder)
    }