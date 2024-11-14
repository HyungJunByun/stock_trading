from debugpy.common.timestamp import current


def initialize_portfolio(initial_cash):
    return {'cash': initial_cash, 'holdings': {'AAPL': 0, 'GOOGL': 0}}

def read_market_data(file_name):
    market_data = []
    #######################  START CODE HERE  ######################
    #파일 읽기 및 리스트에 저장
    f=open(file_name, 'r')
    while True:
        line=f.readline()
        if not line:
            break
        date, AAPL, GOOGL=line.split(sep=',')
        #가격 데이터 실수 자료형으로 변환
        AAPL=float(AAPL)
        GOOGL=float(GOOGL)
        market_data.append({'date':date, 'AAPL':float(round(AAPL,2)), 'GOOGL':float(round(GOOGL,2))})
    #######################  END CODE HERE  ########################
    return market_data

def buy_stock(portfolio, stock, price, quantity):
    #######################  START CODE HERE  ######################

    #잔고가 충분한 경우
    if portfolio['cash']>=price*quantity:
        portfolio['cash']-=price*quantity
        portfolio['holdings'][stock]+=quantity

        return portfolio, 'Bought %d shares of %s at $%d'%(quantity, stock, price)
    #잔고가 충분하지 않은 경우
    else:
        return portfolio, '매수에 실패하였습니다.'

    #######################  END CODE HERE  ########################

def sell_stock(portfolio, stock, price, quantity):
    #######################  START CODE HERE  ######################

    if portfolio['holdings'][stock]>=quantity:
        portfolio['cash']+=price*quantity
        portfolio['holdings'][stock]-=quantity

        return portfolio, 'Sold %d shares of %s at $%d'%(quantity, stock, price)

    else:
        return portfolio, '매도에 실패하였습니다.'

    #######################  END CODE HERE  ########################

def calculate_portfolio_value(portfolio, current_price):
    #######################  START CODE HERE  ######################

    value=float(portfolio['cash']+portfolio['holdings']['AAPL']*current_price['AAPL']+portfolio['holdings']['GOOGL']*current_price['GOOGL'])
    return value

    #######################  END CODE HERE  ########################

def apply_trading_strategy(user, current_price, price_history):
    #######################  START CODE HERE  ######################

    if len(price_history['AAPL'])<5: #과거 5일치의 데이터가 없는 경우
        return user['portfolio'] #코드 중단

    aapl_5day_mean_price=sum(price_history['AAPL'])/len(price_history['AAPL']) #aapl의 5일간 평균 가격
    googl_5day_mean_price=sum(price_history['GOOGL'])/len(price_history['GOOGL']) #googl의 5일간 평균 가격

    #AAPL
    if user['buy_threshold']*aapl_5day_mean_price>current_price['AAPL']: #AAPL 매수해야 하는 경우
        maxbuy=user['portfolio']['cash']//current_price['AAPL'] #매수 가능 수량
        buy_quantity=min(maxbuy, user['max_buy_quantity']) #매수 수량 결정
        user['portfolio'], message=buy_stock(user['portfolio'], 'AAPL', current_price['AAPL'], buy_quantity) #매수 실행
        if buy_quantity>0: #매수 수량이 1개 이상인 경우에만 메시지 출력
            print(message)
    elif user['sell_threshold']*aapl_5day_mean_price<current_price['AAPL']: #AAPL 매도해야 하는 경우
        maxsell=user['portfolio']['holdings']['AAPL']
        sell_quantity=min(maxsell, user['max_sell_quantity'])
        user['portfolio'], message=sell_stock(user['portfolio'], 'AAPL', current_price['AAPL'], sell_quantity)
        if sell_quantity>0:
            print(message)

    #GOOGL
    if current_price['GOOGL']<user['buy_threshold']*googl_5day_mean_price: #GOOGL 매수해야 하는 경우
        maxbuy=user['portfolio']['cash']//current_price['GOOGL'] #매수 가능 수량
        buy_quantity=min(maxbuy, user['max_buy_quantity']) #매수 수량 결정
        user['portfolio'], message=buy_stock(user['portfolio'], 'GOOGL', current_price['GOOGL'], buy_quantity) #매수 실행
        if buy_quantity>0:
            print(message)

    elif current_price['GOOGL']>user['sell_threshold']*googl_5day_mean_price: #GOOGL 매도해야 하는 경우
        maxsell=user['portfolio']['holdings']['GOOGL']
        sell_quantity=min(maxsell, user['max_sell_quantity'])
        user['portfolio'], message=sell_stock(user['portfolio'], 'GOOGL', current_price['GOOGL'], sell_quantity)
        if sell_quantity>0:
            print(message)

    return user['portfolio']

    #######################  END CODE HERE  ########################

def update_price_history(price_history, current_price):
    #######################  START CODE HERE  ######################

    #가격 업데이트
    price_history['AAPL'].append(current_price['AAPL'])
    price_history['GOOGL'].append(current_price['GOOGL'])
    if len(price_history['AAPL'])>5: #길이가 5보다 긴 경우에 과거 데이터는 제거
        price_history['AAPL']=price_history['AAPL'][1:]
        price_history['GOOGL'] = price_history['GOOGL'][1:]

    return price_history

    #######################  END CODE HERE  ########################

def run_simulation(file_path, users):
    market_data = read_market_data(file_path)
    if not market_data:
        print("No market data available for simulation.")

    #######################  START CODE HERE  ######################
    price_history={'AAPL':[], 'GOOGL':[]} #price history 생성
    current_price=None
    #각 일자별 계산
    for i in range(len(market_data)): #market data 안에 데이터 갯수 만큼 반복문 수행
        current_price={'AAPL': float(market_data[i]['AAPL']), 'GOOGL': float(market_data[i]['GOOGL'])} #current_price 생성

        print('Date:', market_data[i]['date'])
        for user in users: #각 유저에 대해 포트폴리오 업데이트
            #buy threshold와 sell threshold 값의 범위에 대한 예외 처리
            if user['buy_threshold'] >= 1:
                raise Exception('buy_threshold는 1보다 작아야 합니다')
            elif user['sell_threshold'] <= 1:
                raise Exception('sell_threshold는 1보다 커야 합니다')
            print('User %s:'%user['name'])
            user['portfolio']=apply_trading_strategy(user, current_price, price_history)
            print('Portfolio value = $%.2f, Cash = $%.2f, Holdings: AAPL = %d shares, GOOGL = %d shares'%(calculate_portfolio_value(user['portfolio'], current_price), user['portfolio']['cash'], user['portfolio']['holdings']['AAPL'], user['portfolio']['holdings']['GOOGL']))
        print()
        price_history=update_price_history(price_history, current_price)

    #각 유저에 대해 최종 포트폴리오 결과 출력
    print('Final Results:')
    for user in users:
        print('User %s:'%user['name'])
        final_value=calculate_portfolio_value(user['portfolio'], current_price) #current_price는 for문 마지막 실행시 가장 최근 것으로 업데이트 됨
        print('User %s: Final Portfolio Value = $%.2f'%(user['name'],final_value))

    #######################  END CODE HERE  ########################


## 실행 예시
## - 뼈대 코드를 지우지 말 것
## - 다른 설정으로 다양하게 테스트 해보는 것은 좋으나, 테스트 유저는 주석 처리하여 제출할 것

user1 = {
    'name': 'Alice',
    'portfolio': initialize_portfolio(10000),
    'buy_threshold': 0.95,
    'sell_threshold': 1.05,
    'max_buy_quantity': 10,
    'max_sell_quantity': 5
}

user2 = {
    'name': 'Bob',
    'portfolio': initialize_portfolio(10000),
    'buy_threshold': 0.97,
    'sell_threshold': 1.07,
    'max_buy_quantity': 15,
    'max_sell_quantity': 7
}

user3 = {
    'name': 'Charlie',
    'portfolio': initialize_portfolio(10000),
    'buy_threshold': 0.95,
    'sell_threshold': 1.10,
    'max_buy_quantity': 5,
    'max_sell_quantity': 3
}


# 시뮬레이션 실행
run_simulation('stock_data.txt', [user1, user2, user3])
