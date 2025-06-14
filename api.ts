import io from "socket.io-client";
import AsyncStorage from "@react-native-async-storage/async-storage";
import * as FileSystem from "expo-file-system";

// Infer the Socket type from the io function
type Socket = ReturnType<typeof io>;

// Base URLs
const API_URL = "http://127.0.0.1:5001"; // Updated port to 5001
const WS_URL = "http://127.0.0.1:5001"; // Updated port to 5001

// Types
interface PredictionResult {
  prediction: string;
  confidence: number;
  prediction_id: number;
  status: string;
}

interface ApiError {
  error: string;
  status: string;
}

// API Service class
class ApiService {
  private socket: Socket | null = null;
  private token: string | null = null;
  private isConnected: boolean = false;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;

  // Initialize the service
  async init() {
    try {
      this.token = await AsyncStorage.getItem("access_token");
      await this.initializeWebSocket();
    } catch (error) {
      console.error("Failed to initialize API service:", error);
      throw error;
    }
  }

  // WebSocket methods
  private async initializeWebSocket() {
    return new Promise<void>((resolve, reject) => {
      try {
        this.socket = io(WS_URL, {
          transports: ["websocket"],
          auth: {
            token: this.token,
          },
          reconnection: true,
          reconnectionAttempts: this.maxReconnectAttempts,
          reconnectionDelay: 1000,
          timeout: 10000,
        });

        this.socket.on("connect", () => {
          console.log("Connected to WebSocket server");
          this.isConnected = true;
          this.reconnectAttempts = 0;
          resolve();
        });

        this.socket.on("disconnect", (reason) => {
          console.log("Disconnected from WebSocket server:", reason);
          this.isConnected = false;
        });

        this.socket.on("connect_error", (error) => {
          console.error("WebSocket connection error:", error);
          this.isConnected = false;
          this.reconnectAttempts++;

          if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            reject(
              new Error(
                "Failed to connect to WebSocket server after multiple attempts"
              )
            );
          }
        });

        this.socket.on("error", (error) => {
          console.error("WebSocket error:", error);
          this.isConnected = false;
        });

        this.socket.on(
          "prediction_result",
          (data: PredictionResult | ApiError) => {
            console.log("Received prediction result:", data);
            // Handle the prediction result here
            if ("error" in data) {
              console.error("Prediction error:", data.error);
            } else {
              console.log("Prediction success:", data);
            }
          }
        );
      } catch (error) {
        console.error("Error initializing WebSocket:", error);
        reject(error);
      }
    });
  }

  // Send image for prediction
  async sendImageForPrediction(imageUri: string): Promise<void> {
    if (!this.socket || !this.isConnected) {
      throw new Error("WebSocket not connected");
    }

    try {
      // Read the image file
      const base64 = await FileSystem.readAsStringAsync(imageUri, {
        encoding: FileSystem.EncodingType.Base64,
      });

      // Generate a unique prediction ID
      const predictionId = Date.now().toString();

      // Send the image data
      this.socket.emit("predict_disease", {
        image: base64,
        predictionId,
      });

      console.log("Image sent for prediction:", predictionId);
    } catch (error) {
      console.error("Error sending image:", error);
      throw error;
    }
  }

  // Cleanup
  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
    }
  }

  // Prediction methods
  async predictDisease(imageUri: string): Promise<PredictionResult> {
    if (!this.token) {
      throw new Error("Not authenticated");
    }

    if (!this.socket || !this.isConnected) {
      throw new Error(
        "WebSocket not connected. Cannot get session_id for HTTP prediction."
      );
    }

    const formData = new FormData();
    formData.append("image", {
      uri: imageUri,
      type: "image/jpeg",
      name: "image.jpg",
    } as any);

    // Add the WebSocket session ID to the form data
    formData.append("session_id", this.socket.id);

    const response = await fetch(`${API_URL}/api/predictions/predict`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
      body: formData,
    });

    // Handle the response
    if (response.ok) {
      const result = await response.json();
      return result as PredictionResult;
    } else {
      throw new Error("HTTP prediction request failed");
    }
  }
}

// Export a singleton instance
export const apiService = new ApiService();
