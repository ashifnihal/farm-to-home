from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
import pytz
from dotenv import load_dotenv
import requests
import razorpay
import hmac
import hashlib
import bcrypt
from security import PaymentSecurity, require_rate_limit, require_https

# Load environment variables
load_dotenv()

# Database selection based on environment variable
DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite').lower()

if DATABASE_TYPE == 'postgres':
    from database_postgres import DatabasePostgres as Database
    print("🐘 Using PostgreSQL database")
else:
    from database import Database
    print("📁 Using SQLite database")

# Set IST timezone
IST = pytz.timezone('Asia/Kolkata')

def get_ist_time():
    """Get current time in IST"""
    return datetime.now(IST)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize Database
db = Database()

# Mailgun Configuration
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
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
@require_rate_limit(max_requests=5, window=60)  # Max 5 orders per minute
@require_https()
def place_order():
    """
    Endpoint to receive order and send email notification
    Enhanced with payment recovery for failed saves
    SECURED: Rate limited + HTTPS required + Input validation
    """
    security = PaymentSecurity()
    
    try:
        # Get order data from request
        order_data = request.json
        
        # Sanitize input
        order_data = security.sanitize_input(order_data)
        
        # Validate order data
        valid, errors = security.validate_order_data(order_data)
        if not valid:
            security.log_security_event('INVALID_ORDER_DATA', f'Errors: {errors}')
            return jsonify({
                'success': False,
                'message': 'Invalid order data',
                'errors': errors
            }), 400
        
        # Detect suspicious activity
        warnings = security.detect_suspicious_activity(order_data)
        if warnings:
            security.log_security_event('SUSPICIOUS_ORDER', f'Warnings: {warnings}, IP: {request.remote_addr}')
            print(f"⚠️  Suspicious activity detected: {warnings}")
        
        # Validate required fields
        required_fields = ['customer', 'items', 'total', 'payment']
        if not all(field in order_data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Log payment details for recovery
        payment_id = order_data.get('razorpay_payment_id', 'N/A')
        order_id = order_data.get('razorpay_order_id', 'N/A')
        print(f"💳 Processing order with payment ID: {payment_id}")
        
        # Save order to database with retry logic
        max_retries = 3
        db_result = None
        
        for attempt in range(max_retries):
            try:
                db_result = db.add_order(order_data)
                if db_result['success']:
                    break
                print(f"⚠️  Retry {attempt + 1}/{max_retries}: {db_result.get('error')}")
            except Exception as retry_error:
                print(f"⚠️  Retry {attempt + 1}/{max_retries} failed: {str(retry_error)}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(0.5)  # Wait before retry
        
        if not db_result or not db_result['success']:
            error_msg = db_result.get('error', 'Unknown error') if db_result else 'Database connection failed'
            print(f"❌ Database error after {max_retries} attempts: {error_msg}")
            print(f"💳 PAYMENT COMPLETED BUT ORDER NOT SAVED!")
            print(f"💳 Payment ID: {payment_id}")
            print(f"💳 Order ID: {order_id}")
            print(f"💳 Customer: {order_data['customer']['name']} ({order_data['customer']['email']})")
            print(f"💳 Amount: ₹{order_data['total']}")
            
            # Log to file for manual recovery
            try:
                import json
                from datetime import datetime
                recovery_file = 'failed_orders.json'
                failed_order = {
                    'timestamp': datetime.now().isoformat(),
                    'payment_id': payment_id,
                    'order_id': order_id,
                    'order_data': order_data,
                    'error': error_msg
                }
                
                # Append to recovery file
                try:
                    with open(recovery_file, 'r') as f:
                        failed_orders = json.load(f)
                except:
                    failed_orders = []
                
                failed_orders.append(failed_order)
                
                with open(recovery_file, 'w') as f:
                    json.dump(failed_orders, f, indent=2)
                
                print(f"📝 Failed order logged to {recovery_file} for recovery")
            except Exception as log_error:
                print(f"❌ Could not log failed order: {str(log_error)}")
            
            return jsonify({
                'success': False,
                'message': f'Payment successful but order save failed. Payment ID: {payment_id}. Please contact support.',
                'payment_id': payment_id,
                'requires_manual_recovery': True
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
        print(f"❌ Critical error processing order: {str(e)}")
        print(f"💳 Payment ID: {order_data.get('razorpay_payment_id', 'N/A')}")
        return jsonify({
            'success': False,
            'message': f'Error processing order: {str(e)}',
            'payment_id': order_data.get('razorpay_payment_id')
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
    Send order notification via Mailgun API
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
    
    # Send via Mailgun API
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Farm to Home <mailgun@{MAILGUN_DOMAIN}>",
            "to": [RECEIVER_EMAIL],
            "subject": subject,
            "html": html_body,
            "h:Reply-To": f"{customer['name']} <{customer['email']}>"
        }
    )
    
    if response.status_code == 200:
        print(f"✅ Order email sent via Mailgun")
    else:
        print(f"❌ Mailgun error: {response.text}")
        raise Exception(f"Mailgun API error: {response.status_code}")

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
    """Send contact form notification via Mailgun API"""
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
    
    # Send via Mailgun API
    response = requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": f"Farm to Home Contact <mailgun@{MAILGUN_DOMAIN}>",
            "to": [RECEIVER_EMAIL],
            "subject": subject,
            "html": html_body,
            "h:Reply-To": f"{name} <{email}>"
        }
    )
    
    if response.status_code == 200:
        print(f"✅ Contact email sent via Mailgun")
    else:
        print(f"❌ Mailgun error: {response.text}")
        raise Exception(f"Mailgun API error: {response.status_code}")

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
@require_rate_limit(max_requests=10, window=60)  # Max 10 payment initiations per minute
@require_https()
def create_payment_order():
    """
    Create Razorpay payment order - UPI only
    SECURED: Rate limited + HTTPS required + Amount validation
    """
    security = PaymentSecurity()
    
    try:
        if not razorpay_client:
            return jsonify({
                'success': False,
                'message': 'Payment gateway not configured'
            }), 500
        
        data = request.json
        amount = data.get('amount')  # Amount in rupees
        
        # Validate amount
        valid, result = security.validate_amount(amount)
        if not valid:
            security.log_security_event('INVALID_AMOUNT', f'Amount: {amount}, IP: {request.remote_addr}')
            return jsonify({
                'success': False,
                'message': result
            }), 400
        
        amount = result  # Use validated amount
        
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
@require_rate_limit(max_requests=20, window=60)  # Max 20 verifications per minute
@require_https()
def verify_payment():
    """
    Verify Razorpay payment signature
    SECURED: Rate limited + HTTPS required + Signature verification
    """
    security = PaymentSecurity()
    
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
        
        # Use secure comparison
        if security.verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature, RAZORPAY_KEY_SECRET):
            print(f"✅ Payment verified successfully: {razorpay_payment_id}")
            security.log_security_event('PAYMENT_VERIFIED', f'Payment ID: {razorpay_payment_id}')
            return jsonify({
                'success': True,
                'message': 'Payment verified successfully'
            }), 200
        else:
            print(f"❌ Payment verification failed")
            security.log_security_event('PAYMENT_VERIFICATION_FAILED', f'Payment ID: {razorpay_payment_id}, IP: {request.remote_addr}')
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

@app.route('/api/failed-orders', methods=['GET'])
def get_failed_orders():
    """Get list of failed orders for manual recovery"""
    try:
        import json
        recovery_file = 'failed_orders.json'
        
        try:
            with open(recovery_file, 'r') as f:
                failed_orders = json.load(f)
            return jsonify({
                'success': True,
                'failed_orders': failed_orders,
                'count': len(failed_orders)
            }), 200
        except FileNotFoundError:
            return jsonify({
                'success': True,
                'failed_orders': [],
                'count': 0,
                'message': 'No failed orders found'
            }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/recover-order', methods=['POST'])
def recover_order():
    """Manually recover a failed order"""
    try:
        data = request.json
        payment_id = data.get('payment_id')
        
        if not payment_id:
            return jsonify({
                'success': False,
                'message': 'Payment ID is required'
            }), 400
        
        # Load failed orders
        import json
        recovery_file = 'failed_orders.json'
        
        try:
            with open(recovery_file, 'r') as f:
                failed_orders = json.load(f)
        except FileNotFoundError:
            return jsonify({
                'success': False,
                'message': 'No failed orders found'
            }), 404
        
        # Find the order
        order_to_recover = None
        remaining_orders = []
        
        for order in failed_orders:
            if order['payment_id'] == payment_id:
                order_to_recover = order
            else:
                remaining_orders.append(order)
        
        if not order_to_recover:
            return jsonify({
                'success': False,
                'message': f'Order with payment ID {payment_id} not found'
            }), 404
        
        # Try to save the order
        db_result = db.add_order(order_to_recover['order_data'])
        
        if db_result['success']:
            # Remove from failed orders file
            with open(recovery_file, 'w') as f:
                json.dump(remaining_orders, f, indent=2)
            
            print(f"✅ Recovered order: {db_result['order_number']}")
            
            return jsonify({
                'success': True,
                'message': 'Order recovered successfully',
                'order_number': db_result['order_number'],
                'order_id': db_result['order_id']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Failed to recover order: {db_result.get("error")}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/register', methods=['POST'])
@require_rate_limit(max_requests=5, window=300)  # Max 5 registrations per 5 minutes
def register_user():
    """Register a new user"""
    security = PaymentSecurity()
    
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'address', 'city', 'pincode', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Validate email
        valid, msg = security.validate_email(data['email'])
        if not valid:
            return jsonify({
                'success': False,
                'message': msg
            }), 400
        
        # Validate phone
        valid, msg = security.validate_phone(data['phone'])
        if not valid:
            return jsonify({
                'success': False,
                'message': msg
            }), 400
        
        # Validate pincode
        if not data['pincode'].isdigit() or len(data['pincode']) != 6:
            return jsonify({
                'success': False,
                'message': 'Pincode must be 6 digits'
            }), 400
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters'
            }), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        result = db.create_user(
            data['name'], 
            data['email'], 
            data['phone'], 
            data['address'],
            data['city'],
            data['pincode'],
            password_hash
        )
        
        if result['success']:
            security.log_security_event('USER_REGISTERED', f'Email: {data["email"]}')
            return jsonify({
                'success': True,
                'message': 'Account created successfully',
                'user_id': result['user_id']
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': result['error']
            }), 400
            
    except Exception as e:
        print(f"❌ Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/login', methods=['POST'])
@require_rate_limit(max_requests=10, window=300)  # Max 10 login attempts per 5 minutes
def login_user():
    """Login user"""
    security = PaymentSecurity()
    
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Get user from database
        user = db.get_user_by_email(data['email'])
        
        if not user:
            security.log_security_event('LOGIN_FAILED', f'Email not found: {data["email"]}, IP: {request.remote_addr}')
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Verify password
        if bcrypt.checkpw(data['password'].encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Update last login
            db.update_last_login(user['id'])
            
            security.log_security_event('LOGIN_SUCCESS', f'User: {user["email"]}')
            
            # Return user data (without password hash)
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'phone': user['phone']
                }
            }), 200
        else:
            security.log_security_event('LOGIN_FAILED', f'Wrong password for: {data["email"]}, IP: {request.remote_addr}')
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all registered users"""
    try:
        users = db.get_all_users()
        return jsonify({
            'success': True,
            'users': users,
            'count': len(users)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/send-test-email', methods=['POST'])
def send_test_email():
    """
    Test endpoint to verify Mailgun email integration
    """
    try:
        # Create test email
        subject = "🥭 Test Email from Farm to Home (Mailgun)"
        html_body = """
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #FFD700;">✅ Mailgun Integration Working!</h2>
                <p>This is a test email from your Farm to Home backend using Mailgun API.</p>
                <p>Your email notification system is set up correctly and ready to receive orders!</p>
                <hr>
                <p style="color: #666; font-size: 14px;">Farm to Home - Mango Delivery Service</p>
                <p style="color: #999; font-size: 12px;">Powered by Mailgun</p>
            </body>
        </html>
        """
        
        # Send via Mailgun API
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Farm to Home <mailgun@{MAILGUN_DOMAIN}>",
                "to": [RECEIVER_EMAIL],
                "subject": subject,
                "html": html_body
            }
        )
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Test email sent successfully via Mailgun! Check your inbox.'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': f'Mailgun API error: {response.status_code} - {response.text}'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to send test email: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Check if Mailgun credentials are set
    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        print("⚠️  WARNING: Mailgun credentials not set!")
        print("Please set MAILGUN_API_KEY and MAILGUN_DOMAIN in .env file")
    else:
        print("✅ Mailgun credentials loaded")
    
    print(f"🚀 Starting Farm to Home API server...")
    print(f"📧 Email notifications will be sent to: {RECEIVER_EMAIL}")
    print(f"📧 Using Mailgun domain: {MAILGUN_DOMAIN}")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5001)
