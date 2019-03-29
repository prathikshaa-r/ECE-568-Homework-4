class Order_resp:
    def __init__(self,order,open,msg,id):
        self.sym = order.sym
        self.amount = order.amount
        self.limit = order.limit
        self.type ="order"
        self.open = open #boolean
        self.msg = msg
        self.id = id  # the order id to be determined by the server when this order is deployed

class TransactionSubResponse:
    def __init__(self,status,price,shares,time):
        self.status=status
        self.price=price
        self.shares=shares
        self.time=time

class TransactionResponse:
    def __init__(self,trans_id,request):
        self.trans_id=trans_id
        self.type="transac"
        self.request=request # query or cancel
        self.trans_resp=[] #the array of Sub_Response objects



#Response=[]
#contains Order_resp and TransactionResponse