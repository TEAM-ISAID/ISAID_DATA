from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys

ETF_ID = 136
ETF_CODE = "251350"
OUTPUT_FILE = "pdf.csv"

# 셀레니움 설정
options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    url = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030108"
    driver.get(url)
    time.sleep(3)

    # 종목 입력 필드 (정확한 ID 사용)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tboxisuCd_finder_secuprodisu1_0"))
    )
    etf_input = driver.find_element(By.ID, "tboxisuCd_finder_secuprodisu1_0")
    etf_input.clear()
    etf_input.clear()
    etf_input.send_keys(ETF_CODE)
    time.sleep(1)
    etf_input.send_keys(Keys.ENTER)
    time.sleep(1)

    # 날짜 입력 필드
    # date_input = driver.find_element(By.ID, "trdDd")
    # date_input.clear()
    # date_input.send_keys(DATE)
    # time.sleep(1)

    # 조회 버튼 클릭
    driver.find_element(By.ID, "jsSearchButton").click()

    # 테이블 로딩 대기
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".CI-GRID-BODY-TABLE-TBODY tr"))
    )
    time.sleep(4)

    # 데이터 파싱
    rows = driver.find_elements(By.CSS_SELECTOR, ".CI-GRID-BODY-TABLE-TBODY tr")[:10]
    results = []

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 6:
            continue

        x = cols[1].text.strip()
        if x in ["원화현금", "설정현금액"]:
            continue  # 제외 조건

        def clean_number(text):
            return "" if text.strip() == "-" else text.strip().replace(",", "")

        results.append([
            ETF_ID,
            cols[0].text.strip(),  # 종목코드
            cols[1].text.strip(),  # 구성종목명
            clean_number(cols[2].text),         # 주식수
            clean_number(cols[3].text),         # 평가금액
            clean_number(cols[4].text),         # 시가총액
            clean_number(cols[5].text),         # 시가총액 기준 구성비중
        ])

    # CSV 저장
    df = pd.DataFrame(results, columns=["ID", "종목코드", "구성종목명", "주식수", "평가금액", "시가총액", "시가총액기준구성비중"])
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"[✅] '{OUTPUT_FILE}' 저장 완료!")

finally:
    driver.quit()
