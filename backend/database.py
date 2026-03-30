import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_name='farm_to_home.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Create a database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                pincode TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create orders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                order_number TEXT UNIQUE NOT NULL,
                total_amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                upi_id TEXT,
                razorpay_order_id TEXT,
                razorpay_payment_id TEXT,
                order_status TEXT DEFAULT 'pending',
                order_date TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Create order_items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                item_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        
        # Create contacts table for enquiry form
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    
    def add_customer(self, customer_data):
        """Add or update customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if customer exists by email
        cursor.execute('SELECT id FROM customers WHERE email = ?', (customer_data['email'],))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing customer
            customer_id = existing['id']
            cursor.execute('''
                UPDATE customers 
                SET name = ?, phone = ?, address = ?, city = ?, pincode = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                customer_data['name'],
                customer_data['phone'],
                customer_data['address'],
                customer_data['city'],
                customer_data['pincode'],
                customer_id
            ))
        else:
            # Insert new customer
            cursor.execute('''
                INSERT INTO customers (name, email, phone, address, city, pincode)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                customer_data['name'],
                customer_data['email'],
                customer_data['phone'],
                customer_data['address'],
                customer_data['city'],
                customer_data['pincode']
            ))
            customer_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return customer_id
    
    def add_order(self, order_data):
        """Add new order with items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Add customer first
            customer_id = self.add_customer(order_data['customer'])
            
            # Generate order number
            order_number = f"FTH{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Extract payment details
            upi_id = order_data.get('upi_id')
            razorpay_order_id = order_data.get('razorpay_order_id')
            razorpay_payment_id = order_data.get('razorpay_payment_id')
            
            # Insert order with 'placed' status
            cursor.execute('''
                INSERT INTO orders (customer_id, order_number, total_amount, payment_method, upi_id, razorpay_order_id, razorpay_payment_id, order_status, order_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer_id,
                order_number,
                order_data['total'],
                order_data['payment'],
                upi_id,
                razorpay_order_id,
                razorpay_payment_id,
                'placed',
                order_data['orderDate']
            ))
            order_id = cursor.lastrowid
            
            # Insert order items
            for item in order_data['items']:
                subtotal = item['price'] * item['quantity']
                cursor.execute('''
                    INSERT INTO order_items (order_id, item_name, item_type, quantity, price, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    order_id,
                    item['name'],
                    item.get('type', 'mango'),
                    item['quantity'],
                    item['price'],
                    subtotal
                ))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'order_id': order_id,
                'order_number': order_number,
                'customer_id': customer_id
            }
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_all_orders(self, limit=100):
        """Get all orders with customer details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                o.id, o.order_number, o.total_amount, o.payment_method, 
                o.upi_id, o.razorpay_order_id, o.razorpay_payment_id,
                o.order_status, o.order_date, o.created_at,
                c.name as customer_name, c.email as customer_email, 
                c.phone as customer_phone, c.address, c.city, c.pincode
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.created_at DESC
            LIMIT ?
        ''', (limit,))
        
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return orders
    
    def get_order_details(self, order_id):
        """Get complete order details including items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get order and customer info
        cursor.execute('''
            SELECT 
                o.*, 
                c.name as customer_name, c.email as customer_email, 
                c.phone as customer_phone, c.address, c.city, c.pincode
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.id = ?
        ''', (order_id,))
        
        order = cursor.fetchone()
        if not order:
            conn.close()
            return None
        
        order_dict = dict(order)
        
        # Get order items
        cursor.execute('''
            SELECT * FROM order_items WHERE order_id = ?
        ''', (order_id,))
        
        order_dict['items'] = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return order_dict
    
    def get_customer_orders(self, customer_email):
        """Get all orders for a specific customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT o.* FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE c.email = ?
            ORDER BY o.created_at DESC
        ''', (customer_email,))
        
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return orders
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE orders SET order_status = ? WHERE id = ?
        ''', (status, order_id))
        
        conn.commit()
        conn.close()
        return True
    
    def add_contact(self, contact_data):
        """Add new contact form submission"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO contacts (name, email, phone, message, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                contact_data['name'],
                contact_data['email'],
                contact_data.get('phone', ''),
                contact_data['message'],
                'new',
                datetime.now().isoformat()
            ))
            
            contact_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'contact_id': contact_id
            }
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_all_contacts(self, limit=100):
        """Get all contact form submissions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM contacts
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        contacts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return contacts
    
    def update_contact_status(self, contact_id, status):
        """Update contact status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE contacts SET status = ? WHERE id = ?
        ''', (status, contact_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_statistics(self):
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total customers
        cursor.execute('SELECT COUNT(*) as count FROM customers')
        total_customers = cursor.fetchone()['count']
        
        # Total orders
        cursor.execute('SELECT COUNT(*) as count FROM orders')
        total_orders = cursor.fetchone()['count']
        
        # Total revenue
        cursor.execute('SELECT SUM(total_amount) as revenue FROM orders')
        total_revenue = cursor.fetchone()['revenue'] or 0
        
        # Total contacts
        cursor.execute('SELECT COUNT(*) as count FROM contacts')
        total_contacts = cursor.fetchone()['count']
        
        # Orders by status
        cursor.execute('''
            SELECT order_status, COUNT(*) as count 
            FROM orders 
            GROUP BY order_status
        ''')
        orders_by_status = {row['order_status']: row['count'] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_customers': total_customers,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_contacts': total_contacts,
            'orders_by_status': orders_by_status
        }
