from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database import Database
import razorpay
import hmac
import hashlib

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize Database
db = Database()

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')

# Initialize Razorpay client
razorpay_client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    print("✅ Razorpay client initialized")
else:
    print("⚠️  Razorpay keys not configured. Payment gateway will not work.")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Farm to Home API is running'
    }), 200

@app.route('/api/place-order', methods=['POST'])
def place_order():
    """
    Endpoint to receive order and send email notification
    """
    try:
        # Get order data from request
        order_data = request.json
        
        # Validate required fields
        required_fields = ['customer', 'items', 'total', 'payment']
        if not all(field in order_data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Save order to database
        db_result = db.add_order(order_data)
        
        if not db_result['success']:
            print(f"❌ Database error: {db_result['error']}")
            return jsonify({
                'success': False,
                'message': f'Failed to save order: {db_result["error"]}'
            }), 500
        
        print(f"✅ Order saved to database: {db_result['order_number']}")
        
        # Return response immediately - don't wait for email
        response = jsonify({
            'success': True,
            'message': 'Order placed successfully',
            'order_number': db_result['order_number'],
            'order_id': db_result['order_id']
        }), 200
        
        # Try to send email in background (non-blocking)
        try:
            import threading
            email_thread = threading.Thread(
                target=send_order_email_safe,
                args=(order_data, db_result['order_number'])
            )
            email_thread.daemon = True
            email_thread.start()
            print(f"📧 Email notification queued for sending...")
        except Exception as email_error:
            print(f"⚠️  Email error: {str(email_error)}")
        
        return response
            
    except Exception as e:
        print(f"Error processing order: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing order: {str(e)}'
        }), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        limit = request.args.get('limit', 100, type=int)
        orders = db.get_all_orders(limit)
        return jsonify({
            'success': True,
            'orders': orders,
            'count': len(orders)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get specific order details"""
    try:
        order = db.get_order_details(order_id)
        if order:
            return jsonify({
                'success': True,
                'order': order
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.json
        status = data.get('status')
        
        if not status:
            return jsonify({
                'success': False,
                'message': 'Status is required'
            }), 400
        
        db.update_order_status(order_id, status)
        return jsonify({
            'success': True,
            'message': 'Order status updated'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get database statistics"""
    try:
        stats = db.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/customer/<email>/orders', methods=['GET'])
def get_customer_orders(email):
    """Get all orders for a specific customer"""
    try:
        orders = db.get_customer_orders(email)
        return jsonify({
            'success': True,
            'orders': orders,
            'count': len(orders)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

def send_order_email_safe(order_data, order_number):
    """
    Wrapper to safely send email without blocking
    """
    try:
        send_order_email(order_data, order_number)
        print(f"✅ Email notification sent successfully!")
    except Exception as e:
        print(f"⚠️  Email sending failed: {str(e)}")

def send_order_email(order_data, order_number):
    """
    Send order notification via email
    """
    customer = order_data['customer']
    items = order_data['items']
    total = order_data['total']
    payment = order_data['payment']
    order_date = datetime.fromisoformat(order_data['orderDate'].replace('Z', '+00:00'))
    
    # Create email subject
    subject = f"🥭 NEW ORDER #{order_number} from {customer['name']} - ₹{total:,}"
    
    # Create HTML email body
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .header {{
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                color: #1a1a1a;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .content {{
                background: white;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .section {{
                margin-bottom: 25px;
                padding-bottom: 20px;
                border-bottom: 2px solid #f0f0f0;
            }}
            .section:last-child {{
                border-bottom: none;
            }}
            .section-title {{
                color: #FFD700;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .info-row {{
                margin: 8px 0;
            }}
            .label {{
                font-weight: bold;
                color: #666;
            }}
            .items-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            .items-table th {{
                background-color: #FFD700;
                color: #1a1a1a;
                padding: 12px;
                text-align: left;
            }}
            .items-table td {{
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
            }}
            .total-row {{
                background-color: #fff9e6;
                font-weight: bold;
                font-size: 18px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                padding: 20px;
                color: #666;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🥭 NEW ORDER - Farm to Home</h1>
                <p style="margin: 10px 0 0 0;">Order #{order_number}</p>
                <p style="margin: 5px 0 0 0;">Received on {order_date.strftime('%d %B %Y at %I:%M %p')}</p>
            </div>
            
            <div class="content">
                <!-- Customer Information -->
                <div class="section">
                    <div class="section-title">👤 Customer Information</div>
                    <div class="info-row"><span class="label">Name:</span> {customer['name']}</div>
                    <div class="info-row"><span class="label">Phone:</span> {customer['phone']}</div>
                    <div class="info-row"><span class="label">Email:</span> {customer['email']}</div>
                </div>
                
                <!-- Delivery Address -->
                <div class="section">
                    <div class="section-title">📍 Delivery Address</div>
                    <div class="info-row">{customer['address']}</div>
                    <div class="info-row">{customer['city']} - {customer['pincode']}</div>
                </div>
                
                <!-- Order Items -->
                <div class="section">
                    <div class="section-title">🛒 Order Items</div>
                    <table class="items-table">
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Qty</th>
                                <th>Price</th>
                                <th>Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Add items to table
    for item in items:
        subtotal = item['price'] * item['quantity']
        html_body += f"""
                            <tr>
                                <td>{item['name']}</td>
                                <td>{item['quantity']}</td>
                                <td>₹{item['price']:,}</td>
                                <td>₹{subtotal:,}</td>
                            </tr>
        """
    
    # Add total row
    html_body += f"""
                            <tr class="total-row">
                                <td colspan="3">TOTAL AMOUNT</td>
                                <td>₹{total:,}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <!-- Payment Information -->
                <div class="section">
                    <div class="section-title">💳 Payment Information</div>
                    <div class="info-row"><span class="label">Payment Method:</span> {payment.upper()}</div>
                    <div class="info-row"><span class="label">Total Amount:</span> ₹{total:,}</div>
                </div>
            </div>
            
            <div class="footer">
                <p>🥭 Farm to Home - From Our Orchards to Your Table</p>
                <p>Please confirm this order with the customer at {customer['phone']}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Create email message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = f"Farm to Home <{SENDER_EMAIL}>"
    message['To'] = RECEIVER_EMAIL
    message['Reply-To'] = f"{customer['name']} <{customer['email']}>"  # Customer's email for easy reply
    
    # Attach HTML body
    html_part = MIMEText(html_body, 'html')
    message.attach(html_part)
    
    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    try:
        data = request.json
        print(f"📧 Contact form submission received from: {data.get('name')}")
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({
                'success': False,
                'message': 'Name, email, and message are required'
            }), 400
        
        # Save to database
        result = db.add_contact(data)
        
        if result['success']:
            print(f"✅ Contact saved to database with ID: {result['contact_id']}")
            
            # Send email notification in background
            try:
                import threading
                email_thread = threading.Thread(
                    target=send_contact_email_safe,
                    args=(data,)
                )
                email_thread.daemon = True
                email_thread.start()
                print(f"📧 Contact email notification queued for sending...")
            except Exception as email_error:
                print(f"⚠️  Email error: {str(email_error)}")
            
            return jsonify({
                'success': True,
                'contact_id': result['contact_id'],
                'message': 'Contact form submitted successfully'
            })
        else:
            print(f"❌ Failed to save contact: {result.get('error')}")
            return jsonify({
                'success': False,
                'message': result.get('error', 'Failed to save contact')
            }), 500
            
    except Exception as e:
        print(f"❌ Error processing contact form: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

def send_contact_email_safe(contact_data):
    """Wrapper to safely send contact email without blocking"""
    try:
        send_contact_email(contact_data)
        print(f"✅ Contact email notification sent successfully!")
    except Exception as e:
        print(f"⚠️  Contact email sending failed: {str(e)}")

def send_contact_email(contact_data):
    """Send contact form notification via email"""
    name = contact_data.get('name')
    email = contact_data.get('email')
    phone = contact_data.get('phone', 'Not provided')
    message = contact_data.get('message')
    
    # Create email subject
    subject = f"📧 New Contact Form Submission from {name}"
    
    # Create HTML email body
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .header {{
                background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .content {{
                background: white;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .section {{
                margin-bottom: 25px;
                padding-bottom: 20px;
                border-bottom: 2px solid #f0f0f0;
            }}
            .section:last-child {{
                border-bottom: none;
            }}
            .section-title {{
                color: #4CAF50;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .info-row {{
                margin: 8px 0;
            }}
            .label {{
                font-weight: bold;
                color: #666;
            }}
            .message-box {{
                background-color: #f8f8f8;
                padding: 20px;
                border-left: 4px solid #4CAF50;
                border-radius: 5px;
                margin-top: 15px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                padding: 20px;
                color: #666;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📧 New Contact Form Submission</h1>
                <p style="margin: 10px 0 0 0;">Farm to Home</p>
            </div>
            
            <div class="content">
                <!-- Contact Information -->
                <div class="section">
                    <div class="section-title">👤 Contact Information</div>
                    <div class="info-row"><span class="label">Name:</span> {name}</div>
                    <div class="info-row"><span class="label">Email:</span> <a href="mailto:{email}">{email}</a></div>
                    <div class="info-row"><span class="label">Phone:</span> {phone}</div>
                </div>
                
                <!-- Message -->
                <div class="section">
                    <div class="section-title">💬 Message</div>
                    <div class="message-box">
                        {message}
                    </div>
                </div>
                
                <!-- Action Required -->
                <div class="section">
                    <div class="section-title">⚡ Action Required</div>
                    <p>Please respond to this inquiry within 24 hours.</p>
                    <p><strong>Reply to:</strong> <a href="mailto:{email}">{email}</a></p>
                    <p><strong>Call:</strong> {phone}</p>
                </div>
            </div>
            
            <div class="footer">
                <p>🥭 Farm to Home - Contact Form Notification</p>
                <p>This is an automated notification from your website</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Create email message
    email_message = MIMEMultipart('alternative')
    email_message['Subject'] = subject
    email_message['From'] = f"Farm to Home Contact <{SENDER_EMAIL}>"
    email_message['To'] = RECEIVER_EMAIL
    email_message['Reply-To'] = f"{name} <{email}>"  # Customer's email for easy reply
    
    # Attach HTML body
    html_part = MIMEText(html_body, 'html')
    email_message.attach(html_part)
    
    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(email_message)

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contact form submissions"""
    try:
        contacts = db.get_all_contacts()
        return jsonify({
            'success': True,
            'contacts': contacts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/create-payment-order', methods=['POST'])
def create_payment_order():
    """Create Razorpay payment order - UPI only"""
    try:
        if not razorpay_client:
            return jsonify({
                'success': False,
                'message': 'Payment gateway not configured'
            }), 500
        
        data = request.json
        amount = data.get('amount')  # Amount in rupees
        
        if not amount:
            return jsonify({
                'success': False,
                'message': 'Amount is required'
            }), 400
        
        # Create Razorpay order
        order_data = {
            'amount': int(amount * 100),  # Convert to paise
            'currency': 'INR',
            'payment_capture': 1  # Auto capture
        }
        
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        return jsonify({
            'success': True,
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency'],
            'key_id': RAZORPAY_KEY_ID
        }), 200
        
    except Exception as e:
        print(f"❌ Error creating payment order: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    """Verify Razorpay payment signature"""
    try:
        data = request.json
        
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return jsonify({
                'success': False,
                'message': 'Missing payment verification data'
            }), 400
        
        # Verify signature
        generated_signature = hmac.new(
            RAZORPAY_KEY_SECRET.encode(),
            f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if generated_signature == razorpay_signature:
            print(f"✅ Payment verified successfully: {razorpay_payment_id}")
            return jsonify({
                'success': True,
                'message': 'Payment verified successfully'
            }), 200
        else:
            print(f"❌ Payment verification failed")
            return jsonify({
                'success': False,
                'message': 'Payment verification failed'
            }), 400
            
    except Exception as e:
        print(f"❌ Error verifying payment: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/send-test-email', methods=['POST'])
def send_test_email():
    """
    Test endpoint to verify email integration
    """
    try:
        # Create test email
        subject = "🥭 Test Email from Farm to Home"
        body = """
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #FFD700;">✅ Email Integration Working!</h2>
                <p>This is a test email from your Farm to Home backend.</p>
                <p>Your email notification system is set up correctly and ready to receive orders!</p>
                <hr>
                <p style="color: #666; font-size: 14px;">Farm to Home - Mango Delivery Service</p>
            </body>
        </html>
        """
        
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = SENDER_EMAIL
        message['To'] = RECEIVER_EMAIL
        
        html_part = MIMEText(body, 'html')
        message.attach(html_part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        
        return jsonify({
            'success': True,
            'message': 'Test email sent successfully! Check your inbox.'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to send test email: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Check if email credentials are set
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("⚠️  WARNING: Email credentials not set!")
        print("Please set SENDER_EMAIL and SENDER_PASSWORD in .env file")
    else:
        print("✅ Email credentials loaded")
    
    print(f"🚀 Starting Farm to Home API server...")
    print(f"📧 Email notifications will be sent to: {RECEIVER_EMAIL}")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5001)
