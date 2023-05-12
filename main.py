from flask import g, request, jsonify, Flask
import time
import json5


app = Flask(__name__)
app.config['previous_request_timestamp'] = 0


def _get_response_data(merchant_id, method=''):
    if merchant_id == "1":
        merchant_name = "ai"
    else:
        return g.no_specify_merchant

    source = f"app/data/{merchant_name}/{method}_response.json5"

    try:
        with open(source, mode='r', encoding='utf8') as f:
            data = json5.load(f)
    except Exception:
        raise

    return data


@app.before_request
def set_up_data():
    g.key = {"h5AppId": "92d272576dde4a4dc6f9ece81626d641", "appActualKey": "L8IbnjHo8OTu+LBwjQA4dw=="}
    g.greeting = {"code": 200, "msg": "Hello guest"}
    g.no_specify_merchant = {"code": 400, "msg": "No specify merchant id"}
    g.no_specify_method = {"code": 400, "msg": "No specify method"}
    g.no_data_response_ai = {"code": 200, "msg": "SUCCESS", "systemTime": 1683611637266, "data": {"totalCount": 0, "orderDTO": []}}


@app.route('/', methods=['GET', 'POST'])
def index():
    return jsonify(g.greeting)


@app.route('/getGameOrderList/<merchant_id>', methods=['POST'])
def mock_order(merchant_id="1"):
    current_timestamp = int(time.time() * 1000)
    if current_timestamp > app.config['previous_request_timestamp'] + 10 * 1000:
        mock_data = _get_response_data(merchant_id=merchant_id, method="order")
        app.config['previous_request_timestamp'] = current_timestamp
    else:
        mock_data = g.no_data_response_ai

    if mock_data["code"] == 200:
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/getTransferOrderList/<merchant_id>', methods=['POST'])
def mock_transfer(merchant_id="1"):
    mock_data = _get_response_data(merchant_id=merchant_id, method="transfer")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time() * 1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/getBalance/<merchant_id>', methods=['POST'])
def mock_balance(merchant_id="1"):
    mock_data = _get_response_data(merchant_id=merchant_id, method="balance")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/deposit/<merchant_id>', methods=['POST'])
def mock_deposit(merchant_id="1"):
    mock_data = _get_response_data(merchant_id=merchant_id, method="deposit")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


@app.route('/withdraw/<merchant_id>', methods=['POST'])
def mock_withdraw(merchant_id="1"):
    mock_data = _get_response_data(merchant_id=merchant_id, method="withdraw")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp

    return jsonify(mock_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
