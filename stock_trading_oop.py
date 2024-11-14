class StockMarket:
    def __init__(self, file_path):
        #######################  START CODE HERE  ######################

        self.current_day=0
        self.price_history={'AAPL':[], 'GOOGL':[]}
        self.file_path=file_path

        #######################  END CODE HERE  ########################

    def read_market_data(self, file_path):
        market_data = []
        #######################  START CODE HERE  ######################

        file=open(file_path, 'r')
        while True:
            line=file.readline()
            if not line:
                break
            date, AAPL, GOOGL=line.split(sep=',')
            AAPL=float(AAPL)
            GOOGL=float(GOOGL)
            market_data.append({'date': date, 'AAPL': float(round(AAPL, 2)), 'GOOGL': float(round(GOOGL,2))})

        #######################  END CODE HERE  ########################

        return market_data

    def update_price(self):
        #######################  START CODE HERE  ######################

        market_data=self.read_market_data(self.file_path)
        if self.current_day>=len(market_data):
            return None
        else:

            current_price=market_data[self.current_day]
            self.price_history['AAPL'].append(current_price['AAPL'])
            self.price_history['GOOGL'].append(current_price['GOOGL'])
            if len(self.price_history['AAPL']) > 5:  # 길이가 5보다 긴 경우에 과거 데이터는 제거
                self.price_history['AAPL'] = self.price_history['AAPL'][1:]
                self.price_history['GOOGL'] = self.price_history['GOOGL'][1:]
            self.current_day += 1
            return current_price

        #######################  END CODE HERE  ########################


class Portfolio:
    def __init__(self, initial_cash):
        #######################  START CODE HERE  ######################

        self.cash=initial_cash
        self.holdings={'AAPL':0, 'GOOGL':0}

        #######################  END CODE HERE  ########################

    def buy(self, stock, price, quantity):
        #######################  START CODE HERE  ######################

        # 잔고가 충분한 경우
        if self.cash >= price * quantity:
            self.cash -= price * quantity
            self.holdings[stock] += quantity
            if quantity>0:
              print('Bought %d shares of %s at $%.2f' % (quantity, stock, price))
        # 잔고가 충분하지 않은 경우
        else:
            print('매수에 실패하였습니다.')

        #######################  END CODE HERE  ########################

    def sell(self, stock, price, quantity):
        #######################  START CODE HERE  ######################

        if self.holdings[stock] >= quantity:
            self.cash += price * quantity
            self.holdings[stock] -= quantity
            if quantity>0:
              print('Sold %d shares of %s at $%.2f' % (quantity, stock, price))

        else:
            print('매도에 실패하였습니다.')

        #######################  END CODE HERE  ########################

    def calculate_value(self, current_price):
        #######################  START CODE HERE  ######################

        value = float(self.cash + self.holdings['AAPL'] * current_price['AAPL'] + self.holdings['GOOGL'] *current_price['GOOGL'])
        return value

        #######################  END CODE HERE  ########################


class TradingStrategy:
    def __init__(self, buy_threshold, sell_threshold, max_buy_quantity, max_sell_quantity):
        #######################  START CODE HERE  ######################

        self.buy_threshold=buy_threshold
        self.sell_threshold=sell_threshold
        self.max_buy_quantity=max_buy_quantity
        self.max_sell_quantity=max_sell_quantity

        #######################  END CODE HERE  ########################

    def apply_strategy(self, portfolio, stock, current_price, price_history):
        #######################  START CODE HERE  ######################

        if len(price_history[stock]) < 5:  # 과거 5일치의 데이터가 없는 경우

            return  # 코드 중단

        five_day_mean_price = sum(price_history[stock]) / len(price_history[stock])  # aapl의 5일간 평균 가격

        # 전략 수행
        if self.buy_threshold * five_day_mean_price > current_price[stock]:  # stock을 매수해야 하는 경우

            maxbuy = portfolio.cash // current_price[stock]  # 매수 가능 수량
            buy_quantity = min(maxbuy, self.max_buy_quantity)  # 매수 수량 결정
            portfolio.buy(stock, current_price[stock], buy_quantity)

        elif self.sell_threshold * five_day_mean_price < current_price[stock]:  # stock 매도해야 하는 경우

            maxsell = portfolio.holdings['AAPL']
            sell_quantity = min(maxsell, self.max_sell_quantity)
            portfolio.sell(stock, current_price[stock], sell_quantity)

        #######################  END CODE HERE  ########################


class User:
    def __init__(self, name, initial_cash, strategy):
        #######################  START CODE HERE  ######################

        self.name=name
        self.portfolio=Portfolio(initial_cash)
        self.strategy=strategy

        #######################  END CODE HERE  ########################

    def run_strategy(self, current_price, price_history):
        #######################  START CODE HERE  ######################

        print('User %s:'%self.name)
        #buy threshold와 sell threshold 값의 범위에 대한 예외 처리
        if self.strategy.buy_threshold>=1:
          raise Exception('buy_threshold는 1보다 작아야 합니다')
        elif self.strategy.sell_threshold<=1:
          raise Exception('sell_threshold는 1보다 커야 합니다')

        self.strategy.apply_strategy(self.portfolio, 'AAPL', current_price, price_history) #AAPL에 대해 전략 적용
        self.strategy.apply_strategy(self.portfolio, 'GOOGL', current_price, price_history) #GOOGL에 대해 전략 적용

        #######################  END CODE HERE  ########################

    def calculate_portfolio_value(self, current_price):
        #######################  START CODE HERE  ######################

        portfolio_value=self.portfolio.calculate_value(current_price)
        return portfolio_value

        #######################  END CODE HERE  ########################


class Simulation:
    def __init__(self, users, market):
        #######################  START CODE HERE  ######################

        self.users=users
        self.market=market

        #######################  END CODE HERE  ########################

    def run(self):
        #######################  START CODE HERE  ######################

        for data in market.read_market_data(market.file_path):

            import copy
            price_history=copy.deepcopy(self.market.price_history) #price history를 먼저 받아온다

            current_price=self.market.update_price() #current price를 받아오고 업데이트 한다

            print('Date:',data['date']) #거래일 추력
            for user in self.users: #각 유저에 대해 전략 수행
                user.run_strategy(current_price, price_history)
                print('Portfolio value = %.2f, Cash= %.2f, Holdings: AAPL = %d shares, GOOGL = %d shares'%(user.calculate_portfolio_value(current_price), user.portfolio.cash, user.portfolio.holdings['AAPL'], user.portfolio.holdings['GOOGL']))

            print() #한줄 띄워주기

        print('Final Results:') #최종 포트폴리오 가치 비교
        for user in self.users:
          print('user %s: Final Portfolio Value = $%.2f'%(user.name, user.calculate_portfolio_value(current_price)))
        #######################  END CODE HERE  ########################



## 실행 예시
## - 뼈대 코드를 지우지 말 것
## - 다른 설정으로 다양하게 테스트 해보는 것은 좋으나, 테스트 유저는 주석 처리하여 제출할 것

# 사용자 정의
user1 = User("Alice", 10000, TradingStrategy(buy_threshold=0.95, sell_threshold=1.05, max_buy_quantity=10, max_sell_quantity=5))
user2 = User("Bob", 10000, TradingStrategy(buy_threshold=0.97, sell_threshold=1.07, max_buy_quantity=15, max_sell_quantity=7))
user3 = User("Charlie", 10000, TradingStrategy(buy_threshold=0.95, sell_threshold=1.10, max_buy_quantity=5, max_sell_quantity=3))

# 주식 시장 및 시뮬레이션 실행
market = StockMarket('stock_data.txt')
simulation = Simulation([user1, user2, user3], market)
simulation.run()