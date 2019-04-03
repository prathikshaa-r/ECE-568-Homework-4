class TransactionSubResponse:
    def __init__(self, status, shares, price, time):
        self.status = status
        self.shares = shares
        self.price = price
        self.time = time

class TransactionResponse:
    def __init__(self, trans_id, type):
        self.trans_id = trans_id
        self.type = type # query or cancel
        self.trans_resp = [] #the array of Sub_Response objects

#Response=[]
#contains Order_resp and TransactionResponse
