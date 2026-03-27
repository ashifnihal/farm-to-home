# 🚀 Farm to Home - Quick Start Guide

## Complete Setup in 2 Minutes

This guide will help you run your Farm to Home platform with UPI payment gateway.

---

## 📋 Prerequisites

Before starting, make sure you have:

- ✅ Python 3.x installed
- ✅ pip (Python package manager)
- ✅ A code editor (VS Code recommended)
- ✅ A web browser (Chrome/Firefox/Safari)

---

## 🎯 Complete Setup

### **Terminal 1 - Frontend Server**

Open your first terminal and run:

```bash
cd farm-to-home
python3 -m http.server 8000
```

**Expected Output:**
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

✅ **Frontend is now running on:** http://localhost:8000

---

### **Terminal 2 - Backend Server**

Open a **second terminal** (keep Terminal 1 running) and run:

```bash
cd farm-to-home/backend
python app.py
```

**Expected Output:**
```
✅ Razorpay client initialized
✅ Email credentials loaded
🚀 Starting Farm to Home API server...
📧 Email notifications will be sent to: your-email@gmail.com
 * Running on http://0.0.0.0:5001
```

✅ **Backend API is now running on:** http://localhost:5001

---

## 🔑 Configure Razorpay (Required for Payments)

### Step 1: Get Razorpay Keys

1. Sign up at https://razorpay.com
2. Go to **Settings** → **API Keys**
3. Click **Generate Test Key**
4. Copy both:
   - Key ID (starts with `rzp_test_`)
   - Key Secret

### Step 2: Add Keys to .env

Open `farm-to-home/backend/.env` and add:

```env
# Razorpay Payment Gateway
RAZORPAY_KEY_ID=rzp_test_your_key_id_here
RAZORPAY_KEY_SECRET=your_secret_key_here
```

### Step 3: Restart Backend

Stop Terminal 2 (Ctrl+C) and restart:

```bash
python app.py
```

---

## 🌐 Access Your Platform

### **Main Website**
```
http://localhost:8000
```

### **Available Pages:**

| Page | URL |
|------|-----|
| 🏠 Home | http://localhost:8000/index.html |
| 🥭 Shop Mangoes | http://localhost:8000/shop.html |
| 🌳 Rent Trees | http://localhost:8000/rent-trees.html |
| ℹ️ About Us | http://localhost:8000/about.html |
| 📧 Contact | http://localhost:8000/contact.html |
| 👨‍💼 Admin Dashboard | http://localhost:8000/admin.html |

---

## 💳 Test UPI Payment

### Step 1: Add Items to Cart
1. Go to http://localhost:8000/shop.html
2. Click "Add to Cart" on any mango variety
3. Click the cart icon (🛒) in navigation

### Step 2: Checkout
1. Fill in your details:
   - Name, Email, Phone
   - Delivery Address
   - City, Pincode
2. Click "Confirm Order"

### Step 3: UPI Payment
1. Razorpay payment modal will open
2. Select **UPI** payment method
3. Use test UPI ID: `success@razorpay`
4. Payment will succeed automatically!

### Step 4: Success!
- ✅ Order saved to database
- ✅ Email confirmation sent
- ✅ Success modal displayed
- ✅ Invoice available for download

---

## 🧪 Test Credentials

### **Test UPI IDs:**
- **Success:** `success@razorpay`
- **Failure:** `failure@razorpay`

### **Test Cards (if needed):**
- **Card Number:** 4111 1111 1111 1111
- **Expiry:** Any future date
- **CVV:** Any 3 digits

---

## 📊 Admin Dashboard

Access the admin panel at:
```
http://localhost:8000/admin.html
```

**Features:**
- 📦 View all orders
- 👥 Manage customers
- 📧 View contact enquiries
- 📊 Statistics dashboard
- 🔍 Search and filter orders

---

## 🛑 Stop Servers

### Stop Frontend (Terminal 1):
```
Press Ctrl+C
```

### Stop Backend (Terminal 2):
```
Press Ctrl+C
```

---

## 🔄 Restart Servers

Just run the same commands again:

**Terminal 1:**
```bash
cd farm-to-home
python3 -m http.server 8000
```

**Terminal 2:**
```bash
cd farm-to-home/backend
python app.py
```

---

## 📁 Project Structure

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
├── backend/
│   ├── app.py             # Flask API server
│   ├── database.py        # Database operations
│   ├── .env               # Configuration (add your keys here)
│   ├── .env.example       # Example configuration
│   ├── requirements.txt   # Python dependencies
│   └── orders.db          # SQLite database (auto-created)
└── docs/
    ├── UPI-PAYMENT-SETUP.md
    ├── PAYMENT-INTEGRATION-GUIDE.md
    └── QUICK-START-GUIDE.md (this file)
```

---

## 🐛 Troubleshooting

### Port Already in Use?

**Frontend (8000):**
```bash
# Use different port
python3 -m http.server 8001
# Then access: http://localhost:8001
```

**Backend (5001):**
```bash
# Edit app.py, change last line to:
app.run(debug=True, host='0.0.0.0', port=5002)
```

### Payment Not Working?

1. ✅ Check if both servers are running
2. ✅ Verify Razorpay keys in .env
3. ✅ Hard refresh browser (Ctrl+Shift+R)
4. ✅ Check browser console for errors
5. ✅ Ensure you're using http://localhost:8000 (not file://)

### Database Errors?

Delete and recreate:
```bash
cd farm-to-home/backend
rm orders.db
python app.py
# Database will be recreated automatically
```

---

## 📚 Additional Documentation

- **UPI Payment Setup:** `UPI-PAYMENT-SETUP.md`
- **Payment Integration:** `PAYMENT-INTEGRATION-GUIDE.md`
- **Backend README:** `backend/README.md`

---

## 🎉 You're All Set!

Your Farm to Home platform is now running with:

✅ **Frontend:** http://localhost:8000
✅ **Backend API:** http://localhost:5001
✅ **UPI Payment Gateway:** Razorpay
✅ **Database:** SQLite
✅ **Email Notifications:** Configured
✅ **Admin Dashboard:** Ready

**Start testing and enjoy your mango delivery platform!** 🥭💰✨

---

## 💡 Pro Tips

1. **Keep both terminals open** while testing
2. **Use test mode** for development (free)
3. **Complete KYC** before going live
4. **Monitor backend logs** for debugging
5. **Check admin dashboard** for orders

---

## 📞 Need Help?

- Check `UPI-PAYMENT-SETUP.md` for detailed payment setup
- Review `PAYMENT-INTEGRATION-GUIDE.md` for technical details
- Contact Razorpay support: support@razorpay.com

---

**Happy Coding! 🚀**