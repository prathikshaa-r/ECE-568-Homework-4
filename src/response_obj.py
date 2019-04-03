class TransactionSubResponse:
    def __init__(self, status, shares, price, time):
        self.status = status
        self.shares = shares
        self.price = price
        self.time = time
        pass

    # print Transaction Sub Response
    def __repr__(self):
        print('Status: ' + self.status)
        print('Amount of shares: ', self.shares)
        print('Price: ', self.price)
        print('Time: ', self.time)
        return ''

class TransactionResponse:
    def __init__(self, trans_id, type):
        self.trans_id = trans_id
        self.type = type # query or cancel
        self.trans_resp = [] #the array of Sub_Response objects
        self.success = True
        self.err = ""
        
#Response=[]
#contains Order_resp and TransactionResponse
