import pandas as pd

# 원본 CSV 파일 경로
input_file = "ETF_pdf.csv"
# 필터링된 ETF 저장 경로
output_file = "1q_etf_sorted.csv"

# CSV 파일 읽기
df = pd.read_csv(input_file)

# '종목명' 기준 내림차순 정렬
df_sorted = df.sort_values(by="종목명", ascending=False)

# 'TIGER'가 종목명에 포함된 행 필터링
df_tiger = df_sorted[df_sorted["종목명"].str.contains("1Q", case=False, na=False)]

# 결과 저장
df_tiger.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"{output_file} 파일로 저장 완료")
