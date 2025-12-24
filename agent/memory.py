class Memory:
    def __init__(self):
        self.data={}
    def remember(self,k,v):
        self.data[k]=v
    def get(self,k):
        return self.data.get(k)
