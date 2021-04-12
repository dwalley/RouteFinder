#Stock market simulation

import pylab,random

class stock():

    def __init__(self,price,distribution):
        self.price = price
        self.history = [price]
        self.distribution = distribution
        self.last_change = 0
        self.ticker = []

    def set_price(self,price):
        self.price = price
        self.history.append(price)

    def get_price(self):
        return self.price

    def get_ticker(self):
        return self.ticker

    def make_move(self,mkt_bias,mo):
        old_price = self.get_price()
        if self.get_price() > 0:
            base_move = self.distribution() + mkt_bias
            self.set_price(self.get_price()*(1+base_move))
            if mo:
                self.set_price(self.get_price()+random.gauss(.5,.5)*self.last_change)
            if self.get_price() < 0:
                self.set_price(0)
        self.history.append(self.get_price())
        self.last_change = self.get_price()- old_price

    def show_history(self,fig_num):
        
        pylab.figure(fig_num)
        pylab.plot(self.history)
        pylab.title('Closing Price: Trial '+str(fig_num))
        pylab.xlabel('Day')
        pylab.ylabel('Price')

def unit_test_stock():
    def run_sim(stks,fig,mo):
        mean = 0.0
        for s in stks:
            for d in range(num_days):
                s.make_move(bias,mo)
            s.show_history(fig)
            mean += s.get_price()
        mean = mean / float(num_stks)
        pylab.axhline(mean)

    num_stks = 20
    num_days = 100
    stks1 = []
    stks2 = []
    bias = 0.0
    mo = True
    for i in range(num_stks):
        volatility = random.uniform(0.0,0.02)
        d1 = lambda: random.uniform(-volatility,volatility)
        d2 = lambda: random.gauss(0.0,volatility/2.0)
        stks1.append(stock(100.0,d1))
        stks2.append(stock(100.0,d2))
    run_sim(stks1,1,mo)
    run_sim(stks2,2,mo)

unit_test_stock()
pylab.show()
