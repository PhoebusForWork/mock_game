from flask import g
import json5


# 獲取資料
def get_response_data(merchant_id, method=''):
    # 定義遊戲id
    MERCHANT_ID_MAPPING = {
        "1": "ai",
        "75": "spinix",
        "78": "evo"
    }
    # 若不存在則返回錯誤信息
    if merchant_id not in MERCHANT_ID_MAPPING:
        return g.no_specify_merchant

    merchant_name = MERCHANT_ID_MAPPING[merchant_id]

    source = f"data/{merchant_name}/{method}_response.json5"

    try:
        with open(source, mode='r', encoding='utf8') as f:
            data = json5.load(f)
    except Exception:
        raise

    return data
