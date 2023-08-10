from flask import Flask, jsonify, g
from api.game_order import game_order_bp
from api.transaction import transaction_bp


app = Flask(__name__)
app.config['previous_request_timestamp'] = 0


# 設定基礎預設資料
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


# 註冊 API 路由藍圖
# 遊戲注單相關
app.register_blueprint(game_order_bp, url_prefix='/api')
app.register_blueprint(transaction_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
