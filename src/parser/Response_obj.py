class Sub_Response:
    def __init__(self,id,status,price,share,time):
        self.transaction=id
        self.status=status
        self.price=price
        self.share=share
        self.time=time

class Response:
    def __init__(self):
        self.response=[] #the array of Sub_Response objects
