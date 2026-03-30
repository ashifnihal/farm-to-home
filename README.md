# 🥭 Farm to Home - Premium Mango Delivery Platform

A complete e-commerce platform for renting mango trees and selling premium mangoes with integrated UPI payment gateway.

![Farm to Home](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Razorpay](https://img.shields.io/badge/Payment-Razorpay%20UPI-orange)

## 🌟 Features

### **Frontend**
- ✅ Responsive multi-page website
- ✅ Shopping cart system
- ✅ Real-time cart updates
- ✅ **Structured address collection (7 fields)** ✨
- ✅ **Comprehensive form validation (8 rules)** ✨
- ✅ **Real-time pincode validation** ✨
- ✅ Modern UI/UX design
- ✅ Image galleries
- ✅ Contact form
- ✅ Admin dashboard with structured address display
- ✅ User registration & authentication
- ✅ User dashboard (tabbed interface)

### **Backend**
- ✅ Flask REST API
- ✅ SQLite database
- ✅ **IST (Indian Standard Time) timezone support** ✨
- ✅ Email notifications (Mailgun)
- ✅ Order management
- ✅ Contact form handling
- ✅ Statistics dashboard
- ✅ User authentication (bcrypt)
- ✅ Security features (rate limiting, HTTPS)

### **Payment Gateway**
- ✅ Razorpay UPI integration
- ✅ Secure payment verification
- ✅ Multiple UPI apps support
- ✅ Test & Live modes
- ✅ Payment tracking

### **Products**
- 🥭 **6 Premium mango varieties** (Alphonso, Kesar, Banganapalli, Dasheri, Langra, Sindhura)
- 📏 **Sold by weight** - Kilograms (kg) instead of dozens
- 🌳 **3 Tree rental plans** (Starter, Premium, Royal)
- 🎖️ **Digital ownership certificates** for tree rentals
- 📦 Custom gift boxes
- 🚚 Bangalore Urban delivery only (101 pincodes)
- 💰 **Fixed delivery charges: ₹500** ✨

### **Delivery Coverage**
- 📍 **Bangalore Urban Only** (101 Pincodes)
- ✅ Real-time pincode validation
- ✅ Valid Range: 560001-560100, 560103
- ✅ Instant feedback (Green ✓ / Red ✗)
- ✅ Cannot place order with invalid pincode

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- pip
- Web browser

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd farm-to-home
```

2. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp backend/.env.example backend/.env
# Edit .env and add your Razorpay keys
```

4. **Start servers**

**Terminal 1 - Frontend:**
```bash
cd farm-to-home
python3 -m http.server 8000
```

**Terminal 2 - Backend:**
```bash
cd farm-to-home/backend
python app.py
```

5. **Access the platform**
```
http://localhost:8000
```

## 📚 Documentation

- **[Latest Updates](LATEST-UPDATES.md)** - Recent features & improvements ✨
- **[Delivery Charges](DELIVERY-CHARGES-UPDATE.md)** - Delivery charges implementation ✨
- **[Quick Start Guide](QUICK-START-GUIDE.md)** - Get started in 2 minutes
- **[UPI Payment Setup](UPI-PAYMENT-SETUP.md)** - Payment gateway configuration
- **[Payment Integration](PAYMENT-INTEGRATION-GUIDE.md)** - Technical details
- **[Backend API](backend/README.md)** - API documentation

## 🎯 Project Structure

```
farm-to-home/
├── index.html              # Home page
├── shop.html               # Shop mangoes
├── rent-trees.html         # Rent trees
├── about.html              # About us
├── contact.html            # Contact form
├── admin.html              # Admin dashboard
├── script.js               # Frontend JavaScript
├── styles.css              # Styling
├── images/                 # Images folder
│   ├── mangoes/           # Mango images
│   ├── trees/             # Tree images
│   ├── background/        # Background images
│   └── team/              # Team photos
├── backend/
│   ├── app.py             # Flask API server
│   ├── database.py        # Database operations
│   ├── .env               # Configuration (not in git)
│   ├── .env.example       # Example configuration
│   ├── requirements.txt   # Python dependencies
│   └── orders.db          # SQLite database (auto-created)
└── docs/
    ├── QUICK-START-GUIDE.md
    ├── UPI-PAYMENT-SETUP.md
    └── PAYMENT-INTEGRATION-GUIDE.md
```

## 🔧 Configuration

### Razorpay Setup

1. Sign up at https://razorpay.com
2. Get API keys from Dashboard → Settings → API Keys
3. Add to `backend/.env`:

```env
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_secret_key
```

### Email Setup (Mailgun)

**Now using Mailgun API for reliable email delivery!**

Add to `backend/.env`:

```env
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=your_sandbox_domain.mailgun.org
RECEIVER_EMAIL=your@email.com
```

**Features:**
- ✅ Fast delivery (1-2 seconds)
- ✅ 5,000 emails/month free
- ✅ No authentication issues
- ✅ Professional service

**Sign up:** https://signup.mailgun.com

## 🧪 Testing

### Test Pincode Validation

**Valid Bangalore Urban Pincodes:**
```
560001 - Bangalore GPO
560028 - Koramangala
560038 - Jayanagar
560100 - Yelahanka
560103 - Whitefield
... (101 pincodes total)
```

**Invalid Pincodes (Will be rejected):**
```
400001 - Mumbai (✗)
110001 - Delhi (✗)
560104 - Outside range (✗)
560200 - Outside range (✗)
```

**Validation Features:**
- ✅ Real-time validation as you type
- ✅ Green border for valid pincodes
- ✅ Red border for invalid pincodes
- ✅ Clear error messages
- ✅ Order blocked if pincode invalid

### Test UPI Payment

Use these test credentials:
- **Success:** `success@razorpay`
- **Failure:** `failure@razorpay`

### Test Cards

- **Card:** 4111 1111 1111 1111
- **Expiry:** Any future date
- **CVV:** Any 3 digits

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/place-order` | POST | Place order |
| `/api/create-payment-order` | POST | Create Razorpay order |
| `/api/verify-payment` | POST | Verify payment |
| `/api/orders` | GET | Get all orders |
| `/api/contact` | POST | Submit contact form |
| `/api/contacts` | GET | Get all contacts |
| `/api/statistics` | GET | Get statistics |

## 🌐 Pages

- **Home:** http://localhost:8000/index.html
- **Shop:** http://localhost:8000/shop.html
- **Rent Trees:** http://localhost:8000/rent-trees.html
- **About:** http://localhost:8000/about.html
- **Contact:** http://localhost:8000/contact.html
- **Admin:** http://localhost:8000/admin.html

## 💳 Payment Methods

- ✅ UPI (Google Pay, PhonePe, Paytm, etc.)
- ✅ Credit/Debit Cards
- ✅ Net Banking
- ✅ Wallets
- ✅ Cash on Delivery

## 🔒 Security

- ✅ Server-side payment verification
- ✅ HMAC-SHA256 signature validation
- ✅ Secure API keys in .env
- ✅ PCI DSS compliant
- ✅ HTTPS recommended for production

## 📱 Responsive Design

- ✅ Mobile-friendly
- ✅ Tablet optimized
- ✅ Desktop enhanced
- ✅ Cross-browser compatible

## 🎨 Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5
- AOS Animation Library
- Font Awesome Icons

**Backend:**
- Python 3.11
- Flask 3.0
- SQLite
- Razorpay SDK

**Payment:**
- Razorpay UPI Gateway
- Secure payment verification
- Multiple payment methods

## 📈 Features Roadmap

- [x] Shopping cart system
- [x] UPI payment integration
- [x] Order management
- [x] Admin dashboard
- [x] Email notifications
- [x] Contact form
- [x] **User authentication** ✨
- [x] **Structured address collection** ✨
- [x] **Comprehensive form validation** ✨
- [x] **IST timezone support** ✨
- [x] **Admin dashboard with structured addresses** ✨
- [ ] Order tracking
- [ ] SMS notifications
- [ ] Mobile app

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

- **Ashif Nihal** - Full Stack Developer
- **Abdul Rehman** - Backend Developer
- **Arif** - Frontend Developer

## 📞 Support

For support, email ashifnihal2012@gmail.com or visit our contact page.

## 🙏 Acknowledgments

- Razorpay for payment gateway
- Bootstrap for UI framework
- Font Awesome for icons
- AOS for animations

---

**Made with ❤️ in India** 🇮🇳

**From Our Orchards to Your Table - Freshness Guaranteed** 🥭✨