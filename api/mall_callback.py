from flask import Blueprint,request , jsonify
import logging
from utils.get_data_tool import get_response_data

mall_callback_bp = Blueprint('mall_callback', __name__)

# 设置日志级别为DEBUG
logging.basicConfig(level=logging.DEBUG)

@mall_callback_bp.route('/mall/callback', methods=['POST'])
def callback():
    # 獲取回調內容
    callback_data = request.json
    status_value = request.args.get('status')
    # 回調日誌
    logging.debug('回調參數: %s', callback_data)

    # 返回成功
    return {"status": status_value}, 200

user_balances = {
    "testUser": {"water": 10, "currentBalance": 20, "P": 100},
    "user2": {"water": 0, "currentBalance": 0, "P": 0},
}

#用戶點數查詢
@mall_callback_bp.route('/qry_current_balance', methods=['POST'])
def getPoint():
    # 获取回调内容
    callback_data = request.json

    # 从回调数据中提取用户名
    username = callback_data.get('username')

    # 如果用户名不存在于预定初始值
    if username not in user_balances:
        user_balances[username] = {"water": 10, "currentBalance": 11, "P": 100}

    # 获取用户的当前余额
    p = user_balances[username]["P"]

    # 构造用户信息字典
    user_info = {
        "code": 1,
        "message": "SUCCESS",
        "data": {
            "username": username,
            "currentBalance": p
        }
    }

    # 输出回调日志
    logging.debug('回调参数: %s', callback_data)
    logging.debug('查詢基本資訊 %s : %s',username ,user_balances[username])
    logging.debug("回傳",user_info)
    # 返回成功响应
    return jsonify(user_info), 200

#紅包回調
@mall_callback_bp.route('/gl/task/point/exchange/callback', methods=['POST'])
def exchange_callback():
    # 获取回调内容
    callback_data = request.json

    # 从回调数据中提取用户名、奖励、水量、兑换积分、当前余额
    username = callback_data.get('username')
    reward = callback_data.get('reward')
    water = callback_data.get('water')
    exchange_points = callback_data.get('exchangePoints')
    current_balance = callback_data.get('currentBalance')

    # 如果用户名不存在于预定义的用户余额字典中，则返回错误响应
    if username not in user_balances:
        return jsonify({"error": "User not found"}), 404

    # 更新用户的当前余额、水量和 P 值
    user = user_balances[username]
    logging.debug('原始基本資訊 %s : %s', username, user )
    user["currentBalance"] += reward if reward is not None else 0
    user["water"] += water if water is not None else 0
    user["P"] -= exchange_points  # 兑换积分
    logging.debug('調整基本資訊 %s : %s', username, user )
    # 输出回调日志
    logging.debug('回调参数: %s', callback_data)
    status= {"status": "success"}
    logging.debug("回傳", status)
    # 返回成功响应
    return jsonify(status), 200