import pandas as pd

# CSV 파일 경로 설정
etf_path = "ETF_pdf.csv"
risk_path = "etf_risk.csv"
output_path = "ETF.csv"

# CSV 파일 불러오기
etf_df = pd.read_csv(etf_path)
risk_df = pd.read_csv(risk_path, encoding='cp949')

# 필요 컬럼만 추출 (펀드번호와 위험등급)
risk_df = risk_df[['펀드번호', '위험등급']]

# "1등급" → 1로 숫자만 추출
risk_df['위험등급'] = risk_df['위험등급'].str.extract(r'(\d)').astype('Int64')  # 숫자가 없는 경우도 안전하게 처리

# 표준코드(ETF.csv) <-> 펀드번호(위험분류.csv) 기준으로 병합
merged_df = pd.merge(etf_df, risk_df, left_on='표준코드', right_on='펀드번호', how='left')

# 펀드번호, 기초지수명 컬럼제거
merged_df.drop(columns=['펀드번호'], inplace=True)
merged_df.drop(columns=['기초지수명'], inplace=True)

# 결과를 새로운 CSV로 저장
merged_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"완료: {output_path}로 저장됨")
