from random import uniform

class Portfolio:
    
    trans_lst = [] #created to store transaction history
    
    def __init__(self):
        self.cash = 0.00
        self.stock_dic = {}
        self.fund_dic = {}
    
    def addCash(self, new_cash):  # DO NOT FORGET NOT DEFINED ERRORS
        try:
            if type(new_cash)==int or type(new_cash)==float:
                if new_cash > 0:
                    self.cash += new_cash
                    self.trans_lst.append(f"${format(new_cash,'.2f')} is added to the portfolio")
                else:
                    print("Cash cannot be negative.")
            else:
                raise TypeError
        except TypeError:
            print("Please enter a number.")
        except:  # created to catch random errors 
            print("Please enter a valid cash amount.")
    
    def buyStock(self, share, stock):
        
        try:
            global stck_prc  #declared to be accessed from sellStock() method when selling the stock
            stck_prc = stock.price
            
            if type(share)==int:
                if share % int(share) != 0:
                    raise TypeError("Stock share cannot be fractional.")
                elif self.cash < share*stock.price:
                    print("Insufficient balance.")
                    return 
                else:
                    self.withdrawCash(share*stock.price)
                    self.trans_lst.append(f"${share*stock.price} is spent to buy {share} share(s) of {stock.symbol}")
                    
                    if stock.symbol in self.stock_dic:
                        self.stock_dic[stock.symbol] += share
                    else:
                        self.stock_dic[stock.symbol] = share
            else:
                print("Please enter a number for stock share.")
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
                        self.fund_dic[mf.symbol] += share
                    else:
                        self.fund_dic[mf.symbol] = share
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
                    print("Less share available than the entry.")
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
                    print("Less stock share available than the entry.")
                    return 
                else: 
                    self.trans_lst.append(f"{share} share(s) of {symbol} is sold each for ${format(p,'.2f')}")
                    self.addCash(share*p)
                    self.stock_dic[symbol] -= share
            else:
                raise TypeError("Enter a string for the first and a whole number for the second argument.")
        except KeyError:
            raise (f"{symbol} is not available in your portfolio.")
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
                raise TypeError
        except TypeError:
            print("Please enter a number.")
        except:  # created to catch random errors 
            print("Please enter a valid cash amount.")
   
    def history(self): #prints a list of all transactions
        for trans in self.trans_lst:
            print(trans)
        pass
            
    def __str__(self): #prints the portfolio
        prnt = "cash: $%s\nstocks:\n" %format(self.cash,'.2f') #Concatenate the cash balance to prnt
        for key, val in self.stock_dic.items():  
            prnt += " %d %s\n" %(val, key)  #Concatenate the stock share and ticker symbol to prnt
        prnt += "mutual funds:\n"
        for key,val in self.fund_dic.items():
            prnt += " %d %s \n" %(val, key)  #Concatenate the fund share and ticker symbol to prnt
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
                raise TypeError("Make sure to enter a string for ticker symbol")
        except:
            print("Please enter a string ticker symbol.")    
    
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




    
   