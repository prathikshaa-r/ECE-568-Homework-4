class Sub_Response:
    def __init__(self,trans_id,status,price,shares,time):
        self.trans_id=trans_id
        self.status=status
        self.price=price
        self.shares=shares
        self.time=time

class Response:
    def __init__(self):
        self.response=[] #the array of Sub_Response objects
