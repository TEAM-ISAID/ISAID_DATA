import os
import psycopg2
from dotenv import load_dotenv

# 환경변수 로딩
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# DB 연결
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Category 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY,
    asset_class VARCHAR(100),
    asset_type VARCHAR(100),
    asset_subtype VARCHAR(100),
    full_path VARCHAR(255)
);
""")

# ETF 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS etf (
    id INTEGER PRIMARY KEY,
    issue_code VARCHAR(20),
    issue_name TEXT,
    category_id INTEGER REFERENCES category(id),
    return_1y NUMERIC(5, 2),
    etf_obj_index_name TEXT,
    trace_err_rate NUMERIC(5, 2),
    net_asset_total_amount BIGINT,
    divergence_rate NUMERIC(5, 2),
    volatility VARCHAR(10),
    issue_std_code VARCHAR(20),
    issue_name_ko TEXT,
    issue_name_abbr TEXT,
    issue_name_en TEXT,
    list_date DATE,
    idx_obj_index_name TEXT,
    idx_calc_inst_nm1 VARCHAR(100),
    idx_calc_inst_nm2 VARCHAR(100),
    etf_replication_method VARCHAR(50),
    idx_market_type VARCHAR(50),
    idx_asset_type VARCHAR(50),
    list_shrs BIGINT,
    com_abbrv VARCHAR(50),
    cu_qtv INTEGER,
    etf_total_fee NUMERIC(5, 2),
    tax_type TEXT
);
""")

# ETF_PDF 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS etf_pdf (
    id SERIAL PRIMARY KEY,
    etf_id INTEGER REFERENCES etf(id),
    compst_issue_code VARCHAR(20),
    compst_issue_name TEXT,
    compst_issue_cu1_shares NUMERIC(15, 2),
    value_amount BIGINT,
    compst_amount BIGINT,
    compst_ratio NUMERIC(5, 2)
);
""")

# 커밋 및 종료
conn.commit()
print("✅ 테이블 생성 완료")

cur.close()
conn.close()
