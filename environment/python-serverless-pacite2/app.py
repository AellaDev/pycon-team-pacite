import boto3
from flask import Flask, render_template, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products_page():
    return render_template('products.html')

@app.route('/api/products')
def get_products():
    # Configure AWS with environment variables
    dynamodb = boto3.resource('dynamodb',
        region_name='us-east-2',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    
    table = dynamodb.Table('products-pacite2')
    response = table.scan()
    
    return jsonify(response['Items'])

if __name__ == '__main__':
    app.run(debug=True)