# Payment Gateway Integration Guide - Razorpay

## Overview
This guide explains how to integrate Razorpay payment gateway into your Farm to Home platform.

## Prerequisites
1. Create a Razorpay account at https://razorpay.com
2. Get your API keys from Razorpay Dashboard
3. Install Razorpay Python SDK

## Step 1: Install Razorpay SDK

```bash
cd farm-to-home/backend
pip install razorpay
```

## Step 2: Update .env file

Add these to your `backend/.env`:

```env
# Razorpay Configuration
RAZORPAY_KEY_ID=your_razorpay_key_id_here
RAZORPAY_KEY_SECRET=your_razorpay_key_secret_here
```

## Step 3: Backend Implementation

The backend code has been updated with:
- `/api/create-payment-order` - Creates Razorpay order
- `/api/verify-payment` - Verifies payment signature
- Payment verification before order confirmation

## Step 4: Frontend Implementation

The frontend (`script.js`) has been updated with:
- Razorpay checkout integration
- Payment success/failure handling
- Automatic order creation after successful payment

## Step 5: Testing

### Test Mode (Free)
1. Use Razorpay Test Keys
2. Test card: 4111 1111 1111 1111
3. Any future expiry date
4. Any CVV

### Live Mode
1. Complete KYC verification on Razorpay
2. Use Live Keys
3. Real payments will be processed

## Payment Flow

1. User adds items to cart
2. User fills checkout form
3. User clicks "Confirm Order"
4. Razorpay payment modal opens
5. User completes payment
6. Payment verified by backend
7. Order saved to database
8. Email confirmation sent
9. Success modal shown

## Security Features

✅ Server-side payment verification
✅ Signature validation
✅ Secure API keys in .env
✅ HTTPS recommended for production

## Supported Payment Methods

- Credit/Debit Cards
- UPI (Google Pay, PhonePe, Paytm)
- Net Banking
- Wallets (Paytm, PhonePe, etc.)
- EMI options

## Important Notes

1. **Test Mode**: Use test keys for development
2. **Live Mode**: Complete KYC before going live
3. **Webhooks**: Set up webhooks for payment notifications
4. **Refunds**: Can be processed from Razorpay dashboard
5. **Settlement**: Payments settled to bank account in 2-3 days

## Getting Razorpay Keys

1. Sign up at https://razorpay.com
2. Go to Settings → API Keys
3. Generate Test Keys (for development)
4. Generate Live Keys (after KYC for production)

## Support

- Razorpay Docs: https://razorpay.com/docs/
- Razorpay Support: support@razorpay.com
- Integration Help: https://razorpay.com/docs/payment-gateway/

## Next Steps

1. ✅ Create Razorpay account
2. ✅ Get API keys
3. ✅ Add keys to .env file
4. ✅ Install razorpay package
5. ✅ Test with test keys
6. ✅ Complete KYC for live mode
7. ✅ Switch to live keys