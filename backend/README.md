# Farm to Home - Python Backend API

This is the Python Flask backend for the Farm to Home website that automatically sends WhatsApp notifications when orders are placed.

## Features

- ✅ Automatic WhatsApp notifications via Twilio
- ✅ RESTful API endpoints
- ✅ CORS enabled for frontend integration
- ✅ Order validation
- ✅ Test endpoint for WhatsApp verification

## Prerequisites

- Python 3.8 or higher
- Twilio account (free trial available)
- pip (Python package manager)

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Get Twilio Credentials

1. **Sign up for Twilio** (Free Trial):
   - Go to https://www.twilio.com/try-twilio
   - Sign up for a free account
   - You'll get $15 free credit

2. **Get Your Credentials**:
   - Go to https://console.twilio.com/
   - Find your **Account SID** and **Auth Token**
   - Copy these values

3. **Set up WhatsApp Sandbox** (for testing):
   - Go to https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Follow instructions to connect your WhatsApp
   - Send the code to the Twilio WhatsApp number
   - Your WhatsApp is now connected!

### 3. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` file with your credentials:
```env
TWILIO_ACCOUNT_SID=your_actual_account_sid
TWILIO_AUTH_TOKEN=your_actual_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
YOUR_WHATSAPP_NUMBER=whatsapp:+917382055950
```

### 4. Run the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

You should see:
```
✅ Twilio credentials loaded
🚀 Starting Farm to Home API server...
📱 WhatsApp notifications will be sent to: whatsapp:+917382055950
```

## API Endpoints

### 1. Health Check
```
GET /api/health
```
Returns server status.

**Response:**
```json
{
  "status": "healthy",
  "message": "Farm to Home API is running"
}
```

### 2. Place Order
```
POST /api/place-order
```
Receives order data and sends WhatsApp notification.

**Request Body:**
```json
{
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "address": "123 Main St",
    "city": "Mumbai",
    "pincode": "400001"
  },
  "items": [
    {
      "name": "Alphonso Mangoes",
      "price": 1999,
      "quantity": 2
    }
  ],
  "total": 3998,
  "payment": "cod",
  "orderDate": "2024-03-27T10:00:00.000Z"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Order placed successfully and WhatsApp notification sent",
  "message_sid": "SM..."
}
```

### 3. Send Test Message
```
POST /api/send-test-message
```
Sends a test WhatsApp message to verify integration.

**Response:**
```json
{
  "success": true,
  "message": "Test WhatsApp message sent successfully",
  "message_sid": "SM..."
}
```

## Testing the Backend

### Test 1: Health Check
```bash
curl http://localhost:5000/api/health
```

### Test 2: Send Test WhatsApp Message
```bash
curl -X POST http://localhost:5000/api/send-test-message
```

Check your WhatsApp - you should receive a test message!

### Test 3: Place Test Order
```bash
curl -X POST http://localhost:5000/api/place-order \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "name": "Test Customer",
      "email": "test@example.com",
      "phone": "9876543210",
      "address": "Test Address",
      "city": "Mumbai",
      "pincode": "400001"
    },
    "items": [
      {
        "name": "Alphonso Mangoes",
        "price": 1999,
        "quantity": 1
      }
    ],
    "total": 1999,
    "payment": "cod",
    "orderDate": "2024-03-27T10:00:00.000Z"
  }'
```

## Frontend Integration

Update your frontend JavaScript to use the backend API:

```javascript
// In script.js, replace the sendOrderToWhatsApp function:

async function sendOrderToWhatsApp(orderData) {
    try {
        const response = await fetch('http://localhost:5000/api/place-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('WhatsApp notification sent successfully!');
        } else {
            console.error('Failed to send WhatsApp notification:', result.message);
        }
    } catch (error) {
        console.error('Error sending WhatsApp notification:', error);
    }
}
```

## Deployment

### Option 1: Deploy to Heroku (Free)

1. Install Heroku CLI
2. Create `Procfile`:
```
web: python app.py
```

3. Deploy:
```bash
heroku create farm-to-home-api
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set YOUR_WHATSAPP_NUMBER=whatsapp:+917382055950
git push heroku main
```

### Option 2: Deploy to Railway (Free)

1. Go to https://railway.app/
2. Connect your GitHub repo
3. Add environment variables
4. Deploy automatically

### Option 3: Deploy to PythonAnywhere (Free)

1. Go to https://www.pythonanywhere.com/
2. Upload your code
3. Set up virtual environment
4. Configure WSGI file
5. Add environment variables

## Troubleshooting

### Issue: "Twilio credentials not set"
**Solution:** Make sure your `.env` file exists and contains valid credentials.

### Issue: "WhatsApp message not received"
**Solution:** 
1. Verify you've connected your WhatsApp to Twilio sandbox
2. Check the phone number format: `whatsapp:+[country_code][number]`
3. Make sure you sent the join code to Twilio's WhatsApp number

### Issue: "CORS error in frontend"
**Solution:** The backend has CORS enabled. Make sure the backend is running on port 5000.

### Issue: "Module not found"
**Solution:** Run `pip install -r requirements.txt` again.

## Cost Information

### Twilio Pricing:
- **Free Trial**: $15 credit (enough for ~1000 messages)
- **WhatsApp Messages**: ~$0.005 per message
- **After Trial**: Pay-as-you-go pricing

### Free Alternatives:
- Use the current frontend-only solution (opens WhatsApp)
- Use email notifications instead
- Use Telegram Bot API (completely free)

## Security Notes

- ⚠️ Never commit `.env` file to Git
- ⚠️ Keep your Twilio credentials secret
- ✅ Use environment variables for sensitive data
- ✅ Enable rate limiting in production
- ✅ Add authentication for production use

## Support

For issues or questions:
- Twilio Docs: https://www.twilio.com/docs/whatsapp
- Flask Docs: https://flask.palletsprojects.com/

## License

MIT License - Feel free to use for your business!