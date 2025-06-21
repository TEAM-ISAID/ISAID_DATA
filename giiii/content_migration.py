import pandas as pd

def merge_etf_data(file1, file2, output_file):
    def safe_read_csv(filepath, encodings=('utf-8', 'euc-kr', 'cp949')):
        for encoding in encodings:
            try:
                return pd.read_csv(filepath, encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"파일 {filepath}를 지원하는 인코딩으로 읽을 수 없습니다.")

    try:
        # 데이터 파일 읽기
        df1 = safe_read_csv(file1)
        df2 = safe_read_csv(file2)

        # 종목코드를 문자열로 변환 및 정렬
        df1['종목코드'] = df1['종목코드'].astype(str).str.zfill(6)
        df2['종목코드'] = df2['종목코드'].astype(str).str.zfill(6)

        # 두 데이터를 종목코드를 기준으로 병합
        merged_df = pd.merge(df1, df2, on='종목코드', how='outer', suffixes=('_file1', '_file2'))

        # 중복 열 제거 (같은 data가 다른 열명으로 존재할 경우 우선순위 정리)
        merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

        # 결과 CSV로 저장
        merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"병합 완료: {output_file}")
    except Exception as e:
        print(f"병합 과정에서 오류 발생: {e}")

# 파일 경로 설정
file1 = "ETF_PDF_분류기준/ETF_상세정보.csv"  # 예: 종목코드 있음
file2 = "ETF_PDF_분류기준/전종목기본정보.csv"  # 예: 표준코드 및 전체정보 포함
output_file = "ETF_PDF_분류기준/merged_etf_data.csv"

merge_etf_data(file1, file2, output_file)