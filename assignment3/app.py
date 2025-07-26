from flask import Flask, request, jsonify
import boto3
import json
import uuid
import time
from botocore.exceptions import ClientError

app = Flask(__name__)

table = None
s3 = None


def get_aws_clients():
    global table, s3
    # this is the only way I got mock db and bucket to work, I had issues with it setting up but not creating table
    if table is None or s3 is None:
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566', region_name='us-east-1',
                                  aws_access_key_id='test', aws_secret_access_key='test')
        s3 = boto3.client('s3', endpoint_url='http://localstack:4566', region_name='us-east-1',
                          aws_access_key_id='test', aws_secret_access_key='test')
        table = dynamodb.Table('items')

    return table, s3


def init_aws_resources():
    # I initialize resources here, and in get_aws_clients(), I "fetch" them
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566', region_name='us-east-1',
                              aws_access_key_id='test', aws_secret_access_key='test')
    s3_client = boto3.client('s3', endpoint_url='http://localstack:4566', region_name='us-east-1',
                             aws_access_key_id='test', aws_secret_access_key='test')

    table_obj = dynamodb.create_table(
        TableName='items',
        KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    table_obj.wait_until_exists()

    s3_client.create_bucket(Bucket='items-bucket')

    test_table = dynamodb.Table('items')
    test_table.scan(Limit=1)
    return True

@app.route('/items', methods=['GET'])
def get_items():
    try:
        table_obj, s3_client = get_aws_clients()

        item_id = request.args.get('id')
        if item_id:
            response = table_obj.get_item(Key={'id': item_id})
            if 'Item' in response:
                return jsonify(response['Item'])
            return jsonify({'error': 'Item not found'}), 404

        response = table_obj.scan()
        return jsonify({'items': response.get('Items', [])})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/items', methods=['POST'])
def create_item():
    try:
        table_obj, s3_client = get_aws_clients()

        data = request.get_json()

        existing = table_obj.scan(FilterExpression=boto3.dynamodb.conditions.Attr('name').eq(data['name']))
        if existing['Items']:
            return jsonify({'error': 'Item already exists'}), 409

        item_id = str(uuid.uuid4())
        item = {'id': item_id, 'name': data['name'], 'description': data.get('description', '')}

        table_obj.put_item(Item=item)
        s3_client.put_object(Bucket='items-bucket', Key=f"{item_id}.json", Body=json.dumps(item))

        return jsonify(item), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        table_obj, s3_client = get_aws_clients()

        data = request.get_json()
        response = table_obj.get_item(Key={'id': item_id})
        if 'Item' not in response:
            return jsonify({'error': 'Item not found'}), 404

        item = response['Item']
        item.update({'name': data.get('name', item['name']),
                     'description': data.get('description', item.get('description', ''))})

        table_obj.put_item(Item=item)
        s3_client.put_object(Bucket='items-bucket', Key=f"{item_id}.json", Body=json.dumps(item))

        return jsonify(item)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        table_obj, s3_client = get_aws_clients()
        response = table_obj.get_item(Key={'id': item_id})
        if 'Item' not in response:
            return jsonify({'error': 'Item not found'}), 404

        table_obj.delete_item(Key={'id': item_id})
        s3_client.delete_object(Bucket='items-bucket', Key=f"{item_id}.json")

        return jsonify({'message': 'Item deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    if init_aws_resources():
        app.run(host='0.0.0.0', port=5000)
        exit(1)