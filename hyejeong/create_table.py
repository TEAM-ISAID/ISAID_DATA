import os
import mysql.connector
from dotenv import load_dotenv

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

# Category 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS etf_category (
    id INTEGER PRIMARY KEY,
    asset_class VARCHAR(100),
    asset_type VARCHAR(100),
    asset_subtype VARCHAR(100),
    full_path VARCHAR(100)
);
""")

# ETF 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS etf (
    id INTEGER PRIMARY KEY,
    issue_code VARCHAR(20),
    issue_name VARCHAR(100),
    etf_category_id INTEGER REFERENCES category(id),
    return_1y NUMERIC(5, 2),
    etf_obj_index_name VARCHAR(100),
    trace_err_rate NUMERIC(5, 2),
    net_asset_total_amount BIGINT,
    divergence_rate NUMERIC(5, 2),
    volatility VARCHAR(10),
    issue_std_code VARCHAR(20),
    issue_name_ko VARCHAR(100),
    issue_name_abbrv VARCHAR(100),
    issue_name_en VARCHAR(100),
    list_date DATE,
    idx_obj_index_name VARCHAR(100),
    idx_calc_inst_nm1 VARCHAR(100),
    idx_calc_inst_nm2 VARCHAR(100),
    etf_replication_method VARCHAR(50),
    idx_market_type VARCHAR(50),
    idx_asset_type VARCHAR(50),
    list_shrs BIGINT,
    com_abbrv VARCHAR(50),
    cu_qtv INTEGER,
    etf_total_fee NUMERIC(5, 2),
    tax_type VARCHAR(50)
);
""")

# ETF_PDF 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS etf_pdf (
    id INT AUTO_INCREMENT PRIMARY KEY,
    etf_id INTEGER NOT NULL,
    compst_issue_code VARCHAR(20),
    compst_issue_name VARCHAR(100),
    compst_issue_cu1_shares NUMERIC(15, 2),
    value_amount BIGINT,
    compst_amount BIGINT,
    compst_ratio NUMERIC(5, 2),
    FOREIGN KEY (etf_id) REFERENCES etf(id) ON DELETE CASCADE
);
""")

# ETF_PRICES 테이블 생성
cur.execute("""
CREATE TABLE IF NOT EXISTS etf_daily_trading (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    etf_id INTEGER NOT NULL,
    base_date DATE,
    issue_code VARCHAR(20),
    issue_name VARCHAR(100),
    cmp_prevdd_price NUMERIC(10, 2),
    fluc_rate NUMERIC(5, 2),
    tdd_close_price NUMERIC(10, 2),
    nav NUMERIC(10, 2),
    tdd_open_price NUMERIC(10, 2),
    tdd_high_price NUMERIC(10, 2),
    tdd_low_price NUMERIC(10, 2),
    acc_trade_volume BIGINT,
    acc_total_value BIGINT,
    market_cap BIGINT,
    net_asset_total_amount BIGINT,
    list_shrs BIGINT,
    idx_ind_nm VARCHAR(100),
    obj_stkprc_idx NUMERIC(10, 2),
    cmpprevdd_idx NUMERIC(10, 2),
    fluc_rt_idx NUMERIC(5, 2),
    FOREIGN KEY (etf_id) REFERENCES etf(id) ON DELETE CASCADE
);
""")

# 커밋 및 종료
conn.commit()
print("✅ 테이블 생성 완료")

cur.close()
conn.close()
