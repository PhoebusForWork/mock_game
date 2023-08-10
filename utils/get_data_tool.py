from flask import g
import json5


# 獲取資料
def get_response_data(merchant_id, method=''):
    if merchant_id == "1":
        merchant_name = "ai"
    else:
        return g.no_specify_merchant

    source = f"./data/{merchant_name}/{method}_response.json5"

    try:
        with open(source, mode='r', encoding='utf8') as f:
            data = json5.load(f)
    except Exception:
        raise

    return data
