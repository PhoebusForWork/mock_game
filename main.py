from flask import g, request, jsonify, Flask
import time
import json


app = Flask(__name__)


def _get_data(merchant_id, method=''):
    if merchant_id == "1":
        merchant_name = "ai"
    else:
        return g.no_specify_merchant

    if method == "login":
        source = f"data/{merchant_name}/login_response.json"
    elif method == "order":
        source = f"data/{merchant_name}/order_response.json"
    elif method == "transfer":
        source = f"data/{merchant_name}/transfer_response.json"
    elif method == "balance":
        source = f"data/{merchant_name}/balance_response.json"
    elif method == "deposit":
        source = f"data/{merchant_name}/deposit_response.json"
    elif method == "withdraw":
        source = f"data/{merchant_name}/withdraw_response.json"
    else:
        raise Exception("no specify method")

    try:
        with open(source, mode='r', encoding='utf8') as f:
            data = json.load(f)
    except Exception:
        raise

    return data


@app.before_request
def set_up_data():
    g.key = {"h5AppId": "92d272576dde4a4dc6f9ece81626d641", "appActualKey": "L8IbnjHo8OTu+LBwjQA4dw=="}
    g.no_specify_merchant = {"code": 400, "msg": "No specify merchant id"}


@app.route('/login', methods=['POST'])
def mock_login():
    try:
        param_merchant_id = request.args.get("merchantId", default="1")
    except Exception:
        raise

    mock_data = _get_data(merchant_id=param_merchant_id, method="login")
    if mock_data["code"] == 200:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        current_timestamp = int(time.time()*1000)
        mock_data["data"]["list"][0]["tradeDate"] = current_time
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/order', methods=['POST'])
def mock_order():
    try:
        param_merchant_id = request.args.get("merchantId", default="1")
    except Exception:
        raise

    mock_data = _get_data(merchant_id=param_merchant_id, method="order")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/transfer', methods=['POST'])
def mock_transfer():
    try:
        param_merchant_id = request.args.get("merchantId", default="1")
    except Exception:
        raise

    mock_data = _get_data(merchant_id=param_merchant_id, method="transfer")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/balance', methods=['POST'])
def mock_balance():
    try:
        param_merchant_id = request.args.get("merchantId", default="1")
    except Exception:
        raise

    mock_data = _get_data(merchant_id=param_merchant_id, method="balance")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/deposit', methods=['POST'])
def mock_deposit():
    try:
        param_merchant_id = request.args.get("merchantId", default="1")
    except Exception:
        raise

    mock_data = _get_data(merchant_id=param_merchant_id, method="deposit")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/withdraw', methods=['POST'])
def mock_withdraw():
    try:
        param_merchant_id = request.args.get("merchantId", default="1")
    except Exception:
        raise

    mock_data = _get_data(merchant_id=param_merchant_id, method="withdraw")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
