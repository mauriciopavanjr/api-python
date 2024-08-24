from flask import request, jsonify, Blueprint
from app import app, db
from app.models import WeatherData, UserRequest
from app.utils import fetch_weather_data
import asyncio

@app.route('/weather', methods=['POST'])
def post_weather():
    data = request.json
    user_id = data.get('user_id')
    city_ids = data.get('city_ids')
    
    if not user_id or not city_ids:
        return jsonify({'error': 'user_id and city_ids are required'}), 400
    
    if UserRequest.query.filter_by(user_id=user_id).first():
        return jsonify({'error': 'user_id must be unique'}), 400
    
    user_request = UserRequest(user_id=user_id, total_cities=len(city_ids))
    db.session.add(user_request)
    db.session.commit()
    
    asyncio.run(fetch_weather_data(user_id, city_ids))
    
    return jsonify({'message': 'Weather data is being processed'}), 202

@app.route('/progress/<string:user_id>', methods=['GET'])
def get_progress(user_id):
    user_request = UserRequest.query.filter_by(user_id=user_id).first()
    
    if not user_request:
        return jsonify({'error': 'user_id not found'}), 404
    
    progress = (user_request.cities_processed / user_request.total_cities) * 100
    
    return jsonify({'progress': progress}), 200


main = Blueprint('main', __name__)

@main.route('/progress/<string:user_id>', methods=['GET'])
def progress(user_id):
    return jsonify({'user_id': user_id, 'progress': 'data'})
