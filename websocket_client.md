# 🔌 WebSocket Client Integration

## URLs and Configuration

```javascript
// Base URLs
const API_URL = "http://127.0.0.1:5000"; // For HTTP requests
const WS_URL = "http://127.0.0.1:5000"; // For WebSocket connection

// Socket.IO Configuration
const socketConfig = {
  transports: ["websocket"],
  auth: {
    token: "your-jwt-token", // Will be set after login
  },
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
};
```

## 📱 Frontend Integration Examples

### 1. Using Socket.IO Client (Recommended)

```javascript
import { io } from "socket.io-client";

// Initialize socket connection
const socket = io(WS_URL, {
  transports: ["websocket"],
  auth: {
    token: "your-jwt-token", // Set after login
  },
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
});

// Connection event handlers
socket.on("connect", () => {
  console.log("Connected to WebSocket server");
});

socket.on("disconnect", () => {
  console.log("Disconnected from WebSocket server");
});

// Listen for prediction results
socket.on("prediction_result", (data) => {
  console.log("Received prediction:", data);
});

// Send image for prediction
async function sendImageForPrediction(imageUri, predictionId) {
  try {
    // Convert image to base64
    const base64 = await convertImageToBase64(imageUri);

    // Send the image data
    socket.emit("predict_disease", {
      image: base64,
      predictionId,
    });

    console.log("Image sent for prediction:", predictionId);
  } catch (error) {
    console.error("Error sending image:", error);
    throw error;
  }
}
```

### 2. React Component Example

```jsx
import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";

function PredictionComponent() {
  const [socket, setSocket] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [connected, setConnected] = useState(false);
  const [token, setToken] = useState(null);

  useEffect(() => {
    // Get token from storage
    const getToken = async () => {
      const storedToken = await AsyncStorage.getItem("access_token");
      setToken(storedToken);
    };
    getToken();
  }, []);

  useEffect(() => {
    if (!token) return;

    // Initialize socket connection
    const newSocket = io(WS_URL, {
      transports: ["websocket"],
      auth: {
        token,
      },
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    // Connection event handlers
    newSocket.on("connect", () => {
      setConnected(true);
      console.log("Connected to WebSocket server");
    });

    newSocket.on("disconnect", () => {
      setConnected(false);
      console.log("Disconnected from WebSocket server");
    });

    // Listen for prediction results
    newSocket.on("prediction_result", (data) => {
      setPrediction(data);
    });

    setSocket(newSocket);

    // Cleanup on component unmount
    return () => {
      newSocket.close();
    };
  }, [token]);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (file && socket) {
      try {
        const base64 = await convertImageToBase64(file);
        const predictionId = generatePredictionId(); // Implement this function

        socket.emit("predict_disease", {
          image: base64,
          predictionId,
        });
      } catch (error) {
        console.error("Error sending image:", error);
      }
    }
  };

  return (
    <div>
      <h2>Rice Leaf Disease Detection</h2>
      <p>Connection status: {connected ? "Connected" : "Disconnected"}</p>

      <input type="file" accept="image/*" onChange={handleImageUpload} />

      {prediction && (
        <div>
          <h3>Prediction Result:</h3>
          <p>Disease: {prediction.prediction}</p>
          <p>Confidence: {prediction.confidence}%</p>
          <p>Timestamp: {prediction.timestamp}</p>
        </div>
      )}
    </div>
  );
}

export default PredictionComponent;
```

## 🔧 Configuration Options

### Socket.IO Client Options

```javascript
const options = {
  transports: ["websocket"], // Force WebSocket transport
  auth: {
    token: "your-jwt-token", // Authentication token
  },
  reconnection: true, // Enable reconnection
  reconnectionAttempts: 5, // Number of reconnection attempts
  reconnectionDelay: 1000, // Delay between reconnection attempts
  timeout: 20000, // Connection timeout
  autoConnect: true, // Automatically connect
};
```

## 🔐 Authentication

To include authentication token in WebSocket connection:

```javascript
const socket = io(WS_URL, {
  transports: ["websocket"],
  auth: {
    token: "your-jwt-token",
  },
});
```

## 🌐 Production Configuration

For production, use secure WebSocket connection:

```javascript
const API_URL = "https://your-domain.com";
const WS_URL = "https://your-domain.com";
```

## 📊 Error Handling

```javascript
socket.on("connect_error", (error) => {
  console.error("Connection error:", error);
});

socket.on("error", (error) => {
  console.error("Socket error:", error);
});

socket.on("reconnect_attempt", (attemptNumber) => {
  console.log("Reconnection attempt:", attemptNumber);
});

socket.on("reconnect_failed", () => {
  console.error("Failed to reconnect");
});
```

## 🔄 Reconnection Strategy

```javascript
const socket = io(WS_URL, {
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  randomizationFactor: 0.5,
});
```

## 📈 Performance Optimization

1. Use base64 encoding for image transfer
2. Implement message queuing
3. Handle backpressure
4. Implement message compression
5. Use connection pooling

## 🔐 Security Best Practices

1. Use WSS in production
2. Implement token authentication
3. Validate all messages
4. Implement rate limiting
5. Handle connection timeouts

## 📝 API Endpoints

### Authentication

- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login user
- GET `/api/auth/profile` - Get user profile

### Predictions

- POST `/api/predictions/predict` - Upload and analyze image
- GET `/api/predictions/history` - Get prediction history

## 🔍 Debugging

Enable Socket.IO debug mode:

```javascript
localStorage.debug = "socket.io-client:*";
```

## 📱 Mobile Considerations

1. Handle connection state changes
2. Implement reconnection logic
3. Handle offline/online events
4. Manage battery usage
5. Handle poor network conditions
