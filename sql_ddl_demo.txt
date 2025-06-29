CREATE TABLE Users (
    id INT PRIMARY KEY,
    user_name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

INSERT INTO Users (id, user_name, email) VALUES (1, 'Rahul', 'rahul@email.com'), (2, 'Sneha', 'sneha@email.com')
INSERT INTO Orders (order_id, user_id) VALUES (100, 1), (101, 2)  