import requests
import json

# 인증키 불러오기
with open('config.json', 'r') as f:
    config = json.load(f)
api_key = config["api_key"]

def fetch_etf_daily_trade_data(base_date: str):
    url = "http://data-dbg.krx.co.kr/svc/apis/etp/etf_bydd_trd"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "basDd": base_date
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        etf_list = data.get("OutBlock_1", [])
        return etf_list
    else:
        print(f"API 요청 실패: {response.status_code}")
        return None

if __name__ == "__main__":
    base_date = "20250623"
    result = fetch_etf_daily_trade_data(base_date)
    if result:
        import pandas as pd
        df = pd.DataFrame(result)
        output_path = f"giiii/신규/{base_date}.csv"
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"데이터 저장 완료: {output_path}")