# Exchange Server
Go to erss-hwk4-pr109-yz476 folder and run 'sudo docker-compose up' to deploy the server.

Under erss-hwk4-pr109-yz476 folder, go to test folder, you can run 'sh test.sh' to test the functionality of the server.
This test will send a sequence of requests and then recieve corresponding responses.
The sent requests are listed below (following these sequence), and you can check the reponses to see if they are resonable.
Before you execute this script, you need to open client.py and go to line 183 to change the address to be the server's address.

## Scalability Tests
Another test program is scalability_test.py. It can send many random requests. You can run it with one argument with specify the number of request that this prgram will send, e.g. ' python3 scalability_test.py 1000'. Also, before executing this program, please go to line 56 to change the address to be the server's address.
The scalability_test function will produce 6 numbers, each represents the number of requests whose latency lies in the corresponding gap.
The first number corresonds to the latency from 0 to 10 ms, and the second corresonds to the latency from 10 to 20 ms ... The last number is the number of requests whose latency is larger than 50 ms. 
After this 6 numbers, another line will tell you the total excution time of this program, in ms.

<?xml version="1.0" ?>
<create>
  <account balance="1000000" id="123456"/>
  <account balance="1000000" id="234567"/>
  <account balance="1000000" id="01234"/>
  <symbol sym="Test1">
    <account id="123456">100000</account>
  </symbol>
  <symbol sym="Test3">
    <account id="123456">100000</account>
  </symbol>
  <symbol sym="Test2">
    <account id="234567">100000</account>
  </symbol>
  <symbol sym="Test2">
    <account id="01234">100000</account>
  </symbol>
  <account balance="1000000" id="123456"/>
  <symbol sym="Test2">
    <account id="98765">100000</account>
  </symbol>
</create>

<?xml version="1.0" ?>
<transactions id="01234">
  <order amount="-250" limit="100" sym="Test2"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="234567">
  <order amount="-400" limit="100" sym="Test2"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="123456">
  <order amount="400" limit="150" sym="Test2"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="123456">
  <order amount="5000" limit="1000" sym="Test2"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="98765">
  <order amount="5000" limit="1000" sym="Test2"/>
  <query id="2"/>
  <cancel id="3"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="01234">
  <query id="1"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="123456">
  <query id="3"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="234567">
  <query id="2"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="234567">
  <cancel id="2"/>
</transactions>

<?xml version="1.0" ?>
<transactions id="234567">
  <query id="2"/>
</transactions>