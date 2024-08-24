import pytest
from app import app, db
from flask import json

@pytest.fixture(scope='module')
def test_client():
    testing_client = app.test_client()
    with app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()

def test_post_weather_success(test_client):
    payload = {
        'user_id': 'test_user',
        'city_ids': [524901, 703448]
    }
    
    response = test_client.post('/weather', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 202
    assert b'Weather data is being processed' in response.data

def test_get_progress_success(test_client):
    payload = {
        'user_id': 'test_progress_user',
        'city_ids': [524901, 703448]
    }
    
    response = test_client.post('/weather', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 202
    response = test_client.get('/progress/test_progress_user')
    assert response.status_code == 200
    assert b'progress' in response.data