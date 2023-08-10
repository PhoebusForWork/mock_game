from flask import Blueprint, jsonify
import time
from utils.get_data_tool import get_response_data

transaction_bp = Blueprint('transaction', __name__)


@transaction_bp.route('/deposit/<merchant_id>', methods=['POST'])
def mock_deposit(merchant_id="1"):
    mock_data = get_response_data(merchant_id=merchant_id, method="deposit")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@transaction_bp.route('/withdraw/<merchant_id>', methods=['POST'])
def mock_withdraw(merchant_id="1"):
    mock_data = get_response_data(merchant_id=merchant_id, method="withdraw")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)
