from flask import Blueprint, jsonify, g, current_app
# current_app是用來拿取對應的config物件的
import time
import threading
from utils.get_data_tool import get_response_data


lock = threading.Lock()


# 製作一個Blueprint物件
game_order_bp = Blueprint('game_order', __name__)


@game_order_bp.route('/getGameOrderList/<merchant_id>', methods=['POST'])
def mock_order(merchant_id="1"):
    with lock:
        current_timestamp = int(time.time() * 1000)
        print(f"current_timestamp = {current_timestamp}", flush=True)
        print(f"previous_request_timestamp = {current_app.config['previous_request_timestamp']}", flush=True)
        if current_timestamp > current_app.config['previous_request_timestamp'] + 10 * 1000:
            mock_data = get_response_data(merchant_id=merchant_id, method="order")
            current_app.config['previous_request_timestamp'] = current_timestamp
        else:
            mock_data = g.no_data_response_ai

        if mock_data["code"] == 200:
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
