from flask import Blueprint, request, jsonify, g, current_app
from faker import Faker
# current_app是用來拿取對應的config物件的
import time
import threading
import datetime
from utils.get_data_tool import get_response_data
from utils.game_order_generator import generate_orders


lock = threading.Lock()
fake = Faker()

# 製作一個Blueprint物件
game_order_bp = Blueprint('game_order', __name__)


@game_order_bp.route('/getGameOrderList/<merchant_id>', methods=['POST'])
def mock_order(merchant_id="1"):
    with lock:
        # 用prarms取得注單種類,預設為order
        type_value = request.args.get('type')
        type_result = 'order' if type_value is None else type_value

        current_timestamp = int(time.time() * 1000)
        print(f"current_timestamp = {current_timestamp}", flush=True)
        print(f"previous_request_timestamp = {current_app.config['previous_request_timestamp']}", flush=True)
        # 判斷是否重複請求
        if current_timestamp < current_app.config['previous_request_timestamp'] + 10 * 1000 and type_result == 'order':
            mock_data = g.no_data_response_ai
        else:
            mock_data = get_response_data(merchant_id=merchant_id, method=type_result)
            current_app.config['previous_request_timestamp'] = current_timestamp
            
        # 這邊要去看新接的遊戲回傳代碼做判斷調整
        if mock_data.get("code") == 200 or mock_data.get("status") == 200:
            mock_data["systemTime"] = current_timestamp

        return jsonify(mock_data)


@game_order_bp.route('/getTransferOrderList/<merchant_id>', methods=['POST'])
def mock_transfer(merchant_id="1"):
    mock_data = get_response_data(merchant_id=merchant_id, method="transfer")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time() * 1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@game_order_bp.route('/getBalance/<merchant_id>', methods=['POST'])
def mock_balance(merchant_id="1"):
    mock_data = get_response_data(merchant_id=merchant_id, method="balance")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)

@game_order_bp.route('/get_orders/<merchant_code>', methods=['GET'])
def get_orders(merchant_code="AI"):
    num_orders = int(request.args.get('num_orders', 100))
    
    # 獲取當前日期的開始與結束時間
    now = datetime.datetime.now()
    default_from_time = now.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
    default_to_time = now.replace(hour=23, minute=59, second=59, microsecond=999999).strftime('%Y-%m-%d %H:%M:%S')
    
    from_time = request.args.get('from_time', default_from_time)
    to_time = request.args.get('to_time', default_to_time)
    
    from_time = datetime.datetime.strptime(from_time, '%Y-%m-%d %H:%M:%S')
    to_time = datetime.datetime.strptime(to_time, '%Y-%m-%d %H:%M:%S')
    
    orders = generate_orders(num_orders, from_time, to_time, merchant_code)
    
    return jsonify(orders)