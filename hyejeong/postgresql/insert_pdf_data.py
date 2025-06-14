import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# CSV 파일 로드
df = pd.read_csv("1q_pdf.csv", encoding="utf-8-sig")

def safe_int(val):
    try:
        if pd.isna(val) or val == '-':
            return None
        return int(float(val))
    except:
        return None

def safe_float(val):
    try:
        if pd.isna(val) or val == '-':
            return None
        return round(float(val), 2)
    except:
        return None

# 연결
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# 삽입
for index, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO etf_pdf (
                etf_id,
                compst_issue_code,
                compst_issue_name,
                compst_issue_cu1_shares,
                value_amount,
                compst_amount,
                compst_ratio
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            int(row["ID"]),
            str(row["종목코드"]),
            row["구성종목명"],
            safe_float(row["주식수"]),
            safe_int(row["평가금액"]),
            safe_int(row["시가총액"]),
            safe_float(row["시가총액기준구성비중"]),
        ))
    except Exception as e:
        conn.rollback()
        print(f"❌ Row {index} 삽입 실패: {e}")
        continue


# 커밋 및 연결 해제
conn.commit()
cur.close()
conn.close()
