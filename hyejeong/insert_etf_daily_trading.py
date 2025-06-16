import os
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# 환경변수 로딩
load_dotenv()

# DB 연결
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cur = conn.cursor()

# 결측치 또는 '-' 문자열을 처리
def clean_value(val, target_type=None):
    if pd.isna(val) or str(val).strip() == '-':
        return None
    if target_type == 'date':
        try:
            return datetime.strptime(str(val), "%Y%m%d").date()
        except:
            return None
    return val

# etf_id를 종목코드(issue_code) 기준으로 가져오기 위한 맵 생성
cur.execute("SELECT id, issue_code FROM etf")
etf_code_map = {row[1]: row[0] for row in cur.fetchall()}

# 폴더 내 모든 CSV 파일 처리
folder_path = "new"
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        print(f"📂 파일 처리 중: {file_path}")

        df = pd.read_csv(file_path, encoding="utf-8-sig")

        for index, row in df.iterrows():
            try:
                issue_code = str(row["ISU_CD"]).zfill(6)
                etf_id = etf_code_map.get(issue_code)

                if not etf_id:
                    print(f"❌ 종목코드 '{issue_code}' 일치 없음 → Row {index+1} 건너뜀")
                    continue

                cur.execute("""
                    INSERT INTO etf_daily_trading (
                        etf_id, base_date, issue_code, issue_name,
                        cmp_prevdd_price, fluc_rate, tdd_close_price, nav,
                        tdd_open_price, tdd_high_price, tdd_low_price,
                        acc_trade_volume, acc_total_value, market_cap,
                        net_asset_total_amount, list_shrs, idx_ind_nm,
                        obj_stkprc_idx, cmpprevdd_idx, fluc_rt_idx
                    ) VALUES (
                        %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s
                    )
                """, (
                    etf_id,
                    clean_value(row["BAS_DD"], "date"),
                    issue_code,
                    row["ISU_NM"],
                    clean_value(row["CMPPREVDD_PRC"]),
                    clean_value(row["FLUC_RT"]),
                    clean_value(row["TDD_CLSPRC"]),
                    clean_value(row["NAV"]),
                    clean_value(row["TDD_OPNPRC"]),
                    clean_value(row["TDD_HGPRC"]),
                    clean_value(row["TDD_LWPRC"]),
                    clean_value(row["ACC_TRDVOL"]),
                    clean_value(row["ACC_TRDVAL"]),
                    clean_value(row["MKTCAP"]),
                    clean_value(row["INVSTASST_NETASST_TOTAMT"]),
                    clean_value(row["LIST_SHRS"]),
                    row["IDX_IND_NM"],
                    clean_value(row["OBJ_STKPRC_IDX"]),
                    clean_value(row["CMPPREVDD_IDX"]),
                    clean_value(row["FLUC_RT_IDX"])
                ))
            except Exception as e:
                print(f"❌ {file_name} Row {index+1} 삽입 실패: {e}")
                continue

# 커밋 및 종료
conn.commit()
cur.close()
conn.close()
print("✅ 모든 CSV 파일 데이터 삽입 완료")
