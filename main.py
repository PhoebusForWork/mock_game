from flask import g, request, jsonify, Flask
from cipher import AESCipher
import time, json


key = "L8IbnjHo8OTu+LBwjQA4dw=="
app = Flask(__name__)
aes = AESCipher(secret_key=key)


def _get_data(merchant_id, method=''):
    source = ""
    if merchant_id == "1":
        merchant_name = "ai"
    else:
        return g.no_specify_merchant

    if method == "login":
        source = f"data/{merchant_name}/login_response.json"
    elif method == "order":
        source = f"data/{merchant_name}/order_response.json"

    try:
        with open(source, mode='r', encoding='utf8') as f:
            data = json.load(f)
    except Exception:
        raise

    return data


@app.before_request
def set_up_data():
    g.key = {"h5AppId": "92d272576dde4a4dc6f9ece81626d641", "appActualKey": "L8IbnjHo8OTu+LBwjQA4dw=="}
    g.login_fail_response = {"code": 400, "msg": "LOGIN FAILED"}
    g.no_specify_merchant = {"code": 400, "msg": "No specify merchant id"}


@app.route('/merchantapi/multiCurrency/player/mixLogin', methods=['POST'])
def login_mock():
    """
        request body:
        {"merchantId":"da7450d1ff4f0abd0bd7ec7c3a1d4ba9", "appId" : "b42feb8cf7066bf96afd72645a0ddf34", "env" : "1", "data": { "loginName": "daotest001", "nickName": "daotest001", "headImg": "", "wid":"1", "merchantPayNo": "dao0707test001", "amountStr":"[{\"walletType\":\"1\",\"amount\":\"100\"},{\"walletType\":\"2\",\"amount\":\"100\"},{\"walletType\":\"3\",\"amount\":\"1000000\"}]" } }
        response body:
        {"code": 200, "msg": "SUCCESS", "systemTime": 1625642964351, "data": { "token": "begerge1db65679e3dfccc53c", "playerId": "3ff2889e81ergea5849e", "betUrl": "http://gergerg/dataview/bet?theme=100&lang=zh-cn&terType=1&token=gerg9fe2a7d74e1dgdfg79e3dfccc53c", "list":[]}}
    """
    try:
        request_body = request.json
        param_merchant_id = request.args.get("merchantId", default="1")
        param_test_wallet = request.args.get("testWallet")
        param_time_type = request.args.get("timeType")
        if param_test_wallet:
            print(param_test_wallet)
        if param_time_type:
            print(param_time_type)
        if request_body["data"]:
            request_data = eval(aes.decrypt(request_body["data"]))
        else:
            return jsonify(g.login_fail_response)
    except Exception:
        raise

    mock_data = _get_data(merchant_id=param_merchant_id, method="login")
    if mock_data["code"] == 200:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        current_timestamp = int(time.time()*1000)
        mock_data["data"]["playerId"] = request_data["loginName"]
        mock_data["data"]["list"][0]["tradeDate"] = current_time
        mock_data["systemTime"] = current_timestamp
    print(mock_data)

    return jsonify(mock_data)


@app.route('/merchantapi/multiCurrency/order/streamline/list', methods=['POST'])
def order_mock():
    try:
        param_merchant_id = request.args.get("merchantId", default="1")
        param_test_wallet = request.args.get("testWallet", default=1)
        param_time_type = request.args.get("timeType", default=1)
        if param_test_wallet:
            pass
        if param_time_type:
            pass
    except Exception:
        raise

    mock_data = _get_data(merchant_id=param_merchant_id, method="order")
    if mock_data["code"] == 200:
        current_timestamp = int(time.time()*1000)
        mock_data["systemTime"] = current_timestamp
    print(mock_data)

    return jsonify(mock_data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
