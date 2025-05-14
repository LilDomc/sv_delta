import db

def setup_db():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rate (
            rateID SERIAL PRIMARY KEY,
            productID INT NOT NULL,
            "5_star" INT,
            "4_star" INT,
            "3_star" INT,
            "2_star" INT,
            "1_star" INT,
            average_rating DECIMAL(3,2),
            FOREIGN KEY (productID) REFERENCES products(productID)
        );
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    return True