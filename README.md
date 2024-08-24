# Flask API Project Documentation
## Project Description

This project is a Flask-based API that connects to the OpenWeatherMap API to retrieve weather data. It uses SQLAlchemy to manage the database and Aiohttp for asynchronous requests. The application is configured to support both development and production environments, with environment variables defined in a .env file.

## Project Structure
### Main Files

#### \_\_init\_\_.py
Function: Configures the Flask application, loads environment variables, and initializes the database connection and migration.

Configuration: Relies on the defined environment (development or production) to load the appropriate settings.

#### models.py
Function: Defines the data models used by the application. Includes:

WeatherData: Stores weather information in JSON format, along with a user identifier, a timestamp, and the city ID.

UserRequest: Manages information about user requests, including the user identifier, the total number of cities requested, the number of cities processed, and the creation date.

#### routes.py
Function: Defines the API routes, including:

**\/weather**: POST route to receive and process weather data. Adds a new user request and triggers the retrieval of weather data.

**\/progress/string:user_id**: GET route to check the progress of the user request, returning the percentage of cities processed.

#### utils.py
Function: Contains helper functions to fetch weather data from the OpenWeatherMap API. Uses asynchronous operations to efficiently handle requests and updates the database with the received information.


## Environment Configuration
### Environment Variables

The project uses a .env file to define environment variables. Required variables include:

**ENVIRONMENT**: Defines the execution environment (development or production).
**OPENWEATHER_API_KEY**: API key to access OpenWeatherMap data.

## Tests
The project uses pytest for testing. The tests verify the creation and updating of database records, ensuring that the application functions as expected.

Commands to Run Tests:

```
pytest
```

## Running with Docker
To build and start the application using Docker, use the following commands:
```
docker-compose build
```
```
docker-compose up
```

## Requests

The application will be accessible at http://localhost:5000.
### POST
#### URL
```
http://localhost:5000/weather
```
#### Headers:
```
Content-Type: application/json
```
#### Request Body:
```
{
    "user_id": "123993",
    "city_ids": [
        3439525, 3439781, 3440645, 3442098, 3442778, 3443341, 
        3442233, 3440781, 3441572, 3441575, 3443207, 3442546, 
        3441287, 3441242]
}

```

#### Response:
If the request is correct, you will receive a message confirming the processing:
```
{
    "message": "Weather data is being processed"
}
```
### GET
#### URL
```
http://localhost:5000/progress/{user_id}
```
#### Response:
If the POST request is complete, you will receive a message with the percentage of cities processed:
```
{
    "progress": 100.0
}
```
If the user_id does not exist, you will receive the following message:
```
{
    "message": "Weather data is being processed"
}
```