import json
import requests
import pytest
import time
import boto3

BASE_URL = "http://app:5000"

SAMPLE_ITEMS = [
    {"name": "One ring", "description": "To rule them all"},
    {"name": "Darth Vader", "description": "May the 4th be with you"},
    {"name": "Indiana Jones", "description": "Indy"},
    {"name": "Jon Snow", "description": "King in the north"},
    {"name": "Tyrion Lannister", "description": "Great until season 6"}
]

@pytest.fixture(autouse=True, scope="session")
def setup_test_data():
    for _ in range(60):
        try:
            response = requests.get(f"{BASE_URL}/items", timeout=10)
            if response.status_code == 200:
                break
        except:
            time.sleep(2)

    try:
        response = requests.get(f"{BASE_URL}/items")
        if response.status_code == 200:
            existing_items = response.json().get('items', [])
            for item in existing_items:
                requests.delete(f"{BASE_URL}/items/{item['id']}")
                time.sleep(0.1)
    except:
        pass

    created_items = []
    for item_data in SAMPLE_ITEMS:
        response = requests.post(f"{BASE_URL}/items", json=item_data)
        if response.status_code == 201:
            created_items.append(response.json())
        time.sleep(0.2)

    yield created_items

    for item in created_items:
        try:
            requests.delete(f"{BASE_URL}/items/{item['id']}")
        except:
            pass

def verify_s3_dynamo_consistency(item_id):
    try:
        s3 = boto3.client('s3', endpoint_url='http://localstack:4566', region_name='us-east-1',
                          aws_access_key_id='test', aws_secret_access_key='test')
        dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566', region_name='us-east-1',
                                  aws_access_key_id='test', aws_secret_access_key='test')

        s3_object = s3.get_object(Bucket='items-bucket', Key=f'{item_id}.json')
        s3_data = json.loads(s3_object['Body'].read())

        table = dynamodb.Table('items')
        dynamo_response = table.get_item(Key={'id': item_id})
        dynamo_data = dynamo_response.get('Item', {})

        return (s3_data.get('name') == dynamo_data.get('name') and
                s3_data.get('description') == dynamo_data.get('description'))
    except:
        return False

def test_get_sample_item_by_id(setup_test_data):
    sample_items = setup_test_data
    if sample_items:
        item_id = sample_items[0]['id']
        response = requests.get(f"{BASE_URL}/items?id={item_id}")
        assert response.status_code == 200
        assert response.json()['name'] == sample_items[0]['name']
        assert verify_s3_dynamo_consistency(item_id)

def test_get_no_params(setup_test_data):
    response = requests.get(f"{BASE_URL}/items")
    assert response.status_code == 200
    data = response.json()
    assert 'items' in data
    assert len(data['items']) >= len(SAMPLE_ITEMS)

def test_get_not_found():
    response = requests.get(f"{BASE_URL}/items?id=lukeiamnotyouritem")
    assert response.status_code == 404

def test_get_incorrect_params():
    response = requests.get(f"{BASE_URL}/items?blablathisisbad")
    assert response.status_code == 200

def test_post_create_item():
    data = {"name": "test_item_new", "description": "test"}
    response = requests.post(f"{BASE_URL}/items", json=data)
    assert response.status_code == 201
    assert response.json()['name'] == 'test_item_new'

    item_id = response.json()['id']
    time.sleep(0.2)
    assert verify_s3_dynamo_consistency(item_id)

def test_post_duplicate():
    duplicate_data = {"name": "Darth Vader", "description": "May the 4th be with you"}
    response = requests.post(f"{BASE_URL}/items", json=duplicate_data)
    assert response.status_code == 409
    assert 'error' in response.json()
    assert 'already exists' in response.json()['error']

def test_put_existing_sample_item(setup_test_data):
    sample_items = setup_test_data
    if sample_items:
        item_id = sample_items[0]['id']
        update_data = {"name": "Tywin Lannister", "description": "Hear me roar!"}

        response = requests.put(f"{BASE_URL}/items/{item_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()['name'] == 'Tywin Lannister'
        assert response.json()['description'] == 'Hear me roar!'

        time.sleep(0.2)
        assert verify_s3_dynamo_consistency(item_id)

def test_put_not_found():
    response = requests.put(f"{BASE_URL}/items/nonexistent", json={"name": "test"})
    assert response.status_code == 404

def test_delete_existing_item(setup_test_data):
    sample_items = setup_test_data
    if sample_items and len(sample_items) > 1:
        item_id = sample_items[-1]['id']
        response = requests.delete(f"{BASE_URL}/items/{item_id}")
        assert response.status_code == 200
        time.sleep(0.2)
        get_response = requests.get(f"{BASE_URL}/items?id={item_id}")
        assert get_response.status_code == 404

def test_delete_not_found():
    response = requests.delete(f"{BASE_URL}/items/nonexistent")
    assert response.status_code == 404