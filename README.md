## Overview
This application is a Flask-based proxy server for forwarding GraphQL requests to a target endpoint (AniList's GraphQL API). It caches responses using Python's built-in LRU (Least Recently Used) cache for optimization and includes error handling for failed requests.

## Features
- **GraphQL Proxy Endpoints**: Two routes (`/graphql` and `/`) that accept incoming JSON requests and forward them to the target API.
- **Caching**: Utilizes `functools.lru_cache` for caching responses and optimizing repeated requests.
- **Custom Headers and Cookies**: Configurable headers and cookies for request forwarding.
- **Error Handling**: Graceful handling of request errors and missing payloads.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/adgsenpai/AnilistByPass
   cd AnilistByPass
   ```

2. **Install dependencies**:
   Ensure you have Python 3.x installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
1. **Start the Flask server**:
   ```bash
   python app.py
   ```
   The application will run on `http://0.0.0.0:8000` by default.

## Usage
### Endpoints
- **`/graphql`** and **`/`** (POST request): Accepts a JSON payload representing the GraphQL query/mutation.

### Example Request
Send a POST request with the following payload:
```json
{
  "query": "{ Media(id: 1) { title { romaji } } }"
}
```

### Response
A successful response will return the JSON result from the target GraphQL API.
```json
{
  "data": {
    "Media": {
      "title": {
        "romaji": "Cowboy Bebop"
      }
    }
  }
}
```

## Configuration
### Customizing Headers and Cookies
Update the `HEADERS` and `COOKIES` dictionaries in the code to include your custom values as needed.

### Caching
The `@lru_cache` decorator is set to cache up to 128 unique requests. This can be adjusted by modifying `maxsize` in the code.

## Error Handling
- If an incoming request does not contain a JSON payload, the server returns:
  ```json
  { "error": "Invalid request, JSON body required" }
  ```
  with a 400 status code.
- If the request to the target endpoint fails, a 500 status code and an error message are returned.

## Security Note
Ensure that sensitive data such as cookie values or authentication tokens are managed securely and not hard-coded in a production environment.

## License
MIT License

## Contact
For further information or questions, please contact Ashlin Darius Govindasamy at [your-email@example.com].

