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

challenge_data = [
    (13,  'ATTEND_7DAYS',         '연속 출석',                   '7일 연속으로 출석하면',              'STREAK', 0.1),
    (13,  'QUIZ_DAILY',           '출석체크 금융 퀴즈',          '출석체크 금융 퀴즈',                'DAILY',  0.02),
    (362, 'FIRST_INVEST_TEST',    '첫 투자성향 테스트',          '첫 투자성향 테스트',                'ONCE',   0.065),
    (406, 'FIRST_CONNECT_ISA',    '첫 ISA 계좌 연결',            '첫 ISA 계좌 연결',                  'ONCE',   0.084),
    (3,   'HOLD_ETF_3PLUS',       '보유 ETF 3종목 이상',         '보유 ETF 3종목 이상',               'ONCE',   0.115),
    (13,  'HOLD_ACCOUNT_500DAYS', '계좌 보유 기간 500일 달성',   '계좌 보유 기간 500일 달성',         'ONCE',   0.3),
    (3,   'VIEW_AI_PORTFOLIO',    '하나 원큐 AI포트폴리오 조회', '하나 원큐 AI포트폴리오 조회',       'ONCE',   0.2),
    (318, 'TEST_INVEST_DNA',      '하나 원큐 투자 DNA 테스트',   '하나 원큐 투자 DNA 테스트',         'ONCE',   0.2),
    (318, 'YEARLY_DEPOSIT',       '연간 납입 한도 100만원 이상', '연간 납입 한도 100만원 이상',       'ONCE',   0.077),
]

# Category 데이터 삽입
cur.executemany("""
    INSERT INTO challenge (etf_id, code, title, challenge_description, challenge_type, quantity)
    VALUES (%s, %s, %s, %s, %s, %s)
""", challenge_data)
conn.commit()
print("✅ Category 데이터 삽입 완료")

cur.close()
conn.close()
