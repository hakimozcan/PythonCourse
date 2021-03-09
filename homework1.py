from random import uniform

class Portfolio:
    
    trans_lst = [] #created to store transaction history
    
    def __init__(self):
        self.cash = 0.00
        self.stock_dic = {} #created to store stock symbol(key) and share(val) 
        self.fund_dic = {}  #created to store mutual fund symbol(key) and share(val)
    
    def addCash(self, new_cash):
        try:
            if type(new_cash)==int or type(new_cash)==float:
                if new_cash > 0:
                    self.cash += new_cash
                    self.trans_lst.append(f"${format(new_cash,'.2f')} is added to the portfolio")
                else:
                    print("Cash cannot be negative.")
            else:
                print("Please enter a number.") 
        except:  # created to catch random errors 
            print("Please enter a valid cash amount.")
    
    def buyStock(self, share, stock):
        try:
            global stck_prc  #declared to be accessed from sellStock() method when selling the stock
            stck_prc = stock.price
            
            if type(share)==int:
                if self.cash < share*stock.price:
                    print("Insufficient balance.")
                    return 
                else:
                    self.withdrawCash(share*stock.price)
                    self.trans_lst.append(f"${share*stock.price} is spent to buy {share} share(s) of {stock.symbol}")
                    if stock.symbol in self.stock_dic: 
                        self.stock_dic[stock.symbol] += share #sums up the share with the previous share
                    else:
                        self.stock_dic[stock.symbol] = share #creates a new symbol(key) and share(val) pair
            else:
                print("Please enter a whole number for stock share.")
        except AttributeError:
            print("Please enter a valid input for stock.")
        except: 
            print("Please enter valid inputs")
            
    def buyMutualFund(self, share, mf): 
        try:
            if type(share)==float or type(share)==int: # Buys 2 shares of "GHT"
                if self.cash < share:
                    print("Insufficient balance")
                    return
                else:
                    self.withdrawCash(share)
                    self.trans_lst.append(f"${share} is spent to buy {share} share(s) of {mf.symbol}")
                    if mf.symbol in self.fund_dic:
                        self.fund_dic[mf.symbol] += share #sums up the share with the previous share
                    else:
                        self.fund_dic[mf.symbol] = share  #creates a new symbol(key) and share(val) pair
            else:
                print("Please enter a number for share.")
        except AttributeError:
            print("Please enter a valid input for mutual fund.")
        except:
            print("Please enter valid inputs.")
            
    def sellMutualFund(self, symbol, share):
        try:
            if type(symbol)==str and type(share)==int or type(share)==float:  # Buys 2 shares of "GHT"
                p = uniform(0.9, 1.2) #generated to get a selling price for funds
                if self.fund_dic[symbol] < share:
                    print("Insufficient share in the portfolio.")
                    return
                else:
                    self.trans_lst.append(f"{share} share(s) of {symbol} is sold each for ${format(p,'.2f')}")
                    self.addCash(share*p)
                    self.fund_dic[symbol] -= share
            else:
                print("Please enter a string for symbol and a number for share.")
        except KeyError:
            print(f"{symbol} is not available in your portfolio.")
        except:
            print("Please enter a valid ticker symbol and share.")
      
    def sellStock(self, symbol, share):  
        try:
            if type(symbol)==str and type(share)==int:
                p = uniform(0.5*stck_prc, 1.5*stck_prc) #generated to get a selling price for stocks
                
                if self.stock_dic[symbol] < share:
                    print("Insufficient stock share in the portfolio.")
                    return 
                else: 
                    self.trans_lst.append(f"{share} share(s) of {symbol} is sold each for ${format(p,'.2f')}")
                    self.addCash(share*p)
                    self.stock_dic[symbol] -= share
            else:
                print("Please enter a string for symbol and a number for share.")
        except KeyError:
            print(f"{symbol} is not available in your portfolio.")
        except:
            print("Please enter valid inputs.")
    
    def withdrawCash(self, new_cash): 
        try:    
            if type(new_cash)==int or type(new_cash)==float:
                if new_cash > self.cash: 
                    print("Insufficient balance")
                    return
                elif new_cash < 0:
                    print("Cash cannot be negative!")
                    return 
                else: 
                    self.cash -= new_cash
                    self.trans_lst.append(f"${new_cash} is withdrawn from the portfolio")
            else:
                print("Please enter a number.")
        except:  # created to catch random errors 
            print("Please enter a valid cash amount.")
   
    def history(self): #prints a list of all transactions
        for trans in self.trans_lst:
            print(trans)
        pass
            
    def __str__(self): #prints the portfolio
        prnt = "cash: $%s\nstocks:\n" %format(self.cash,'.2f') #Concatenates the cash balance to prnt
        for key, val in self.stock_dic.items():  
            prnt += " %d %s\n" %(val, key)  #Concatenates the stock share and ticker symbol to prnt
        prnt += "mutual funds:\n"
        for key,val in self.fund_dic.items():
            prnt += " %d %s \n" %(val, key)  #Concatenates the fund share and ticker symbol to prnt
        return prnt
            
class Stock: 
    def __init__(self, price, symbol):
        try:
            if type(price)==int and type(symbol)==str:
                self.price = price
                self.symbol = symbol
            else:
               print("Enter a number for price and string for ticker symbol")
        except:
            print("Please enter a valid price and ticker symbol.")
            
class MutualFund:   
    def __init__(self, symbol):
        try:
            if type(symbol)==str:
                self.symbol = symbol
            else:
                print("Please enter a string for ticker symbol")
        except: #created to catch potential random erros
            print("Please enter a valid ticker symbol.")   
    




    
   