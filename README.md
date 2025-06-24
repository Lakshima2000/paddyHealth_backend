# 🌾 Rice Leaf Disease Detection

This project helps farmers detect diseases in rice plants by analyzing images of rice leaves. It uses artificial intelligence to identify common rice leaf diseases and provides instant results.

## 🚀 Quick Start Guide

### Step 1: Install Python

1. Download Python from [python.org](https://python.org)
2. During installation, make sure to check "Add Python to PATH"
3. To verify installation, open Terminal (Mac/Linux) or Command Prompt (Windows) and type:
   ```bash
   python --version
   ```

### Step 2: Set Up the Project

1. Download or clone this project to your computer
2. Open Terminal (Mac/Linux) or Command Prompt (Windows)
3. Navigate to the project folder:
   ```bash
   cd riceleaf-diesease-prediction
   ```

### Step 3: Create a Virtual Environment

1. Create a new virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

### Step 4: Install Required Packages

1. Install all required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Step 5: Set Up Environment Variables

1. Create a new file named `.env` in the project folder
2. Add the following content (replace with your own values):
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-email-password
   ```

### Step 6: Run the Application

1. Start the server:
   ```bash
   python app.py
   ```
2. Open your web browser and go to:
   ```
   http://localhost:5000
   ```

## 📱 Using the Application

### Register a New Account

1. Click on "Register" or go to `/api/auth/register`
2. Fill in your details:
   - Username
   - Email
   - Password
3. Click "Register"

### Login

1. Click on "Login" or go to `/api/auth/login`
2. Enter your email and password
3. Click "Login"
4. Save the access token you receive

### Upload an Image

1. Click on "Upload Image" or go to `/api/predictions/predict`
2. Select an image of a rice leaf
3. Click "Upload"
4. Wait for the results

## 🔧 Troubleshooting

### Common Issues and Solutions

1. **"Module not found" error**

   - Make sure you're in the virtual environment
   - Try running: `pip install -r requirements.txt` again

2. **"Port already in use" error**

   - Close other applications using port 5000
   - Or change the port in `app.py`

3. **Email not working**

   - Check your email settings in `.env`
   - Make sure you're using an app password for Gmail

4. **Database errors**
   - Delete the existing database file (if any)
   - Restart the application

## 📚 Project Structure

```
riceleaf-diesease-prediction/
├── app.py              # Main application file
├── auth.py             # Authentication routes
├── prediction.py       # Disease prediction routes
├── models.py           # Database models
├── config.py           # Configuration settings
├── extensions.py       # Flask extensions
├── requirements.txt    # Required packages
└── .env               # Environment variables
```

## 🤝 Contributing

Feel free to contribute to this project! Here's how:

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request


## 🙏 Acknowledgments

- Thanks to all contributors and supervisor Dr chamara
- Special thanks to the open-source community
- Inspired by the need to help farmers detect plant diseases early

## 📞 Support

If you need help:

1. Check the troubleshooting section
2. Open an issue on GitHub
3. Contact the maintainers

## 🌟 Features

- 🔐 User authentication
- 📸 Image upload
- 🤖 AI-powered disease detection
- 📱 Real-time results
- 🔒 Secure API endpoints

## 🔮 Future Improvements

- [ ] Mobile app development
- [ ] More disease types
- [ ] Offline mode
- [ ] Multi-language support
- [ ] Batch processing

## 📊 Performance

- Image processing time: < 5 seconds
- API response time: < 1 second
- Accuracy: > 90%

## 🔍 Testing

To run tests:

```bash
python -m pytest
```

## 📈 Monitoring

The application includes:

- Error logging
- Performance monitoring
- User activity tracking

## 🔐 Security

- JWT authentication
- Password hashing
- CORS protection
- Rate limiting
- Input validation

## 🌐 API Documentation

### Authentication Endpoints

- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login user
- GET `/api/auth/profile` - Get user profile

### Prediction Endpoints

- POST `/api/predictions/predict` - Upload and analyze image
- GET `/api/predictions/history` - Get prediction history

## 🎯 Best Practices

1. Always use the virtual environment
2. Keep your `.env` file secure
3. Update packages regularly
4. Back up your database
5. Monitor server logs

## 🚨 Error Codes

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## 📱 Mobile Support

The API is mobile-friendly and supports:

- iOS
- Android
- Progressive Web Apps

## 🌍 Internationalization

Currently supports:

- English
- More languages coming soon


## 🔄 Updates

Check for updates:

```bash
git pull origin main
pip install -r requirements.txt
```

## 🎨 UI/UX

- Clean, modern interface
- Responsive design
- Dark/light mode
- Accessibility features

## 📦 Deployment

Deploy to:

- Heroku
- AWS
- DigitalOcean
- Google Cloud

## 🔍 Debugging

Enable debug mode:

```bash
export FLASK_DEBUG=1
```

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [JWT Documentation](https://jwt.io/)
- [Python Documentation](https://docs.python.org/)
