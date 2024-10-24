CREATE TABLE subscriptions (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    service_subscribed_to VARCHAR(255),
    source_url VARCHAR(255),
    form_id VARCHAR(255),
    unsubscribed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    unsubscribe_token VARCHAR(255),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);
