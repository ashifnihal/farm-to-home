# PostgreSQL Setup Guide for Farm to Home

This guide will help you set up PostgreSQL for the Farm to Home application.

## Prerequisites

- PostgreSQL installed on your system
- Python environment with required packages

## Installation

### 1. Install PostgreSQL

#### macOS (using Homebrew):
```bash
brew install postgresql@15
brew services start postgresql@15
```

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Windows:
Download and install from: https://www.postgresql.org/download/windows/

### 2. Create Database and User

```bash
# Access PostgreSQL
psql postgres

# Create database
CREATE DATABASE farm_to_home;

# Create user (optional, or use default postgres user)
CREATE USER farm_admin WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE farm_to_home TO farm_admin;

# Exit
\q
```

### 3. Configure Environment Variables

Create or update your `.env` file in the `backend` directory:

```env
# Database Configuration
DATABASE_TYPE=postgres

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=farm_to_home
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password

# ... other configurations (Mailgun, Razorpay, etc.)
```

### 4. Install Python Dependencies

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install psycopg2-binary==2.9.9
```

### 5. Run the Application

```bash
python app.py
```

The application will automatically:
- Detect that you're using PostgreSQL
- Create all necessary tables
- Start the Flask server

## Switching Between SQLite and PostgreSQL

You can easily switch between databases by changing the `DATABASE_TYPE` in your `.env` file:

### Use SQLite (default):
```env
DATABASE_TYPE=sqlite
```

### Use PostgreSQL:
```env
DATABASE_TYPE=postgres
```

## Migrating Data from SQLite to PostgreSQL

If you have existing data in SQLite and want to migrate to PostgreSQL:

### Option 1: Manual Export/Import

1. Export data from SQLite:
```bash
sqlite3 farm_to_home.db .dump > backup.sql
```

2. Modify the SQL file to be PostgreSQL compatible (change syntax if needed)

3. Import to PostgreSQL:
```bash
psql -U postgres -d farm_to_home -f backup.sql
```

### Option 2: Use Python Script

Create a migration script that:
1. Connects to both databases
2. Reads data from SQLite
3. Inserts into PostgreSQL

Example:
```python
from database import Database as SQLiteDB
from database_postgres import DatabasePostgres as PostgresDB

# Initialize both databases
sqlite_db = SQLiteDB()
postgres_db = PostgresDB()

# Get all orders from SQLite
orders = sqlite_db.get_all_orders(limit=1000)

# Insert into PostgreSQL
for order in orders:
    # Process and insert each order
    pass
```

## Verifying the Setup

1. Check if PostgreSQL is running:
```bash
psql -U postgres -d farm_to_home -c "SELECT version();"
```

2. Check tables:
```bash
psql -U postgres -d farm_to_home -c "\dt"
```

3. Test the API:
```bash
curl http://localhost:5001/api/statistics
```

## Troubleshooting

### Connection Refused
- Ensure PostgreSQL is running: `brew services list` (macOS) or `sudo systemctl status postgresql` (Linux)
- Check if the port is correct (default: 5432)
- Verify credentials in `.env` file

### Authentication Failed
- Check username and password in `.env`
- Ensure the user has proper permissions
- Try using the default `postgres` user

### Tables Not Created
- Check the application logs for errors
- Manually create tables using the SQL in `database_postgres.py`
- Ensure the user has CREATE TABLE permissions

## Performance Tips

1. **Indexes**: Add indexes for frequently queried columns:
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_customers_email ON customers(email);
```

2. **Connection Pooling**: For production, consider using connection pooling with `psycopg2.pool`

3. **Backup**: Set up regular backups:
```bash
pg_dump -U postgres farm_to_home > backup_$(date +%Y%m%d).sql
```

## Production Deployment

For production environments:

1. Use environment-specific credentials
2. Enable SSL connections
3. Set up regular backups
4. Monitor database performance
5. Use connection pooling
6. Consider using managed PostgreSQL services (AWS RDS, Google Cloud SQL, etc.)

## Support

For issues or questions:
- Check PostgreSQL logs: `/usr/local/var/log/postgresql@15.log` (macOS)
- Review application logs
- Consult PostgreSQL documentation: https://www.postgresql.org/docs/