import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# 환경변수 로딩
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# DB 연결
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cur = conn.cursor()

# CSV 읽기
df = pd.read_csv("ETF.csv", encoding="utf-8-sig")

# 결측치나 '-' 문자열 처리
def clean_value(val, target_type):
    if pd.isna(val) or val == '-':
        return None
    if target_type == 'date':
        try:
            return datetime.strptime(val, "%Y/%m/%d").date()
        except:
            return None
    return val

# full_path → etf_category_id 맵 사전 로딩
cur.execute("SELECT id, full_path FROM etf_category")
category_map = {row[1]: row[0] for row in cur.fetchall()}

# 삽입
for index, row in df.iterrows():
    try:
        full_path = row["분류체계"]
        etf_category_id = category_map.get(full_path)

        if not etf_category_id:
            print(f"❌ 분류체계 '{full_path}' 일치 없음 → Row {row['시퀀스']} 건너뜀")
            continue
        
        cur.execute("""
            INSERT IGNORE INTO etf (
                id, issue_code, issue_name, etf_category_id, return_1y,
                etf_obj_index_name, trace_err_rate, net_asset_total_amount, divergence_rate,
                volatility, issue_std_code, issue_name_ko, issue_name_abbrv, issue_name_en,
                list_date, idx_calc_inst_nm1, idx_calc_inst_nm2,
                etf_replication_method, idx_market_type, idx_asset_type, list_shrs,
                com_abbrv, cu_qtv, etf_total_fee, tax_type, risk_grade
            ) VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """, (
            row["시퀀스"],
            row["종목코드"],
            row["종목명"],
            etf_category_id,
            clean_value(row["수익률(최근 1년)"], None),
            row["기초지수"],
            clean_value(row["추적오차"], None),
            clean_value(row["순자산총액"], None),
            clean_value(row["괴리율"], None),
            row["변동성"],
            row["표준코드"],
            row["한글종목명"],
            row["한글종목약명"],
            row["영문종목명"],
            clean_value(row["상장일"], "date"),
            row["지수산출기관"],
            row["추적배수"],
            row["복제방법"],
            row["기초시장분류"],
            row["기초자산분류"],
            clean_value(row["상장좌수"], None),
            row["운용사"],
            clean_value(row["CU수량"], None),
            clean_value(row["총보수"], None),
            row["과세유형"],
            clean_value(row["위험등급"], None)
        ))
    except Exception as e:
        print(f"❌ Row {row['시퀀스']} 삽입 실패: {e}")
        continue

# 커밋 및 종료
conn.commit()
cur.close()
conn.close()
