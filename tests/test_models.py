import os
import pytest
from datetime import datetime
from app import app, db
from app.models import WeatherData, UserRequest

if os.getenv('ENVIRONMENT') == 'production':
    app.config.from_object('config.ProductionConfig')
elif os.getenv('ENVIRONMENT') == 'development':
    app.config.from_object('config.DevelopmentConfig')

@pytest.fixture(scope='module')
def test_client():
    testing_client = app.test_client()

    with app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()

@pytest.fixture(scope='module')
def init_db(test_client):
    user_request = UserRequest(
        user_id='12345',
        total_cities=10
    )
    db.session.add(user_request)
    db.session.commit()

    weather_info = {
        "city_id": 524901,
        "temperature": 20.24,
        "humidity": 92
    }

    weather_data = WeatherData(
        user_id='12345',
        weather_info=weather_info,
        timestamp=datetime.utcnow()
    )
    db.session.add(weather_data)
    db.session.commit()
    return user_request, weather_data

def test_user_request_model(init_db):
    user_request, _ = init_db
    assert user_request is not None
    assert user_request.user_id == '12345'
    assert user_request.total_cities == 10
    assert user_request.cities_processed == 0
    assert isinstance(user_request.created_at, datetime)

def test_weather_data_model(init_db):
    _, weather_data = init_db
    assert weather_data is not None
    assert weather_data.user_id == '12345'
    assert weather_data.weather_info['city_id'] == 524901
    assert weather_data.weather_info['temperature'] == 20.24
    assert weather_data.weather_info['humidity'] == 92
    assert isinstance(weather_data.timestamp, datetime)

def test_user_request_update(init_db):
    user_request, _ = init_db
    user_request.cities_processed = 5
    db.session.commit()
    updated_request = UserRequest.query.filter_by(user_id='12345').first()
    assert updated_request.cities_processed == 5

def test_weather_data_update(init_db):
    _, weather_data = init_db
    updated_weather_info = {
        "city_id": 524901,
        "temperature": 25.00,
        "humidity": 92
    }
    weather_data.weather_info = updated_weather_info
    db.session.commit()
    updated_weather_data = WeatherData.query.filter_by(user_id='12345').first()
    assert updated_weather_data.weather_info['temperature'] == 25.00
