// Shopping Cart System
let cart = JSON.parse(localStorage.getItem('farmToHomeCart')) || [];

// Update cart count
function updateCartCount() {
    const cartCount = document.querySelector('.cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
}

// Add to cart function
function addToCart(productName, price, image, type = 'mango') {
    const existingItem = cart.find(item => item.name === productName);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            name: productName,
            price: price,
            image: image,
            quantity: 1,
            type: type
        });
    }
    
    localStorage.setItem('farmToHomeCart', JSON.stringify(cart));
    updateCartCount();
    showNotification(`${productName} added to cart!`);
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'error' ? '#f44336' : '#4CAF50'};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        max-width: 300px;
        font-weight: 600;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add event listeners to all "Add to Cart" buttons
document.querySelectorAll('.btn-cart').forEach((button, index) => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const productCard = this.closest('.product-card');
        const productName = productCard.querySelector('h3').textContent;
        const priceText = productCard.querySelector('.price').textContent;
        const price = parseInt(priceText.replace(/[^0-9]/g, ''));
        const image = productCard.querySelector('img')?.src || 'mango-icon.png';
        
        addToCart(productName, price, image, 'mango');
    });
});

// Add event listeners to "Rent Now" buttons
document.querySelectorAll('.plan-card .btn-primary').forEach((button, index) => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        const planCard = this.closest('.plan-card');
        const planName = planCard.querySelector('h3').textContent;
        const priceText = planCard.querySelector('.price').textContent;
        const price = parseInt(priceText.replace(/[^0-9]/g, ''));
        const image = planCard.querySelector('img')?.src || 'tree-icon.png';
        
        addToCart(planName, price, image, 'tree');
    });
});

// Cart icon click - show cart modal
document.querySelector('.cart-icon').addEventListener('click', function(e) {
    e.preventDefault();
    showCartModal();
});

// Show cart modal
function showCartModal() {
    const existingModal = document.querySelector('.cart-modal');
    if (existingModal) existingModal.remove();
    
    const modal = document.createElement('div');
    modal.className = 'cart-modal';
    
    let cartHTML = `
        <div class="cart-modal-content">
            <div class="cart-header">
                <h2>🛒 Your Cart</h2>
                <button class="close-modal">&times;</button>
            </div>
            <div class="cart-items">
    `;
    
    if (cart.length === 0) {
        cartHTML += '<p class="empty-cart">Your cart is empty</p>';
    } else {
        cart.forEach((item, index) => {
            cartHTML += `
                <div class="cart-item">
                    <img src="${item.image}" alt="${item.name}" onerror="this.style.display='none'">
                    <div class="cart-item-details">
                        <h4>${item.name}</h4>
                        <p class="cart-item-price">₹${item.price.toLocaleString('en-IN')}</p>
                    </div>
                    <div class="cart-item-quantity">
                        <button class="qty-btn" onclick="updateQuantity(${index}, -1)">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-btn" onclick="updateQuantity(${index}, 1)">+</button>
                    </div>
                    <button class="remove-item" onclick="removeFromCart(${index})">🗑️</button>
                </div>
            `;
        });
        
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cartHTML += `
            </div>
            <div class="cart-footer">
                <div class="cart-total">
                    <span>Total:</span>
                    <span class="total-amount">₹${total.toLocaleString('en-IN')}</span>
                </div>
                <button class="btn btn-primary" onclick="proceedToCheckout()">Place Order</button>
            </div>
        `;
    }
    
    cartHTML += '</div>';
    modal.innerHTML = cartHTML;
    document.body.appendChild(modal);
    
    setTimeout(() => modal.classList.add('show'), 10);
    
    modal.querySelector('.close-modal').addEventListener('click', () => {
        modal.classList.remove('show');
        setTimeout(() => modal.remove(), 300);
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 300);
        }
    });
}

// Update quantity
function updateQuantity(index, change) {
    cart[index].quantity += change;
    if (cart[index].quantity <= 0) {
        cart.splice(index, 1);
    }
    localStorage.setItem('farmToHomeCart', JSON.stringify(cart));
    updateCartCount();
    showCartModal();
}

// Remove from cart
function removeFromCart(index) {
    const itemName = cart[index].name;
    cart.splice(index, 1);
    localStorage.setItem('farmToHomeCart', JSON.stringify(cart));
    updateCartCount();
    showNotification(`${itemName} removed from cart`);
    showCartModal();
}

// Proceed to checkout
function proceedToCheckout() {
    if (cart.length === 0) {
        showNotification('Your cart is empty!');
        return;
    }
    
    const modal = document.querySelector('.cart-modal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => modal.remove(), 300);
    }
    
    showCheckoutModal();
}

// Show checkout modal
function showCheckoutModal() {
    const modal = document.createElement('div');
    modal.className = 'cart-modal';
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    modal.innerHTML = `
        <div class="cart-modal-content checkout-modal">
            <div class="cart-header">
                <h2>📦 Checkout</h2>
                <button class="close-modal">&times;</button>
            </div>
            <form class="checkout-form" onsubmit="placeOrder(event)">
                <div class="form-group">
                    <label>Full Name *</label>
                    <input type="text" name="name" required placeholder="Enter your full name">
                </div>
                <div class="form-group">
                    <label>Email *</label>
                    <input type="email" name="email" required placeholder="your@email.com">
                </div>
                <div class="form-group">
                    <label>Phone Number *</label>
                    <input type="tel" name="phone" required placeholder="+91 XXXXX XXXXX" pattern="[0-9]{10}">
                </div>
                <h3 style="margin: 1.5rem 0 1rem 0; color: #333; border-bottom: 2px solid #FFD700; padding-bottom: 0.5rem;">📍 Delivery Address</h3>
                <div class="form-group">
                    <label>House/Flat Number, Building Name *</label>
                    <input type="text" name="house" required placeholder="e.g., Flat 301, Green Valley Apartments">
                </div>
                <div class="form-group">
                    <label>Street / Area / Locality *</label>
                    <input type="text" name="street" required placeholder="e.g., 15th Cross, Indiranagar">
                </div>
                <div class="form-group">
                    <label>Landmark (Optional)</label>
                    <input type="text" name="landmark" placeholder="e.g., Near Metro Station, Opposite Park">
                </div>
                <div class="form-group">
                    <label>City *</label>
                    <input type="text" name="city" required value="Bangalore" readonly style="background-color: #f0f0f0; cursor: not-allowed;">
                    <small style="color: #667eea; font-size: 12px; display: block; margin-top: 5px;">Currently delivering to Bangalore only</small>
                </div>
                <div class="form-group">
                    <label>State *</label>
                    <input type="text" name="state" required value="Karnataka" readonly style="background-color: #f0f0f0; cursor: not-allowed;">
                </div>
                <div class="form-group">
                    <label>PIN Code *</label>
                    <input type="text" name="pincode" id="checkoutPincode" required placeholder="Enter 6-digit pincode" pattern="[0-9]{6}" maxlength="6" style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px;">
                    <small id="checkoutPincodeHelp" style="color: #667eea; font-size: 12px; display: block; margin-top: 5px;">Bangalore Urban pincodes only (560001-560103)</small>
                    <small id="checkoutPincodeError" style="color: #f44336; font-size: 12px; display: none; margin-top: 5px;"></small>
                </div>
                <div class="form-group">
                    <label>Country *</label>
                    <input type="text" name="country" required value="India" readonly style="background-color: #f0f0f0; cursor: not-allowed;">
                </div>
                <div style="display: none;">
                    <select name="pincode_hidden">
                        <option value="">Select your area</option>
                        <option value="560001">560001 - Bangalore GPO</option>
                        <option value="560002">560002 - Bangalore City</option>
                        <option value="560003">560003 - Malleshwaram</option>
                        <option value="560004">560004 - Malleshwaram West</option>
                        <option value="560005">560005 - Rajajinagar</option>
                        <option value="560006">560006 - Chamrajpet</option>
                        <option value="560007">560007 - Sheshadripuram</option>
                        <option value="560008">560008 - Sadashivanagar</option>
                        <option value="560009">560009 - Majestic</option>
                        <option value="560010">560010 - Rajajinagar Industrial</option>
                        <option value="560011">560011 - Basavanagudi</option>
                        <option value="560012">560012 - Hanumanthanagar</option>
                        <option value="560013">560013 - Gavipuram</option>
                        <option value="560014">560014 - Jayanagar 4th Block</option>
                        <option value="560015">560015 - Vijayanagar</option>
                        <option value="560016">560016 - Basaveshwaranagar</option>
                        <option value="560017">560017 - Malleshwaram</option>
                        <option value="560018">560018 - Yelahanka</option>
                        <option value="560019">560019 - Jalahalli</option>
                        <option value="560020">560020 - Rajajinagar</option>
                        <option value="560021">560021 - Jayanagar</option>
                        <option value="560022">560022 - Banashankari</option>
                        <option value="560023">560023 - Girinagar</option>
                        <option value="560024">560024 - Banashankari 2nd Stage</option>
                        <option value="560025">560025 - Kengeri</option>
                        <option value="560026">560026 - Richmond Town</option>
                        <option value="560027">560027 - Shantinagar</option>
                        <option value="560028">560028 - Koramangala</option>
                        <option value="560029">560029 - Indiranagar</option>
                        <option value="560030">560030 - Ulsoor</option>
                        <option value="560031">560031 - Frazer Town</option>
                        <option value="560032">560032 - Benson Town</option>
                        <option value="560033">560033 - Jayamahal</option>
                        <option value="560034">560034 - Koramangala 5th Block</option>
                        <option value="560035">560035 - Koramangala 6th Block</option>
                        <option value="560036">560036 - Koramangala 7th Block</option>
                        <option value="560037">560037 - Koramangala 8th Block</option>
                        <option value="560038">560038 - Jayanagar 3rd Block</option>
                        <option value="560039">560039 - Banashankari 3rd Stage</option>
                        <option value="560040">560040 - Jayanagar 9th Block</option>
                        <option value="560041">560041 - Jayanagar 2nd Block</option>
                        <option value="560042">560042 - Wilson Garden</option>
                        <option value="560043">560043 - Shantinagar</option>
                        <option value="560044">560044 - Ejipura</option>
                        <option value="560045">560045 - Viveknagar</option>
                        <option value="560046">560046 - Magrath Road</option>
                        <option value="560047">560047 - Koramangala 1st Block</option>
                        <option value="560048">560048 - Koramangala 2nd Block</option>
                        <option value="560049">560049 - Koramangala 3rd Block</option>
                        <option value="560050">560050 - Koramangala 4th Block</option>
                        <option value="560051">560051 - Domlur</option>
                        <option value="560052">560052 - Indiranagar 2nd Stage</option>
                        <option value="560053">560053 - Hoysala Nagar</option>
                        <option value="560054">560054 - Hennur</option>
                        <option value="560055">560055 - Kammanahalli</option>
                        <option value="560056">560056 - Lingarajapuram</option>
                        <option value="560057">560057 - Rajajinagar 5th Block</option>
                        <option value="560058">560058 - Rajajinagar 6th Block</option>
                        <option value="560059">560059 - Rajajinagar 7th Block</option>
                        <option value="560060">560060 - Rajajinagar 8th Block</option>
                        <option value="560061">560061 - Yelahanka New Town</option>
                        <option value="560062">560062 - Yelahanka</option>
                        <option value="560063">560063 - Yelahanka Satellite Town</option>
                        <option value="560064">560064 - Yelahanka</option>
                        <option value="560065">560065 - Yelahanka</option>
                        <option value="560066">560066 - Jalahalli</option>
                        <option value="560067">560067 - Rajajinagar</option>
                        <option value="560068">560068 - Peenya</option>
                        <option value="560069">560069 - Peenya 2nd Stage</option>
                        <option value="560070">560070 - Banashankari</option>
                        <option value="560071">560071 - Chamarajpet</option>
                        <option value="560072">560072 - Chickpet</option>
                        <option value="560073">560073 - Cottonpet</option>
                        <option value="560074">560074 - Kalasipalya</option>
                        <option value="560075">560075 - Gandhinagar</option>
                        <option value="560076">560076 - Seshadripuram</option>
                        <option value="560077">560077 - Yeshwanthpur</option>
                        <option value="560078">560078 - Malleswaram</option>
                        <option value="560079">560079 - Rajajinagar</option>
                        <option value="560080">560080 - Nagarbhavi</option>
                        <option value="560081">560081 - Vijayanagar</option>
                        <option value="560082">560082 - Chandra Layout</option>
                        <option value="560083">560083 - Mahalakshmi Layout</option>
                        <option value="560084">560084 - Rajarajeshwari Nagar</option>
                        <option value="560085">560085 - Uttarahalli</option>
                        <option value="560086">560086 - Yeshwanthpur</option>
                        <option value="560087">560087 - Jalahalli East</option>
                        <option value="560088">560088 - Jalahalli West</option>
                        <option value="560089">560089 - Mathikere</option>
                        <option value="560090">560090 - Yeshwanthpur</option>
                        <option value="560091">560091 - Hebbal</option>
                        <option value="560092">560092 - Hebbal Kempapura</option>
                        <option value="560093">560093 - Sahakara Nagar</option>
                        <option value="560094">560094 - Vidyaranyapura</option>
                        <option value="560095">560095 - Yelahanka</option>
                        <option value="560096">560096 - Yelahanka</option>
                        <option value="560097">560097 - Yelahanka</option>
                        <option value="560098">560098 - Doddaballapur Road</option>
                        <option value="560099">560099 - Yelahanka</option>
                        <option value="560100">560100 - Yelahanka</option>
                        <option value="560103">560103 - Whitefield</option>
                    </select>
                    <small style="color: #667eea; font-size: 12px; display: block; margin-top: 5px;">Select your Bangalore Urban area</small>
                </div>
                <div class="form-group">
                    <label>Payment Method *</label>
                    <select name="payment" required>
                        <option value="upi" selected>UPI Payment (Google Pay, PhonePe, Paytm, etc.)</option>
                    </select>
                    <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">
                        💳 Secure UPI payment powered by Razorpay
                    </p>
                </div>
                <div class="order-summary">
                    <h3>Order Summary</h3>
                    <div class="summary-items">
                        ${cart.map(item => `
                            <div class="summary-item">
                                <span>${item.name} x ${item.quantity}</span>
                                <span>₹${(item.price * item.quantity).toLocaleString('en-IN')}</span>
                            </div>
                        `).join('')}
                    </div>
                    <div class="summary-total">
                        <span>Total Amount:</span>
                        <span class="total-amount">₹${total.toLocaleString('en-IN')}</span>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">
                    Confirm Order
                </button>
            </form>
        </div>
    `;
    
    document.body.appendChild(modal);
    setTimeout(() => modal.classList.add('show'), 10);
    
    // Add pincode validation after modal is created
    setTimeout(() => {
        const pincodeInput = document.getElementById('checkoutPincode');
        if (pincodeInput) {
            const validPincodes = [
                '560001', '560002', '560003', '560004', '560005', '560006', '560007', '560008', '560009', '560010',
                '560011', '560012', '560013', '560014', '560015', '560016', '560017', '560018', '560019', '560020',
                '560021', '560022', '560023', '560024', '560025', '560026', '560027', '560028', '560029', '560030',
                '560031', '560032', '560033', '560034', '560035', '560036', '560037', '560038', '560039', '560040',
                '560041', '560042', '560043', '560044', '560045', '560046', '560047', '560048', '560049', '560050',
                '560051', '560052', '560053', '560054', '560055', '560056', '560057', '560058', '560059', '560060',
                '560061', '560062', '560063', '560064', '560065', '560066', '560067', '560068', '560069', '560070',
                '560071', '560072', '560073', '560074', '560075', '560076', '560077', '560078', '560079', '560080',
                '560081', '560082', '560083', '560084', '560085', '560086', '560087', '560088', '560089', '560090',
                '560091', '560092', '560093', '560094', '560095', '560096', '560097', '560098', '560099', '560100',
                '560103'
            ];
            
            pincodeInput.addEventListener('input', function(e) {
                const pincode = e.target.value;
                const pincodeError = document.getElementById('checkoutPincodeError');
                const pincodeHelp = document.getElementById('checkoutPincodeHelp');
                
                if (pincode.length === 6) {
                    if (validPincodes.includes(pincode)) {
                        e.target.style.borderColor = '#4CAF50';
                        pincodeError.style.display = 'none';
                        pincodeHelp.style.display = 'block';
                        pincodeHelp.textContent = '✓ Valid Bangalore Urban pincode';
                        pincodeHelp.style.color = '#4CAF50';
                    } else {
                        e.target.style.borderColor = '#f44336';
                        pincodeHelp.style.display = 'none';
                        pincodeError.style.display = 'block';
                        pincodeError.textContent = '✗ Invalid pincode. We only deliver to Bangalore Urban (560001-560103)';
                    }
                } else {
                    e.target.style.borderColor = '#ddd';
                    pincodeError.style.display = 'none';
                    pincodeHelp.style.display = 'block';
                    pincodeHelp.textContent = 'Bangalore Urban pincodes only (560001-560103)';
                    pincodeHelp.style.color = '#667eea';
                }
            });
        }
    }, 100);
    
    modal.querySelector('.close-modal').addEventListener('click', () => {
        modal.classList.remove('show');
        setTimeout(() => modal.remove(), 300);
    });
    
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 300);
        }
    });
}

// Place order with UPI payment
async function placeOrder(event) {
    event.preventDefault();
    
    // Get the submit button and disable it to prevent duplicate submissions
    const submitButton = event.target.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    
    // Get form data first for validation
    const formData = new FormData(event.target);
    const name = formData.get('name')?.trim();
    const email = formData.get('email')?.trim();
    const phone = formData.get('phone')?.trim();
    const house = formData.get('house')?.trim();
    const street = formData.get('street')?.trim();
    const landmark = formData.get('landmark')?.trim() || '';
    const city = formData.get('city')?.trim();
    const state = formData.get('state')?.trim();
    const pincode = formData.get('pincode')?.trim();
    const country = formData.get('country')?.trim();
    
    // Comprehensive validation before processing
    
    // 1. Validate Name (minimum 3 characters, only letters and spaces)
    if (!name || name.length < 3) {
        showNotification('Please enter a valid name (minimum 3 characters)', 'error');
        event.target.querySelector('input[name="name"]').focus();
        return;
    }
    if (!/^[a-zA-Z\s]+$/.test(name)) {
        showNotification('Name should contain only letters and spaces', 'error');
        event.target.querySelector('input[name="name"]').focus();
        return;
    }
    
    // 2. Validate Email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
        showNotification('Please enter a valid email address', 'error');
        event.target.querySelector('input[name="email"]').focus();
        return;
    }
    
    // 3. Validate Phone (exactly 10 digits)
    if (!phone || !/^[0-9]{10}$/.test(phone)) {
        showNotification('Please enter a valid 10-digit phone number', 'error');
        event.target.querySelector('input[name="phone"]').focus();
        return;
    }
    
    // 4. Validate House/Flat Number (minimum 3 characters)
    if (!house || house.length < 3) {
        showNotification('Please enter house/flat number and building name', 'error');
        event.target.querySelector('input[name="house"]').focus();
        return;
    }
    
    // 5. Validate Street/Area (minimum 5 characters)
    if (!street || street.length < 5) {
        showNotification('Please enter street/area/locality', 'error');
        event.target.querySelector('input[name="street"]').focus();
        return;
    }
    
    // 6. Validate City (must be Bangalore)
    if (!city || city.toLowerCase() !== 'bangalore') {
        showNotification('We currently deliver only to Bangalore', 'error');
        return;
    }
    
    // 7. Validate State (must be Karnataka)
    if (!state || state.toLowerCase() !== 'karnataka') {
        showNotification('We currently deliver only to Karnataka', 'error');
        return;
    }
    
    // 8. Validate Bangalore Urban pincode
    const validPincodes = [
        '560001', '560002', '560003', '560004', '560005', '560006', '560007', '560008', '560009', '560010',
        '560011', '560012', '560013', '560014', '560015', '560016', '560017', '560018', '560019', '560020',
        '560021', '560022', '560023', '560024', '560025', '560026', '560027', '560028', '560029', '560030',
        '560031', '560032', '560033', '560034', '560035', '560036', '560037', '560038', '560039', '560040',
        '560041', '560042', '560043', '560044', '560045', '560046', '560047', '560048', '560049', '560050',
        '560051', '560052', '560053', '560054', '560055', '560056', '560057', '560058', '560059', '560060',
        '560061', '560062', '560063', '560064', '560065', '560066', '560067', '560068', '560069', '560070',
        '560071', '560072', '560073', '560074', '560075', '560076', '560077', '560078', '560079', '560080',
        '560081', '560082', '560083', '560084', '560085', '560086', '560087', '560088', '560089', '560090',
        '560091', '560092', '560093', '560094', '560095', '560096', '560097', '560098', '560099', '560100',
        '560103'
    ];
    
    if (!pincode || !validPincodes.includes(pincode)) {
        showNotification('Invalid pincode! We only deliver to Bangalore Urban (560001-560103)', 'error');
        const pincodeInput = document.getElementById('checkoutPincode');
        if (pincodeInput) {
            pincodeInput.style.borderColor = '#f44336';
            pincodeInput.focus();
        }
        return;
    }
    
    // Disable button and show loading state
    submitButton.disabled = true;
    submitButton.innerHTML = '⏳ Processing...';
    submitButton.style.opacity = '0.6';
    submitButton.style.cursor = 'not-allowed';
    
    try {
        // Build complete address string
        const fullAddress = `${house}, ${street}${landmark ? ', ' + landmark : ''}, ${city}, ${state} - ${pincode}, ${country}`;
        
        const orderData = {
            customer: {
                name: name,
                email: email,
                phone: phone,
                address: fullAddress,
                house: house,
                street: street,
                landmark: landmark,
                city: city,
                state: state,
                pincode: pincode,
                country: country
            },
            payment: 'upi',  // Always UPI
            items: cart,
            total: cart.reduce((sum, item) => sum + (item.price * item.quantity), 0),
            orderDate: new Date().toISOString()
        };
        
        console.log('Initiating UPI payment for order:', orderData);
        
        // Initiate Razorpay UPI payment
        await initiateRazorpayPayment(orderData, submitButton, originalButtonText);
        
    } catch (error) {
        console.error('Error placing order:', error);
        
        // Re-enable button on error
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
        submitButton.style.opacity = '1';
        submitButton.style.cursor = 'pointer';
        
        showNotification('An error occurred. Please try again.', 'error');
    }
}

// Initiate Razorpay UPI Payment
async function initiateRazorpayPayment(orderData, submitButton, originalButtonText) {
    const API_URL = 'http://localhost:5001';
    
    try {
        // Step 1: Create payment order on backend
        console.log('📤 Creating payment order...');
        const orderResponse = await fetch(`${API_URL}/api/create-payment-order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: orderData.total
            })
        });
        
        if (!orderResponse.ok) {
            throw new Error('Failed to create payment order');
        }
        
        const orderResult = await orderResponse.json();
        console.log('✅ Payment order created:', orderResult);
        
        // Step 2: Open Razorpay checkout with UPI only
        const options = {
            key: orderResult.key_id,
            amount: orderResult.amount,
            currency: orderResult.currency,
            name: 'Farm to Home',
            description: 'Premium Mango Order',
            image: 'https://your-logo-url.com/logo.png', // Optional: Add your logo
            order_id: orderResult.order_id,
            method: {
                upi: true,  // Enable UPI only
                card: false,
                netbanking: false,
                wallet: false
            },
            prefill: {
                name: orderData.customer.name,
                email: orderData.customer.email,
                contact: orderData.customer.phone
            },
            theme: {
                color: '#FFD700'
            },
            handler: async function (response) {
                // Payment successful - verify and save order
                console.log('✅ Payment successful:', response);
                await verifyAndSaveOrder(response, orderData, submitButton, originalButtonText);
            },
            modal: {
                ondismiss: function() {
                    // Payment cancelled
                    console.log('❌ Payment cancelled by user');
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalButtonText;
                    submitButton.style.opacity = '1';
                    submitButton.style.cursor = 'pointer';
                    showNotification('Payment cancelled', 'error');
                }
            }
        };
        
        // Open Razorpay checkout
        const rzp = new Razorpay(options);
        rzp.open();
        
    } catch (error) {
        console.error('❌ Error initiating payment:', error);
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
        submitButton.style.opacity = '1';
        submitButton.style.cursor = 'pointer';
        showNotification('Payment initiation failed. Please try again.', 'error');
    }
}

// Verify payment and save order
async function verifyAndSaveOrder(paymentResponse, orderData, submitButton, originalButtonText) {
    const API_URL = 'http://localhost:5001';
    
    try {
        // Step 1: Verify payment signature
        console.log('🔐 Verifying payment...');
        const verifyResponse = await fetch(`${API_URL}/api/verify-payment`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                razorpay_order_id: paymentResponse.razorpay_order_id,
                razorpay_payment_id: paymentResponse.razorpay_payment_id,
                razorpay_signature: paymentResponse.razorpay_signature
            })
        });
        
        const verifyResult = await verifyResponse.json();
        
        if (!verifyResult.success) {
            throw new Error('Payment verification failed');
        }
        
        console.log('✅ Payment verified successfully');
        
        // Step 2: Save order to database with payment details
        console.log('💾 Saving order to database...');
        const saveResponse = await fetch(`${API_URL}/api/place-order`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ...orderData,
                upi_id: paymentResponse.upi_id || null,
                razorpay_order_id: paymentResponse.razorpay_order_id,
                razorpay_payment_id: paymentResponse.razorpay_payment_id,
                payment_status: 'paid'
            })
        });
        
        const saveResult = await saveResponse.json();
        
        if (saveResult.success) {
            console.log('✅ Order saved successfully:', saveResult.order_number);
            
            // Clear cart
            cart = [];
            localStorage.setItem('farmToHomeCart', JSON.stringify(cart));
            updateCartCount();
            
            // Close checkout modal
            const modal = document.querySelector('.cart-modal');
            if (modal) {
                modal.classList.remove('show');
                setTimeout(() => modal.remove(), 300);
            }
            
            // Show success modal
            showSuccessModal(orderData, saveResult.order_number);
            showNotification('Payment successful! Order placed.', 'success');
        } else {
            throw new Error('Failed to save order');
        }
        
    } catch (error) {
        console.error('❌ Error verifying/saving order:', error);
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
        submitButton.style.opacity = '1';
        submitButton.style.cursor = 'pointer';
        showNotification('Order processing failed. Please contact support with payment ID: ' + paymentResponse.razorpay_payment_id, 'error');
    }
}

// Send order to WhatsApp via Backend API
async function sendOrderToWhatsApp(orderData) {
    const API_URL = 'http://localhost:5001/api/place-order';
    
    try {
        console.log('📤 Sending order to backend...', orderData);
        console.log('📤 API URL:', API_URL);
        
        // Add timeout to fetch request
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        console.log('📥 Response received!');
        console.log('📥 Response status:', response.status);
        console.log('📥 Response ok:', response.ok);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Response error:', errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('📥 Response data:', result);
        
        if (result.success && result.order_number) {
            console.log('✅ Order saved to database successfully!');
            console.log('Order Number:', result.order_number);
            showNotification('Order placed successfully! ✅', 'success');
            return result.order_number;
        } else {
            console.error('❌ Failed to save order:', result.message || 'Unknown error');
            showNotification('Failed to place order. Please try again.', 'error');
            return null;
        }
    } catch (error) {
        if (error.name === 'AbortError') {
            console.error('❌ Request timeout after 30 seconds');
            showNotification('Request timeout. Please check your connection and try again.', 'error');
        } else {
            console.error('❌ Error connecting to backend:', error);
            showNotification('Cannot connect to server. Please ensure backend is running on port 5001.', 'error');
        }
        return null;
    }
}

// Fallback function to open WhatsApp manually
function openWhatsAppManually(orderData) {
    const whatsappNumber = '917382055950';
    
    let message = `🥭 *NEW ORDER - Farm to Home* 🥭\n\n`;
    message += `📋 *Order Details:*\n`;
    message += `━━━━━━━━━━━━━━━━\n\n`;
    message += `👤 *Customer Information:*\n`;
    message += `Name: ${orderData.customer.name}\n`;
    message += `Phone: ${orderData.customer.phone}\n`;
    message += `Email: ${orderData.customer.email}\n\n`;
    message += `📍 *Delivery Address:*\n`;
    message += `${orderData.customer.address}\n`;
    message += `${orderData.customer.city} - ${orderData.customer.pincode}\n\n`;
    message += `🛒 *Order Items:*\n`;
    orderData.items.forEach((item, index) => {
        message += `${index + 1}. ${item.name}\n`;
        message += `   Qty: ${item.quantity} | Price: ₹${item.price.toLocaleString('en-IN')}\n`;
        message += `   Subtotal: ₹${(item.price * item.quantity).toLocaleString('en-IN')}\n\n`;
    });
    message += `━━━━━━━━━━━━━━━━\n`;
    message += `💰 *Total Amount: ₹${orderData.total.toLocaleString('en-IN')}*\n\n`;
    message += `💳 *Payment Method:* ${orderData.payment.toUpperCase()}\n\n`;
    const orderDate = new Date(orderData.orderDate);
    message += `📅 *Order Date:* ${orderDate.toLocaleString('en-IN')}\n\n`;
    message += `━━━━━━━━━━━━━━━━\n`;
    message += `Please confirm this order! 🙏`;
    
    const encodedMessage = encodeURIComponent(message);
    const whatsappURL = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`;
    window.open(whatsappURL, '_blank');
}

// Global variable to store last order data for invoice
let lastOrderData = null;

// Show success modal
function showSuccessModal(orderData, orderNumber = null) {
    const modal = document.createElement('div');
    modal.className = 'cart-modal';
    
    // MUST use database Order ID only - no manual generation
    if (!orderNumber) {
        showNotification('Error: Could not retrieve Order ID from database. Please contact support.', 'error');
        console.error('❌ Order ID not received from database');
        return;
    }
    
    const orderId = orderNumber;
    
    // Store order data globally for invoice download
    lastOrderData = {
        orderId: orderId,
        orderData: orderData
    };
    
    modal.innerHTML = `
        <div class="cart-modal-content success-modal">
            <button class="close-modal" onclick="closeSuccessModal()" style="position: absolute; top: 15px; right: 15px; background: none; border: none; font-size: 30px; cursor: pointer; color: #999; line-height: 1; padding: 0; width: 30px; height: 30px;">&times;</button>
            <div class="success-icon">✅</div>
            <h2>Order Placed Successfully!</h2>
            <p>Thank you for your order, ${orderData.customer.name}!</p>
            <div class="order-details">
                <p style="background: #f8f8f8; padding: 15px; border-radius: 8px; font-size: 1.2rem; margin: 1rem 0;">
                    <strong>Order ID:</strong> <span style="color: #FFD700; font-weight: 900;">${orderId}</span>
                </p>
                <p><strong>Order Total:</strong> ₹${orderData.total.toLocaleString('en-IN')}</p>
                <p><strong>Payment Method:</strong> ${orderData.payment.toUpperCase()}</p>
                <p><strong>Delivery Address:</strong> ${orderData.customer.address}, ${orderData.customer.city} - ${orderData.customer.pincode}</p>
            </div>
            <p class="success-message">Your order details have been sent to your email (${orderData.customer.email}). We'll contact you shortly at ${orderData.customer.phone} to confirm your order.</p>
            <p style="color: #4CAF50; font-weight: 600; margin-top: 1rem;">📧 Email confirmation sent automatically!</p>
            <div style="display: flex; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap;">
                <button class="btn btn-primary" onclick="downloadInvoiceFromGlobal()">
                    📄 Download Invoice
                </button>
                <button class="btn btn-secondary" onclick="closeSuccessModal()">Continue Shopping</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    setTimeout(() => modal.classList.add('show'), 10);
}

// Close success modal
function closeSuccessModal() {
    const modal = document.querySelector('.cart-modal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => modal.remove(), 300);
    }
}

// Initialize cart count on page load
updateCartCount();

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        // Skip if href is just '#' or empty
        if (!href || href === '#' || href.length <= 1) {
            return;
        }
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.plan-card, .product-card, .feature, .step-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Download Invoice from global variable
function downloadInvoiceFromGlobal() {
    if (!lastOrderData) {
        showNotification('Error: Order data not found. Please try again.', 'error');
        return;
    }
    downloadInvoice(lastOrderData.orderId, lastOrderData.orderData);
}

// Download Invoice Function
function downloadInvoice(orderId, orderData) {
    const orderDate = new Date(orderData.orderDate);
    
    // Create invoice HTML
    const invoiceHTML = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Invoice - ${orderId}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; padding: 40px; background: #fff; }
        .invoice-container { max-width: 800px; margin: 0 auto; border: 2px solid #000; padding: 30px; }
        .header { text-align: center; border-bottom: 3px solid #FFD700; padding-bottom: 20px; margin-bottom: 30px; }
        .company-name { font-size: 32px; font-weight: bold; color: #FFD700; margin-bottom: 5px; }
        .company-tagline { font-size: 14px; color: #666; font-style: italic; }
        .invoice-title { font-size: 24px; font-weight: bold; margin: 20px 0; text-align: center; }
        .invoice-details { display: flex; justify-content: space-between; margin-bottom: 30px; }
        .detail-section { flex: 1; }
        .detail-section h3 { font-size: 16px; margin-bottom: 10px; color: #333; border-bottom: 2px solid #FFD700; padding-bottom: 5px; }
        .detail-section p { margin: 5px 0; font-size: 14px; line-height: 1.6; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th { background: #FFD700; color: #000; padding: 12px; text-align: left; font-weight: bold; }
        td { padding: 12px; border-bottom: 1px solid #ddd; }
        .total-row { background: #f8f8f8; font-weight: bold; font-size: 16px; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 2px solid #FFD700; text-align: center; font-size: 12px; color: #666; }
        .thank-you { text-align: center; margin: 30px 0; font-size: 18px; color: #4CAF50; font-weight: bold; }
        @media print { body { padding: 0; } .invoice-container { border: none; } }
    </style>
</head>
<body>
    <div class="invoice-container">
        <div class="header">
            <div class="company-name">🥭 FARM TO HOME 🥭</div>
            <div class="company-tagline">Nature's Gold, Delivered Fresh</div>
            <p style="margin-top: 10px; font-size: 12px;">
                📍 Chittoor, Andhra Pradesh 517001<br>
                📞 +91 8247221546 | 📧 care@farmtohome.in
            </p>
        </div>
        
        <div class="invoice-title">TAX INVOICE</div>
        
        <div class="invoice-details">
            <div class="detail-section">
                <h3>Invoice Details</h3>
                <p><strong>Invoice No:</strong> ${orderId}</p>
                <p><strong>Date:</strong> ${orderDate.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })}</p>
                <p><strong>Time:</strong> ${orderDate.toLocaleTimeString('en-IN')}</p>
                <p><strong>Payment:</strong> ${orderData.payment.toUpperCase()}</p>
            </div>
            
            <div class="detail-section">
                <h3>Bill To</h3>
                <p><strong>${orderData.customer.name}</strong></p>
                <p>${orderData.customer.address}</p>
                <p>${orderData.customer.city} - ${orderData.customer.pincode}</p>
                <p>📞 ${orderData.customer.phone}</p>
                <p>📧 ${orderData.customer.email}</p>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">#</th>
                    <th>Item Description</th>
                    <th style="width: 80px; text-align: center;">Qty</th>
                    <th style="width: 120px; text-align: right;">Price</th>
                    <th style="width: 120px; text-align: right;">Amount</th>
                </tr>
            </thead>
            <tbody>
                ${orderData.items.map((item, index) => `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${item.name}</td>
                        <td style="text-align: center;">${item.quantity}</td>
                        <td style="text-align: right;">₹${item.price.toLocaleString('en-IN')}</td>
                        <td style="text-align: right;">₹${(item.price * item.quantity).toLocaleString('en-IN')}</td>
                    </tr>
                `).join('')}
                <tr class="total-row">
                    <td colspan="4" style="text-align: right;">TOTAL AMOUNT:</td>
                    <td style="text-align: right;">₹${orderData.total.toLocaleString('en-IN')}</td>
                </tr>
            </tbody>
        </table>
        
        <div style="margin: 20px 0; padding: 15px; background: #f8f8f8; border-left: 4px solid #FFD700;">
            <p style="margin: 5px 0;"><strong>Amount in Words:</strong> ${numberToWords(orderData.total)} Rupees Only</p>
        </div>
        
        <div class="thank-you">
            ✅ Thank you for your order!
        </div>
        
        <div style="margin: 20px 0; padding: 15px; background: #fff9e6; border: 1px solid #FFD700; border-radius: 5px;">
            <p style="font-size: 13px; line-height: 1.6; margin: 5px 0;">
                <strong>Terms & Conditions:</strong><br>
                • All mangoes are 100% organic and farm-fresh<br>
                • Delivery within 48 hours of order confirmation<br>
                • For any queries, contact us at +91 8247221546<br>
                • This is a computer-generated invoice
            </p>
        </div>
        
        <div class="footer">
            <p><strong>Farm to Home®</strong> - India's Premium Mango Delivery Service</p>
            <p>Cultivating Excellence, Delivering Happiness</p>
            <p style="margin-top: 10px;">🥭 From Our Orchards to Your Table - Freshness Guaranteed 🥭</p>
        </div>
    </div>
</body>
</html>
    `;
    
    // Create a Blob and download
    const blob = new Blob([invoiceHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Invoice_${orderId}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification('Invoice downloaded successfully! 📄');
}

// Convert number to words (for invoice)
function numberToWords(num) {
    const ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'];
    const tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];
    const teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
    
    if (num === 0) return 'Zero';
    
    function convertHundreds(n) {
        let str = '';
        if (n > 99) {
            str += ones[Math.floor(n / 100)] + ' Hundred ';
            n %= 100;
        }
        if (n > 19) {
            str += tens[Math.floor(n / 10)] + ' ';
            n %= 10;
        } else if (n > 9) {
            str += teens[n - 10] + ' ';
            return str;
        }
        if (n > 0) {
            str += ones[n] + ' ';
        }
        return str;
    }
    
    let result = '';
    if (num >= 10000000) {
        result += convertHundreds(Math.floor(num / 10000000)) + 'Crore ';
        num %= 10000000;
    }
    if (num >= 100000) {
        result += convertHundreds(Math.floor(num / 100000)) + 'Lakh ';
        num %= 100000;
    }
    if (num >= 1000) {
        result += convertHundreds(Math.floor(num / 1000)) + 'Thousand ';
        num %= 1000;
    }
    if (num > 0) {
        result += convertHundreds(num);
    }
    
    return result.trim();
}

console.log('%c🥭 Welcome to Farm to Home! 🥭', 'color: #FFD700; font-size: 20px; font-weight: bold;');

// Contact Form Handling
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formMessage = document.getElementById('formMessage');
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const message = document.getElementById('message').value;
            
            // Show loading state
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            
            try {
                // Send to backend API
                const response = await fetch('http://localhost:5001/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name,
                        email,
                        phone,
                        message
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Show success message
                    formMessage.style.display = 'block';
                    formMessage.style.background = 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)';
                    formMessage.style.color = 'white';
                    formMessage.innerHTML = `
                        <strong>✓ Message Sent Successfully!</strong><br>
                        Thank you ${name}! We've received your message and will get back to you within 24 hours at ${email}.
                    `;
                    
                    // Reset form
                    contactForm.reset();
                    
                    // Log success
                    console.log('✅ Contact form saved to database:', result);
                } else {
                    // Show error message
                    formMessage.style.display = 'block';
                    formMessage.style.background = 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)';
                    formMessage.style.color = 'white';
                    formMessage.innerHTML = `
                        <strong>✗ Error!</strong><br>
                        ${result.message || 'Failed to send message. Please try again.'}
                    `;
                }
                
                // Reset button
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                
                // Hide message after 5 seconds
                setTimeout(() => {
                    formMessage.style.display = 'none';
                }, 5000);
                
            } catch (error) {
                console.error('❌ Error submitting contact form:', error);
                
                // Show error message
                formMessage.style.display = 'block';
                formMessage.style.background = 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)';
                formMessage.style.color = 'white';
                formMessage.innerHTML = `
                    <strong>✗ Connection Error!</strong><br>
                    Cannot connect to server. Please ensure backend is running on port 5001.
                `;
                
                // Reset button
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                
                // Hide message after 5 seconds
                setTimeout(() => {
                    formMessage.style.display = 'none';
                }, 5000);
            }
        });
    }
});
