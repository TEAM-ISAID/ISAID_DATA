import pandas as pd

def clean_column_names(input_file, output_file):
    try:
        # 데이터 읽기
        df = pd.read_csv(input_file, encoding="utf-8-sig")

        # '_file1'로 끝나는 열 제거
        df = df.loc[:, ~df.columns.str.endswith('_file1')]

        # '_file2'로 끝나는 열 이름에서 '_file2' 제거
        df.columns = df.columns.str.replace('_file2$', '', regex=True)

        # 결과 데이터 저장
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"컬럼 정리가 완료된 데이터가 저장되었습니다: {output_file}")
    except Exception as e:
        print(f"오류 발생: {e}")

# 파일 경로 설정
input_file = "ETF_PDF_분류기준/merged_etf_data_cleaned.csv"  # 원본 파일 경로
output_file = "ETF_PDF_분류기준/etf_pdf관련지표(시퀀스있는).csv"  # 결과 파일 경로

clean_column_names(input_file, output_file)