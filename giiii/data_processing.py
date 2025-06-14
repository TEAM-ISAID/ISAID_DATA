import pandas as pd
import os

# 전체 ETF 데이터 불러오기
etf_df = pd.read_csv('날짜별_ETF_정보/20250529.csv', encoding='cp949')

# 종목코드를 문자열
etf_df['ISU_CD'] = etf_df['ISU_CD'].astype(str).str.zfill(6)

# 운용사 종목코드 폴더 경로
folder_path = '혼합자산/'

# 결과 저장 경로
output_folder = '20250529'
os.makedirs(output_folder, exist_ok=True)

# 폴더 내 모든 파일 반복
for filename in os.listdir(folder_path):
    if not filename.endswith(('.txt', '.csv')):
        continue

    file_path = os.path.join(folder_path, filename)

    # 종목코드 파일 읽기
    try:
        if filename.endswith('.csv'):
            code_df = pd.read_csv(file_path, encoding='euc-kr')
        else:
            code_df = pd.read_csv(file_path, header=None, names=['종목코드'], encoding='euc-kr')

        # 종목코드 전처리
        code_df['종목코드'] = code_df['종목코드'].astype(str).str.zfill(6)
        filtered_df = etf_df[etf_df['ISU_CD'].isin(code_df['종목코드'])]

        # 운용사명 추출
        company_name = os.path.splitext(filename)[0]

        # 결과 저장
        output_path = os.path.join(output_folder, f"20250529_{company_name}.csv")
        filtered_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"{company_name} → {len(filtered_df)}건 저장 완료")

    except Exception as e:
        print(f"{filename} 처리 중 오류 발생: {e}")