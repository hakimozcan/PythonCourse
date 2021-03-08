
from random import uniform

class Portfolio:
    
    trans_lst = [] #created to store transaction history
    
    def __init__(self):
        self.cash = 0.00
        self.stock_dic = {}
        self.fund_dic = {}
    
    def addCash(self, new_cash):
        try:
            if new_cash > 0:
                self.cash += new_cash
                self.trans_lst.append(f"${format(new_cash,'.2f')} is added to the portfolio")
            else:
                print("Cash cannot be negative.")
        except: # created to catch random errors like string inputs
            print("Please, enter a valid cash amount.")
    
    def buyStock(self, share, stock):
        global stck_prc  #declared to be accessed from sellStock() method when selling the stock
        stck_prc = stock.price
        
        try:
            if share % int(share) != 0:
                print("Stock share cannot be fractional.")
                return 
            elif self.cash < share*stock.price:
                print("Insufficient balance")
            else:
                self.withdrawCash(share*stock.price)
                self.trans_lst.append(f"${share*stock.price} is spent to buy {share} share(s) of {stock.symbol}")
                
                if stock.symbol in self.stock_dic:
                    self.stock_dic[stock.symbol] += share
                else:
                    self.stock_dic[stock.symbol] = share
        except:
            print("Please, enter valid inputs.")

    def buyMutualFund(self, share, mf):
        try:
            if self.cash < share:
                print("Insufficient balance")
                return
            else:
                self.withdrawCash(share)
                self.trans_lst.append(f"${share} is spent to buy {share} share(s) of {mf.symbol}")
                
                if mf.symbol in self.fund_dic:
                    self.fund_dic[mf.symbol] += share
                else:
                    self.fund_dic[mf.symbol] = share
        except:
            print("Please, enter valid inputs.")
            
    def sellMutualFund(self, symbol, share):
        try:
            p = uniform(0.9, 1.2) #generated to get a selling price for funds
            if self.fund_dic[symbol] < share:
                print("Less share available than the entry.")
                return
            else:
                self.trans_lst.append(f"{share} share(s) of {symbol} is sold each for ${format(p,'.2f')}")
                self.addCash(share*p)
                self.fund_dic[symbol] -= share
        except:
            print("Please, enter valid inputs.")
           
    def sellStock(self, symbol, share):  
        try:
            p = uniform(0.5*stck_prc, 1.5*stck_prc) #generated to get a selling price for stocks
            if share % int(share) != 0:
                print("Stock share cannot be fractional.")
                return
            elif self.stock_dic[symbol] < share:
                print("Less stock share available than the entry.")
                return 
            else: 
                self.trans_lst.append(f"{share} share(s) of {symbol} is sold each for ${format(p,'.2f')}")
                self.addCash(share*p)
                self.stock_dic[symbol] -= share
                
        except:
            print("Please, enter valid inputs.")
    
    def withdrawCash(self, new_cash): 
        try:    
            if new_cash > self.cash: 
                print("Insufficient balance")
                return
            elif new_cash < 0:
                print("Cash cannot be negative!")
            else: 
                self.cash -= new_cash
                self.trans_lst.append(f"${new_cash} is withdrawn from the portfolio")
        except:
            print("Please, enter valid inputs.")
   
    def history(self): #prints a list of all transactions
        for trans in self.trans_lst:
            print(trans)
        pass
            
    def __str__(self): #prints the portfolio
        prnt = "cash: $%s\nstock:" %format(self.cash,'.2f') #Concatenate the cash balance to prnt
        for key, val in self.stock_dic.items():  
            prnt += "%d %s \t  \n" %(val, key)  #Concatenate the stock share and ticker symbol to prnt
        prnt += "mutual funds:"
        for key,val in self.fund_dic.items():
            prnt += "%d %s \n\t\t\t  " %(val, key)  #Concatenate the fund share and ticker symbol to prnt
        
        return prnt
            
class Stock: 
    def __init__(self, price, symbol):
        self.price = price
        self.symbol = symbol

class MutualFund:   
    def __init__(self, symbol):
        self.symbol = symbol
    
        
    
portfolio = Portfolio()
portfolio.addCash(300.50) #Adds cash to the portfolio
s = Stock(20, "HFH") #Create Stock with price 20 and symbol "HFH"
portfolio.buyStock(5, s) #Buys 5 shares of stock s


mf1 = MutualFund("BRT") #Create MF with symbol "BRT"
mf2 = MutualFund("GHT") #Create MF with symbol "GHT"
portfolio.buyMutualFund(10.3, mf1) #Buys 10.3 shares of "BRT"
portfolio.buyMutualFund(2, mf2) #Buys 2 shares of "GHT"


print(portfolio) #Prints portfolio  #cash: $140.50  #stock: 5 HFH  #mutual funds: 10.33 BRT # 2 GHT


portfolio.sellMutualFund("BRT", 3) #Sells 3 shares of BRT
portfolio.sellStock("HFH", 1) #Sells 1 share of HFH
portfolio.withdrawCash(50) #Removes $50
portfolio.history() #Prints a list of all transactions  #ordered by time



    
   