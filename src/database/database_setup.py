#!/usr/bin/python3
import psycopg2

database='exchange_matching'
conn = psycopg2.connect(database='exchange_matching', user='postgres', password='passw0rd', host='0.0.0.0', port='5432')

print("Opened database %s successfully" % database)
cur = conn.cursor()
cur.execute('''CREATE TABLE Accounts (
account_id int PRIMARY KEY,
balance real NOT NULL
);''')

cur.commit()

cur.execute('''CREATE TABLE Positions (
position_id SERIAL PRIMARY KEY,
symbol varchar(10) NOT NULL,
amount real NOT NULL, /* positive real number */
account_id int NOT NULL,
FOREIGN KEY(account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);''')
cur.commit()


cur.execute('''CREATE TYPE order_status AS ENUM ('open', 'cancelled','executed');
CREATE TABLE Orders (
order_id SERIAL PRIMARY KEY,
trans_id int NOT NULL,
symbol varchar(10) NOT NULL,
amount real NOT NULL, /* +ve or -ve real number -ve=>sell */
limit_price real NOT NULL, /* positive real number */
account_id int NOT NULL,
status order_status NOT NULL DEFAULT 'open',
/* need to add time */
FOREIGN KEY(account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE /* ideally on delete set status to cancelled */
);''')


print ("Table created successfully")

conn.commit()
conn.close()
