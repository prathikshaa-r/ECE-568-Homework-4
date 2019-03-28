/* create an account */
INSERT INTO Accounts
(account_id, balance)
VALUES (%s, %s)
	/* VALUES */
(account_id, balance)

/* create a position */
SELECT COUNT(*) FROM positions WHERE symbol ='aa' AND account_id=12;
/* if above result is == 0, insert, else update */

INSERT INTO positions (symbol, amount, account_id) VALUES ('aa', 123.33, 12)

UPDATE positions SET amount=amount+139.22 WHERE symbol ='aa' AND account_id = 12;

/* creatre orders */
/*todo: deduct money from account */

INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id)
VALUES (5, 'aa', -200, 140, 12);

INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id)
VALUES (2, 'aa', -100, 130, 12);

INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id)
VALUES (4, 'aa', -500, 128, 12);

INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id)
VALUES (3, 'aa', 200, 127, 12);

INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id)
VALUES (1, 'aa', 300, 125, 12);

INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id)
VALUES (6, 'aa', 400, 125, 12);


/* Query Status of order */
SELECT * FROM Orders WHERE trans_id=10;

/* Cancel */
UPDATE Orders SET Status='cancelled' WHERE trans_id=5


/* Order matching */

/* Select the head of buy priority queue -- maybe multiple rows, need to break ties */
SELECT * FROM Orders WHERE limit_price = (SELECT max(limit_price) FROM Orders WHERE amount>0);

SELECT * FROM Orders
WHERE limit_price = (SELECT min(limit_price) FROM Orders WHERE amount<0);

/* Executed */
/* executed in part 
	one insert
	one update
*/
/* update buyer */
INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id, status)
VALUES (trans_id, symbol, amount_bought, limit_price, account_id, 'executed')

UPDATE Orders SET amount = amount - amount_bought WHERE trans_id=(%s)

/* update seller */
INSERT INTO Orders (trans_id, symbol, amount, limit_price, account_id, status)
VALUES (trans_id, symbol, amount_bought, limit_price, account_id, 'executed')

UPDATE Orders SET amount = amount - amount_bought WHERE trans_id=(%s)


/* executed fully 
	one update
*/
UPDATE Orders SET status='executed' WHERE trans_id=(%s)
