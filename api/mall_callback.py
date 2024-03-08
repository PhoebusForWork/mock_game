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

    # 回調日誌
    logging.debug('回調參數: %s', callback_data)

    # 返回成功
    return {"status": "fail"}, 200


