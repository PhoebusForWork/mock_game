## LD 3.0 假三方遊戲

#### 環境需求
```
python 3.9.x
```

#### 啟動方式
```
1、安裝相應的python套件
pip install -r requirements.txt
2、啟動mock service
python main.py
```

#### 使用說明
```
目前提供的API，皆使用POST method：
{host}/getGameOrderList/{merchant_id}	        撈注單
{host}/getTransferOrderList/{merchant_id}	查詢轉帳記錄
{host}/getBalance/{merchant_id}       	        查詢用戶餘額
{host}/deposit/{merchant_id}                    存款 (存款至三方平台)
{host}/withdraw/{merchant_id}	                取款 (從三方平台取款)

url參數說明：
host: 主機所在的host
merchant_id: 假三方的商戶ID，預設為1 (1：AI體育)

host說明：
sit環境： https://mock-game-merchant-sit.prj300.xyz/
qa環境： https://mock-game-merchant-qa.prj300.xyz/
automation環境： https://mock-game-merchant-automation.prj300.xyz/ (待確認，Billy建置環境中)

curl sample：
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8888/getGameOrderList/1

回傳資料可在以下目錄中設置 (回傳資料格式需符合三方格式，後端服務才能正常解析)：
/data/{merchant}/*.json
```