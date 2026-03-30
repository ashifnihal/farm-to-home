# 🥭 Farm to Home - Premium Mango Delivery Platform

A complete e-commerce platform for renting mango trees and selling premium mangoes with integrated UPI payment gateway, PostgreSQL database, and comprehensive mobile support.

![Farm to Home](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%2015-blue)
![Mobile](https://img.shields.io/badge/Mobile-Optimized-brightgreen)
![Razorpay](https://img.shields.io/badge/Payment-Razorpay%20UPI-orange)

## 🌟 Features

### **Frontend**
- ✅ Responsive multi-page website
- ✅ **100% Mobile Optimized (320px to 4K)** ✨
- ✅ **Touch-friendly interface (44px touch targets)** ✨
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
- ✅ **PWA-ready (Progressive Web App)** ✨

### **Backend**
- ✅ Flask REST API
- ✅ **Dual Database Support (SQLite/PostgreSQL)** ✨
- ✅ **PostgreSQL 15 with IST timezone** ✨
- ✅ **Production-ready database schema** ✨
- ✅ Email notifications (Mailgun)
- ✅ Order management
- ✅ Contact form handling
- ✅ Statistics dashboard
- ✅ User authentication (bcrypt)
- ✅ Security features (rate limiting, HTTPS)
- ✅ **Automatic database migration** ✨

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

### **Mobile Support** ✨
- 📱 **All Devices:** iPhone, Android, Tablets
- 📱 **Screen Sizes:** 320px to 4K displays
- 📱 **Touch Optimized:** 44px minimum touch targets
- 📱 **iOS Fixes:** No zoom on inputs, notch support
- 📱 **Android Optimized:** Smooth scrolling
- 📱 **Accessibility:** Reduced motion, keyboard navigation
- 📱 **Orientations:** Portrait & Landscape

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 15+ (optional, SQLite works too)
- pip
- Web browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ashifnihal/farm-to-home.git
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
# Edit .env and add your configuration
```

4. **Choose Database**

**Option A: SQLite (Default - No setup needed)**
```env
DATABASE_TYPE=sqlite
```

**Option B: PostgreSQL (Recommended for Production)**
```env
DATABASE_TYPE=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=farm_to_home
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
```

5. **Start servers**

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

6. **Access the platform**
```
http://localhost:8000
```

## 📚 Documentation

### **Latest Updates** ✨
- **[PostgreSQL Migration](POSTGRESQL-MIGRATION-COMPLETE.md)** - Complete PostgreSQL setup guide
- **[PostgreSQL Setup](backend/POSTGRES_SETUP.md)** - Database configuration
- **[Latest Updates](LATEST-UPDATES.md)** - Recent features & improvements
- **[Delivery Charges](DELIVERY-CHARGES-UPDATE.md)** - Delivery charges implementation

### **Guides**
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
├── login.html              # User login
├── register.html           # User registration
├── dashboard.html          # User dashboard
├── certificate.html        # Tree ownership certificate
├── script.js               # Frontend JavaScript
├── styles.css              # Styling (Mobile Optimized) ✨
├── images/                 # Images folder
│   ├── mangoes/           # Mango images
│   ├── trees/             # Tree images
│   ├── background/        # Background images
│   └── team/              # Team photos
├── backend/
│   ├── app.py             # Flask API server
│   ├── database.py        # SQLite database operations
│   ├── database_postgres.py  # PostgreSQL operations ✨
│   ├── security.py        # Security features
│   ├── .env               # Configuration (not in git)
│   ├── .env.example       # Example configuration
│   ├── requirements.txt   # Python dependencies
│   ├── orders.db          # SQLite database (auto-created)
│   └── README.md          # Backend documentation
└── docs/
    ├── POSTGRESQL-MIGRATION-COMPLETE.md  ✨
    ├── POSTGRES_SETUP.md                 ✨
    ├── QUICK-START-GUIDE.md
    ├── UPI-PAYMENT-SETUP.md
    └── PAYMENT-INTEGRATION-GUIDE.md
```

## 🔧 Configuration

### Database Setup

**SQLite (Default):**
```env
DATABASE_TYPE=sqlite
```
- ✅ No setup required
- ✅ Perfect for development
- ✅ Auto-creates database file

**PostgreSQL (Production):**
```env
DATABASE_TYPE=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=farm_to_home
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```
- ✅ Production-ready
- ✅ Better performance
- ✅ IST timezone support
- ✅ Scalable

See [PostgreSQL Setup Guide](backend/POSTGRES_SETUP.md) for detailed instructions.

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

### Test Mobile Responsiveness

**Method 1: Chrome DevTools**
```
1. Open website in Chrome
2. Press F12 (Developer Tools)
3. Click mobile icon (Ctrl+Shift+M)
4. Test devices:
   - iPhone SE (375px)
   - iPhone 12 Pro (390px)
   - Samsung Galaxy S20 (360px)
   - iPad (768px)
   - iPad Pro (1024px)
```

**Method 2: Real Devices**
- Test on your phone
- Try portrait and landscape
- Test touch interactions

**Method 3: Online Tools**
- Mobile-Friendly Test: https://search.google.com/test/mobile-friendly
- Responsive Checker: http://responsivedesignchecker.com/

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
| `/api/orders/<id>` | GET | Get order details |
| `/api/contact` | POST | Submit contact form |
| `/api/contacts` | GET | Get all contacts |
| `/api/statistics` | GET | Get statistics |
| `/api/users` | GET | Get all users |
| `/api/register` | POST | Register user |
| `/api/login` | POST | Login user |

## 🌐 Pages

- **Home:** http://localhost:8000/index.html
- **Shop:** http://localhost:8000/shop.html
- **Rent Trees:** http://localhost:8000/rent-trees.html
- **About:** http://localhost:8000/about.html
- **Contact:** http://localhost:8000/contact.html
- **Login:** http://localhost:8000/login.html
- **Register:** http://localhost:8000/register.html
- **Dashboard:** http://localhost:8000/dashboard.html
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
- ✅ Password hashing (bcrypt)
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CORS configured
- ✅ PCI DSS compliant
- ✅ HTTPS recommended for production

## 📱 Mobile Optimization Details

### **Supported Devices**
- ✅ iPhone 6/7/8 (375px)
- ✅ iPhone X/11/12/13/14/15 (390px-428px)
- ✅ Samsung Galaxy (360px-412px)
- ✅ Google Pixel (411px-432px)
- ✅ OnePlus (412px-480px)
- ✅ iPad Mini (768px)
- ✅ iPad (810px)
- ✅ iPad Pro (1024px)
- ✅ All Android tablets

### **Mobile Features**
- ✅ Touch-friendly buttons (44px minimum)
- ✅ No zoom on form inputs (16px font)
- ✅ Full-screen cart on mobile
- ✅ Stacked layouts for small screens
- ✅ Optimized images
- ✅ Fast loading
- ✅ Smooth scrolling
- ✅ No horizontal scroll
- ✅ Safe area support (iPhone notch)
- ✅ Landscape orientation support

### **Accessibility**
- ✅ Keyboard navigation
- ✅ Focus visible indicators
- ✅ Reduced motion support
- ✅ Screen reader friendly
- ✅ High contrast support

## 🎨 Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive Design (Mobile-First)
- Touch Optimized UI
- Progressive Enhancement
- Cross-browser Compatible

**Backend:**
- Python 3.9+
- Flask 3.0
- SQLite / PostgreSQL 15
- Razorpay SDK
- Mailgun API
- bcrypt (Password Hashing)

**Database:**
- SQLite (Development)
- PostgreSQL 15 (Production)
- IST Timezone Support
- Automatic Migrations

**Payment:**
- Razorpay UPI Gateway
- Secure payment verification
- Multiple payment methods

## 🚀 Deployment

### **Recommended Platforms**

**Free Tier:**
- **Render.com** (Recommended)
  - Free PostgreSQL (90 days)
  - Free web service
  - Auto-deploy from GitHub
  - SSL included

**Paid Tier:**
- **DigitalOcean** ($27/month)
- **AWS** ($30-50/month)
- **Heroku** ($12/month)

### **Quick Deploy to Render**

1. Push code to GitHub
2. Sign up at https://render.com
3. Create PostgreSQL database
4. Create web service
5. Add environment variables
6. Deploy!

See deployment guides in documentation.

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
- [x] **PostgreSQL database** ✨
- [x] **Mobile optimization** ✨
- [x] **Admin dashboard with structured addresses** ✨
- [ ] Order tracking
- [ ] SMS notifications
- [ ] Mobile app
- [ ] SEO optimization
- [ ] Analytics dashboard
- [ ] Multi-language support

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
- PostgreSQL for database
- Mailgun for email service
- Bootstrap for UI framework
- Font Awesome for icons
- AOS for animations

## 📊 Statistics

- **Lines of Code:** 10,000+
- **API Endpoints:** 15+
- **Database Tables:** 5
- **Supported Devices:** All (320px to 4K)
- **Payment Methods:** 5+
- **Delivery Pincodes:** 101

---

**Made with ❤️ in India** 🇮🇳

**From Our Orchards to Your Table - Freshness Guaranteed** 🥭✨

---

## 🔗 Quick Links

- **GitHub:** https://github.com/ashifnihal/farm-to-home
- **Documentation:** See `/docs` folder
- **Issues:** Report bugs on GitHub
- **Contact:** ashifnihal2012@gmail.com

---

**Version:** 2.0.0  
**Last Updated:** March 30, 2026  
**Status:** Production Ready ✅