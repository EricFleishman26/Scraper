class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.eps = 0
        self.growth = 0
        self.pe_ratio = 0
        self.fair_val = 0
        self.min_return = 0.15
        self.moving50 = 0
        self.moving200 = 0
