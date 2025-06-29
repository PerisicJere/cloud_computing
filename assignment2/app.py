import os

from flask import Flask, request, jsonify, Response, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///items.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    damage = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'damage': self.damage
        }

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('get_all_items'))

@app.route('/items', methods=['GET'])
def get_all_items() -> str | tuple[Response, int]:
    try:
        items = Item.query.all()
        return render_template("index.html", items=items, title="Items")
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/items/create', methods=['POST'])
def create_item_form():
    try:
        if request.is_json:
            data = request.get_json()
        elif request.form:
            data = request.form.to_dict()
        else:
            return jsonify({'error': 'No data provided'}), 400

        if data is None:
            return jsonify({'error': 'Invalid data'}), 400


        new_item = Item(
            name=data['name'],
            description=data.get('description', ''),
            damage=float(data['damage'])
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('get_all_items'))

    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/items/<int:item_id>/update', methods=['POST', 'PUT'])
def update_item_form(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        if request.is_json:
            data = request.get_json()
        elif request.form:
            data = request.form.to_dict()
        else:
            return jsonify({'error': 'No data provided'}), 400

        if data is None:
            return jsonify({'error': 'Invalid data'}), 400

        item.damage = float(data['damage'])

        db.session.commit()
        return redirect(url_for('get_all_items'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/items/<int:item_id>/delete', methods=['DELETE', 'POST'])
def delete_item_form(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({'error': 'Item not found'}), 404

        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('get_all_items'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error) -> tuple[Response, int]:
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error) -> tuple[Response, int]:
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
