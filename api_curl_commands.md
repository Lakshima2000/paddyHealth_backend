# 🌐 API Curl Commands

This file contains all the curl commands needed to interact with the Rice Leaf Disease Detection API.

## 🔐 Authentication Endpoints

### 1. Register a New User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "yourpassword123"
  }'
```

Expected Response:

```json
{
  "message": "User registered successfully"
}
```

### 2. Login User

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "yourpassword123"
  }'
```

Expected Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Get User Profile

```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected Response:

```json
{
  "email": "test@example.com",
  "created_at": "2024-03-14T12:00:00Z"
}
```

## 📸 Prediction Endpoints

### 1. Upload Image for Prediction

```bash
curl -X POST http://localhost:5000/api/predictions/predict \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "image=@/path/to/your/image.jpg"
```

Expected Response:

```json
{
  "prediction": "Bacterial Leaf Blight",
  "confidence": 0.95,
  "timestamp": "2024-03-14T12:00:00Z"
}
```

### 2. Get Prediction History

```bash
curl -X GET http://localhost:5000/api/predictions/history \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected Response:

```json
{
  "predictions": [
    {
      "id": 1,
      "disease": "Bacterial Leaf Blight",
      "confidence": 0.95,
      "timestamp": "2024-03-14T12:00:00Z",
      "image_url": "http://localhost:5000/uploads/image1.jpg"
    }
  ]
}
```

## 🔄 WebSocket Endpoints

### 1. Connect to WebSocket

```bash
# Using wscat (install with: npm install -g wscat)
wscat -c ws://localhost:5000/socket.io/?EIO=4&transport=websocket
```

### 2. Send Image for Real-time Prediction

```bash
# After connecting with wscat
{"type": "image", "data": "base64_encoded_image_data"}
```

## 🚨 Error Responses

### 400 Bad Request

```json
{
  "error": "Missing required fields"
}
```

### 401 Unauthorized

```json
{
  "error": "Invalid credentials"
}
```

### 403 Forbidden

```json
{
  "error": "Access denied"
}
```

### 404 Not Found

```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "error": "Internal server error"
}
```

## 📝 Notes

1. Replace `YOUR_ACCESS_TOKEN` with the actual JWT token received from the login endpoint
2. Replace `/path/to/your/image.jpg` with the actual path to your image file
3. The server must be running on `localhost:5000` for these commands to work
4. All timestamps are in ISO 8601 format
5. Image uploads should be in JPG or PNG format
6. Maximum image size is 5MB

## 🔧 Testing Tips

1. Save your access token after login:

   ```bash
   export TOKEN="your_access_token"
   ```

2. Use the token in subsequent requests:

   ```bash
   curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/auth/profile
   ```

3. Test image upload with a sample image:
   ```bash
   curl -X POST http://localhost:5000/api/predictions/predict \
     -H "Authorization: Bearer $TOKEN" \
     -F "image=@sample.jpg"
   ```

## 🔐 Security Notes

1. Always use HTTPS in production
2. Never share your access token
3. Store tokens securely
4. Use strong passwords
5. Keep your API endpoints private

## 📊 Rate Limiting

- 100 requests per hour per IP
- 1000 requests per day per user
- 10MB total upload size per day per user

## 🌐 CORS Headers

The API supports the following CORS headers:

```bash
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

## 🔍 Debugging

To enable verbose output in curl:

```bash
curl -v -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "yourpassword123"}'
```

## 📱 Mobile Testing

For testing on mobile devices, replace `localhost` with your computer's IP address:

```bash
curl -X POST http://192.168.1.100:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "yourpassword123"}'
```

## 🔄 Batch Processing

To process multiple images:

```bash
curl -X POST http://localhost:5000/api/predictions/batch \
  -H "Authorization: Bearer $TOKEN" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" \
  -F "images=@image3.jpg"
```

## 📈 Performance Testing

To test API performance:

```bash
# Install Apache Bench
ab -n 1000 -c 10 -p data.json -T 'application/json' http://localhost:5000/api/auth/login
```

## 🔐 Token Refresh

To refresh an expired token:

```bash
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer $TOKEN"
```

## 📝 File Upload Limits

- Maximum file size: 5MB
- Allowed formats: JPG, PNG
- Maximum dimensions: 4096x4096 pixels
- Minimum dimensions: 224x224 pixels

## 🔧 Environment Variables

Required environment variables:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
export MAIL_USERNAME=your-email@gmail.com
export MAIL_PASSWORD=your-email-password
```
