# UPI Payment Integration - Complete Setup Guide

## 🎯 Overview
Your Farm to Home platform now supports **UPI payments only** through Razorpay payment gateway.

## 📋 What You Need

1. **Razorpay Account** (Free to create)
2. **Bank Account** (for receiving payments)
3. **Business Documents** (for KYC - only for live mode)

---

## 🚀 Step-by-Step Setup

### Step 1: Create Razorpay Account

1. Go to https://razorpay.com
2. Click "Sign Up" 
3. Enter your email and create password
4. Verify your email

### Step 2: Get Test API Keys (For Development)

1. Login to Razorpay Dashboard
2. Go to **Settings** → **API Keys**
3. Click **Generate Test Key**
4. Copy both:
   - **Key ID** (starts with `rzp_test_`)
   - **Key Secret** (keep this secret!)

### Step 3: Add Keys to Your Backend

1. Open `farm-to-home/backend/.env`
2. Add your keys:

```env
RAZORPAY_KEY_ID=rzp_test_SWI8qEixK6V90O
RAZORPAY_KEY_SECRET=NBtJWgmHRosx8B3uRGPMh2h8
```

### Step 4: Install Dependencies

```bash
cd farm-to-home/backend
pip install -r requirements.txt
```

This will install:
- Flask
- razorpay
- Other dependencies

### Step 5: Start Backend Server

```bash
cd farm-to-home/backend
python app.py
```

You should see:
```
✅ Razorpay client initialized
✅ Email credentials loaded
🚀 Starting Farm to Home API server...
```

---

## 💳 Testing UPI Payments

### Test Mode (FREE - No Real Money)

When using **Test Keys**, you can test payments without real money:

#### Test UPI IDs:
- **Success**: `success@razorpay`
- **Failure**: `failure@razorpay`

#### How to Test:
1. Add items to cart
2. Fill checkout form
3. Click "Confirm Order"
4. Razorpay payment modal opens
5. Select **UPI** payment method
6. Enter test UPI ID: `success@razorpay`
7. Payment will succeed automatically
8. Order saved to database

---

## 🔴 Going Live (Real Payments)

### Step 1: Complete KYC

1. Login to Razorpay Dashboard
2. Go to **Settings** → **Account & Settings**
3. Complete KYC verification:
   - Business details
   - Bank account details
   - PAN card
   - Business documents

**KYC takes 24-48 hours for approval**

### Step 2: Get Live API Keys

1. After KYC approval
2. Go to **Settings** → **API Keys**
3. Click **Generate Live Key**
4. Copy Live Keys (starts with `rzp_live_`)

### Step 3: Update .env with Live Keys

```env
RAZORPAY_KEY_ID=rzp_live_your_live_key_id
RAZORPAY_KEY_SECRET=your_live_secret_key
```

### Step 4: Restart Backend

```bash
python app.py
```

Now real payments will be processed!

---

## 💰 Payment Flow

```
1. Customer adds items to cart
   ↓
2. Customer fills checkout form
   ↓
3. Customer clicks "Confirm Order"
   ↓
4. Backend creates Razorpay order
   ↓
5. Razorpay payment modal opens (UPI only)
   ↓
6. Customer selects UPI app (GPay, PhonePe, Paytm, etc.)
   ↓
7. Customer completes payment in UPI app
   ↓
8. Payment verified by backend
   ↓
9. Order saved to database
   ↓
10. Email confirmation sent
   ↓
11. Success modal shown to customer
```

---

## 🎨 Supported UPI Apps

✅ Google Pay (GPay)
✅ PhonePe
✅ Paytm
✅ BHIM
✅ Amazon Pay
✅ WhatsApp Pay
✅ Any UPI app

---

## 💵 Pricing & Fees

### Razorpay Fees:
- **UPI**: 2% per transaction
- **No setup fee**
- **No annual fee**
- **No hidden charges**

### Example:
- Order Amount: ₹1,000
- Razorpay Fee: ₹20 (2%)
- You Receive: ₹980

### Settlement:
- Payments settled to your bank account
- **T+2 days** (2 working days)
- Automatic daily settlements

---

## 🔒 Security Features

✅ **PCI DSS Compliant**
✅ **Server-side payment verification**
✅ **Signature validation**
✅ **Encrypted API keys**
✅ **HTTPS recommended for production**
✅ **No card details stored**

---

## 📊 Dashboard Features

### Razorpay Dashboard:
- View all transactions
- Download reports
- Process refunds
- Track settlements
- View analytics
- Manage disputes

### Your Admin Dashboard:
- View orders
- Check payment status
- Manage customers
- View contact enquiries

---

## 🐛 Troubleshooting

### Payment Modal Not Opening?
- Check if Razorpay keys are set in .env
- Check if backend is running
- Check browser console for errors

### Payment Failing?
- In test mode: Use `success@razorpay`
- In live mode: Check if KYC is approved
- Check if bank account is active

### Order Not Saving?
- Check backend logs
- Verify payment was successful
- Check database connection

---

## 📞 Support

### Razorpay Support:
- Email: support@razorpay.com
- Phone: 1800-102-0480
- Docs: https://razorpay.com/docs/

### Integration Help:
- Razorpay Docs: https://razorpay.com/docs/payment-gateway/
- API Reference: https://razorpay.com/docs/api/

---

## ✅ Checklist

Before going live, ensure:

- [ ] Razorpay account created
- [ ] KYC completed and approved
- [ ] Live API keys generated
- [ ] Keys added to .env file
- [ ] Backend running successfully
- [ ] Test payment successful
- [ ] Bank account verified
- [ ] Email notifications working
- [ ] Admin dashboard accessible
- [ ] SSL certificate installed (HTTPS)

---

## 🎉 You're All Set!

Your Farm to Home platform is now ready to accept UPI payments!

**Test Mode**: Use test keys for development
**Live Mode**: Complete KYC and use live keys for real payments

Happy Selling! 🥭💰