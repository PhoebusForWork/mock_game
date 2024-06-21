from flask import Blueprint, request, jsonify, g, current_app
from faker import Faker
import time
import random
import datetime
from concurrent.futures import ThreadPoolExecutor

fake = Faker()

user_names = [f'uf88ga{i}' for i in range(2, 22+1)]

def AI_order(from_time, to_time):
    order = {
        "merId": fake.uuid4(),
        "merName": fake.company(),
        "playerId": fake.uuid4(),
        # 這邊暫時先用測試帳號代替
        # "loginName": fake.user_name(),
        "loginName": random.choice(user_names),
        "playerName": fake.name(),
        "remoteIp": fake.ipv4(),
        "orderId": fake.bothify(text='????????_###'),
        "parlayNum": str(random.randint(1, 5)),
        "gold": random.randint(100, 1000),
        "realGold": random.randint(100, 1000),
        "winGold": random.randint(100, 1000),
        "state": random.choice([1, 2, 3]),
        "creditState": random.choice([0, 1]),
        "realResultDate": fake.date_time_between(start_date=from_time, end_date=to_time).isoformat(),
        "resultDate": fake.date_time_between(start_date=from_time, end_date=to_time).isoformat(),
        "resultDetail": random.choice(['W', 'L']),
        "createDate": fake.date_time_between(start_date=from_time, end_date=to_time).isoformat(),
        "terminalType": str(random.randint(1, 5)),
        "oddfType": random.choice(['A', 'B', 'C']),
        "betDTOList": [],
        "lineType": str(random.randint(1, 5)),
        "cashoutType": str(random.randint(0, 1)),
        "cashouts": {
            "cashoutId": None,
            "stake": None,
            "initGold": None,
            "returnAmount": None,
            "wlAmount": None,
            "placeDateTime": None,
            "state": None
        },
        "betNum": random.randint(1, 10),
        "lang": "zh-cn",
        "walletId": random.randint(1, 5),
        "validAmount": random.randint(100, 1000)
    }
    for _ in range(order["betNum"]):
        bet = {
            "showType": fake.word(),
            "gameType": fake.word(),
            "playType": fake.word(),
            "ratioType": fake.word(),
            "gameDate": fake.date_between(start_date=from_time, end_date=to_time).isoformat(),
            "gameTime": fake.time(),
            "awayTeam": fake.word(),
            "homeTeam": fake.word(),
            "leagueName": fake.word(),
            "leagueShortName": fake.word(),
            "score": fake.word(),
            "ioRatio": fake.word(),
            "ratio": fake.word(),
            "resultScore": fake.word(),
            "betItem": fake.word(),
            "betResultDetail": random.choice(['W', 'L']),
            "session": None,
            "teamSuffix": fake.word(),
            "awayLangTeam": fake.word(),
            "homeLangTeam": fake.word(),
            "leagueLangName": fake.word(),
            "leagueShortLangName": fake.word(),
            "betItem1": fake.word(),
            "playNameLang": fake.word(),
            "playName": fake.word(),
            "betItemLang": fake.word(),
            "gameId": fake.uuid4()
        }
        order["betDTOList"].append(bet)
    return order

# 定义 merchant2 的订单生成逻辑
def JILI_order(from_time, to_time):
    order = {
        # "Account": fake.user_name(),
        "Account": random.choice(user_names),
        "WagersId": fake.random_number(digits=18, fix_len=True),
        "GameId": random.randint(1, 100),
        "WagersTime": datetime.datetime.strptime(fake.date_time_between(start_date=from_time, end_date=to_time).isoformat()[:19], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'),
        "BetAmount": round(random.uniform(-10, -1), 2),
        "PayoffTime": datetime.datetime.strptime(fake.date_time_between(start_date=from_time, end_date=to_time).isoformat()[:19], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'),
        "PayoffAmount": round(random.uniform(0, 10), 2),
        "Status": random.choice([1, 2, 3]),
        "SettlementTime": datetime.datetime.strptime(fake.date_time_between(start_date=from_time, end_date=to_time).isoformat()[:19], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'),
        "GameCategoryId": random.randint(1, 10),
        "VersionKey": 0,
        "Type": random.randint(1, 2),
        "AgentId": fake.bothify(text='????????_#####'),
        "Turnover": round(random.uniform(1, 10), 2)
    }
    return order


# 默认订单格式
def generate_default_order(from_time, to_time):
    return {
        "merId": fake.uuid4(),
        "merName": fake.company(),
        "playerId": fake.uuid4(),
        # "loginName": fake.user_name(),
        "loginName": random.choice(user_names),
        "playerName": fake.name(),
        "remoteIp": fake.ipv4(),
        "orderId": fake.bothify(text='????????_###'),
        "parlayNum": str(random.randint(1, 5)),
        "gold": random.randint(100, 1000),
        "realGold": random.randint(100, 1000),
        "winGold": random.randint(100, 1000),
        "state": random.choice([1, 2, 3]),
        "creditState": random.choice([0, 1]),
        "realResultDate": fake.date_time_between(start_date=from_time, end_date=to_time).isoformat(),
        "resultDate": fake.date_time_between(start_date=from_time, end_date=to_time).isoformat(),
        "resultDetail": random.choice(['W', 'L']),
        "createDate": fake.date_time_between(start_date=from_time, end_date=to_time).isoformat(),
        "terminalType": str(random.randint(1, 5)),
        "oddfType": random.choice(['A', 'B', 'C']),
        "betDTOList": [],
        "lineType": str(random.randint(1, 5)),
        "cashoutType": str(random.randint(0, 1)),
        "cashouts": {
            "cashoutId": None,
            "stake": None,
            "initGold": None,
            "returnAmount": None,
            "wlAmount": None,
            "placeDateTime": None,
            "state": None
        },
        "betNum": random.randint(1, 10),
        "lang": "zh-cn",
        "walletId": random.randint(1, 5),
        "validAmount": random.randint(100, 1000)
    }

def generate_order(from_time, to_time, merchan_code):
    if merchan_code == 'AI':
        return AI_order(from_time, to_time)
    elif merchan_code == 'JILI':
        return JILI_order(from_time, to_time)
    else:
        return generate_default_order(from_time, to_time)

def generate_orders(num_orders, from_time, to_time, merchant_code):
    with ThreadPoolExecutor() as executor:
        orders = list(executor.map(lambda _: generate_order(from_time, to_time, merchant_code), range(num_orders)))
    if merchant_code == 'JILI':
        response_data = {
            "ErrorCode": 0,
            "Message": "",
            "Data": {
                "Result": orders,
                "Pagination": {
                    "CurrentPage": 1,
                    "TotalPages": 1,
                    "PageLimit": num_orders,
                    "TotalNumber": len(orders)
                }
            }
        }
    #merchant_code=AI
    else: 
        response_data = {
            "code": 200,
            "msg": "SUCCESS",
            "systemTime": int(time.time() * 1000),
            "data": {
                "totalCount": len(orders),
                "orderDTO": orders
            },
            "t": -1
        }
    return response_data

