CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, cash NUMERIC NOT NULL DEFAULT 10000.00);
CREATE TABLE sqlite_sequence(name,seq);
CREATE UNIQUE INDEX username ON users (username);
CREATE TABLE portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        FOREIGN KEY (userid) REFERENCES users (id)
    );
CREATE TABLE history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userid INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        method TEXT NOT NULL,
        price NUMERIC NOT NULL,
        transacted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (userid) REFERENCES users (id)
    );
CREATE TABLE orders (id INTEGER, user_id NUMERIC NOT NULL, symbol TEXT NOT NULL, shares NUMERIC NOT NULL, price NUMERIC NOT NULL, timestamp TEXT, PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id));
CREATE INDEX orders_by_user_id_index ON orders (user_id);
