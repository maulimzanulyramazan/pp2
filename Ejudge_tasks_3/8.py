class account():
    balance = 0
    withdrawal = 0
    def calculated(self):
        if(self.balance >= self.withdrawal):
            print(self.balance - self.withdrawal)
        else:
            print("Insufficient Funds")
cred = account()
sums = input().split()
cred.balance = int(sums[0])
cred.withdrawal = int(sums[1])
cred.calculated()