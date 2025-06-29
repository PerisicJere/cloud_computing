import pytest
import json
import tempfile
import os
from cloud_computing.assignment2.app import app, db, Item


@pytest.fixture
def client():
    db_fd, temp_db_path = tempfile.mkstemp()

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + temp_db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

    os.close(db_fd)
    os.unlink(temp_db_path)


item_data = {
    'name': 'Knife',
    'description': 'Stab somebody.',
    'damage': 0.1
}


class TestPostEndpoint:

    def test_create_item(self, client):
        client.post(
            '/items/create',
            data=json.dumps(item_data),
            content_type='application/json'
        )
        items = Item.query.all()
        assert len(items) == 1
        assert items[0].name == item_data['name']
        assert items[0].description == item_data['description']
        assert items[0].damage == item_data['damage']


class TestGetEndpoint:

    def test_get_all_items(self, client):
        for i in range(10):
            item_data['name'] = f'Item {i}'
            item_data['damage'] = i * 0.1
            item_data['description'] = f'Item {i} description'
            client.post(
                '/items/create',
                data=json.dumps(item_data),
                content_type='application/json'
            )
        items = Item.query.all()
        assert len(items) == 10
        assert items[1].name == 'Item 1'
        assert items[1].description == 'Item 1 description'
        assert items[1].damage == 0.1


class TestPutEndpoint:

    def test_put_item(self, client):
        for i in range(10):
            item_data['name'] = f'Item {i}'
            item_data['damage'] = i * 1
            item_data['description'] = f'Item {i} description'
            client.post(
                '/items/create',
                data=json.dumps(item_data),
                content_type='application/json'
            )
        item_id: int = 1
        response = client.put(
            f'/items/{item_id}/update',
            data=json.dumps({'damage': 0.9}),
            content_type='application/json'
        )

        assert len(Item.query.all()) == 10
        assert Item.query.get(item_id).damage == 0.9


class TestDeleteEndpoint:

    def test_delete_item(self, client):
        for i in range(9):
            item_data['name'] = f'Item {i}'
            item_data['damage'] = i * 0.1
            item_data['description'] = f'Item {i} description'
            client.post(
                '/items/create',
                data=json.dumps(item_data),
                content_type='application/json'
            )
        client.post(
            '/items/create',
            data=json.dumps(item_data),
            content_type='application/json'
        )
        item_id: int = 2
        client.delete(f'/items/{item_id}/delete')
        assert len(Item.query.all()) == 9

class TestIntegration:

    def test_integration(self, client):
        for i in range(10):
            item_data['name'] = f'Item {i}'
            item_data['damage'] = i * 0.1
            item_data['description'] = f'Item {i} description'
            client.post(
                '/items/create',
                data=json.dumps(item_data),
                content_type='application/json'
            )

        client.put(
            f'/items/{4}/update',
            data=json.dumps({'damage': 0.7}),
            content_type='application/json'
        )

        assert len(Item.query.all()) == 10
        assert Item.query.get(4).damage == 0.7

        client.delete(f'/items/{4}/delete')
        assert len(Item.query.all()) == 9

