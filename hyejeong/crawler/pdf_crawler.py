from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import csv

INPUT_CSV = "1q/1q_etf_sorted.csv"     # ETF 정보가 담긴 CSV
OUTPUT_FILE = "1q/1q_pdf.csv"        # 결과 저장 파일

# 셀레니움 옵션 설정
options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def clean_number(text):
    return "" if text.strip() == "-" else text.strip().replace(",", "")

def crawl_etf_data(etf_id, etf_code):
    url = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201030108"
    driver.get(url)
    time.sleep(3)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tboxisuCd_finder_secuprodisu1_0"))
        )
        etf_input = driver.find_element(By.ID, "tboxisuCd_finder_secuprodisu1_0")
        etf_input.clear()
        etf_input.send_keys(str(etf_code))
        time.sleep(1)
        etf_input.send_keys(Keys.ENTER)
        time.sleep(1)

        driver.find_element(By.ID, "jsSearchButton").click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".CI-GRID-BODY-TABLE-TBODY tr"))
        )
        time.sleep(5)

        rows = driver.find_elements(By.CSS_SELECTOR, ".CI-GRID-BODY-TABLE-TBODY tr")[:10]
        result_rows = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 6:
                continue
            if cols[1].text.strip() in ["원화현금", "설정현금액"]:
                continue

            result_rows.append([
                etf_id,
                cols[0].text.strip(),
                cols[1].text.strip(),
                clean_number(cols[2].text),
                clean_number(cols[3].text),
                clean_number(cols[4].text),
                clean_number(cols[5].text)
            ])
        return result_rows

    except Exception as e:
        print(f"[⚠️] ETF {etf_id}, {etf_code} 에서 오류 발생: {e}")
        return []

# ETF 목록 로드
etf_list = pd.read_csv(INPUT_CSV)[["시퀀스", "종목코드"]].values.tolist()
# etf_list = pd.read_csv(INPUT_CSV)[["시퀀스", "종목코드"]].head(30).values.tolist()
# etf_list = pd.read_csv(INPUT_CSV)[["시퀀스", "종목코드"]].iloc[30:].values.tolist()

# 전체 결과 수집
all_results = []

for etf_id, etf_code in etf_list:
    print(f"[⏳] 크롤링 중: ETF_ID={etf_id}, CODE={etf_code}")
    result = crawl_etf_data(etf_id, etf_code)
    all_results.extend(result)

# CSV 저장
df = pd.DataFrame(all_results, columns=["ID", "종목코드", "구성종목명", "주식수", "평가금액", "시가총액", "시가총액기준구성비중"])
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print(f"[✅] 모든 ETF 데이터가 '{OUTPUT_FILE}'에 저장되었습니다!")

driver.quit()
