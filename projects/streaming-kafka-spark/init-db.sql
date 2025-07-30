-- This script runs inside the streaming_db database by default (set by POSTGRES_DB env)
-- Create events table
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    product VARCHAR(255) NOT NULL,
    action VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL,
    category VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    city VARCHAR(100),
    processing_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_action ON events(action);
CREATE INDEX IF NOT EXISTS idx_events_product ON events(product);
CREATE INDEX IF NOT EXISTS idx_events_category ON events(category);
CREATE INDEX IF NOT EXISTS idx_events_country ON events(country);
CREATE INDEX IF NOT EXISTS idx_events_session_id ON events(session_id);

-- Create a view for analytics
CREATE OR REPLACE VIEW events_summary AS
SELECT
    DATE(timestamp) as event_date,
    action,
    product,
    category,
    country,
    COUNT(*) as event_count,
    SUM(price * quantity) as total_revenue,
    AVG(price) as avg_price,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT session_id) as unique_sessions
FROM events
GROUP BY DATE(timestamp), action, product, category, country;

-- Create hourly analytics view
CREATE OR REPLACE VIEW events_hourly_summary AS
SELECT
    date_trunc('hour', timestamp) as hour,
    action,
    category,
    country,
    COUNT(*) as event_count,
    SUM(price * quantity) as total_revenue,
    AVG(price) as avg_price,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(DISTINCT session_id) as unique_sessions
FROM events
GROUP BY date_trunc('hour', timestamp), action, category, country;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO postgres;