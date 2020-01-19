DROP TABLE IF EXISTS approved_addresses;

CREATE TABLE approved_addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cashsigntype TEXT NOT NULL,
    message TEXT NOT NULL,
    sig TEXT NOT NULL,
    address TEXT  NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
