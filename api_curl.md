# Rice Leaf Disease Prediction API Documentation

This document provides examples of how to interact with the Rice Leaf Disease Prediction API using curl commands.

## Base URL

```
http://127.0.0.1:5000
```

## Authentication

### Register a New User

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Response:**

```json
{
  "message": "User registered successfully"
}
```

### Login

```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Response:**

```json
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}
```

### Get User Profile

```bash
curl http://127.0.0.1:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**

```json
{
  "email": "test@example.com",
  "created_at": "2024-03-21T10:00:00Z"
}
```

## Predictions

### Predict Disease from Image

```bash
curl -X POST http://127.0.0.1:5000/api/predictions/predict \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "image=@/path/to/your/image.jpg"
```

**Response:**

```json
{
  "prediction": "Bacterial Leaf Blight",
  "confidence": 0.95,
  "timestamp": "2024-03-21T10:00:00Z"
}
```

### Get Prediction History

```bash
curl http://127.0.0.1:5000/api/predictions/history \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**

```json
{
  "predictions": [
    {
      "id": 1,
      "disease": "Bacterial Leaf Blight",
      "confidence": 0.95,
      "timestamp": "2024-03-21T10:00:00Z",
      "image_url": "http://127.0.0.1:5000/uploads/prediction_1.jpg"
    }
  ]
}
```

## WebSocket Connection

### Connect to WebSocket Server

```bash
# Using wscat for testing WebSocket connections
wscat -c "ws://127.0.0.1:5000" -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Send Image for Real-time Prediction

```json
{
  "event": "predict_disease",
  "data": {
    "image": "base64_encoded_image_data",
    "predictionId": "unique_prediction_id"
  }
}
```

### Receive Prediction Result

```json
{
  "event": "prediction_result",
  "data": {
    "prediction": "Bacterial Leaf Blight",
    "confidence": 0.95,
    "timestamp": "2024-03-21T10:00:00Z",
    "predictionId": "unique_prediction_id"
  }
}
```

## Error Responses

### Authentication Error

```json
{
  "error": "Invalid credentials"
}
```

### Validation Error

```json
{
  "error": "Invalid input data",
  "details": {
    "email": "Invalid email format",
    "password": "Password must be at least 8 characters"
  }
}
```

### Server Error

```json
{
  "error": "Internal server error"
}
```

## Notes

1. Replace `YOUR_JWT_TOKEN` with the actual JWT token obtained from the login endpoint
2. Replace `/path/to/your/image.jpg` with the actual path to your image file
3. When testing from a mobile device, replace `127.0.0.1` with your computer's local IP address
4. All timestamps are in ISO 8601 format
5. Image uploads should be in JPEG or PNG format
6. Base64 encoded images should be prefixed with `data:image/jpeg;base64,` or `data:image/png;base64,`

## Testing Tips

1. Use `-v` flag with curl for verbose output:

```bash
curl -v -X POST http://127.0.0.1:5000/api/auth/login ...
```

2. Save JWT token to a variable for easier testing:

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/api/auth/login ... | jq -r '.access_token')
```

3. Use the token in subsequent requests:

```bash
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/api/auth/profile
```

4. For WebSocket testing, install wscat:

```bash
npm install -g wscat
```
