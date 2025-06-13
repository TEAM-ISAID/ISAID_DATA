import pandas as pd
import os

def merge_csv_from_folder(folder_path, output_file):
    # 폴더 내 모든 파일 불러오기
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]

    # 빈 리스트 준비
    dataframes = []

    # 각 파일 읽어서 데이터프레임에 저장
    for file in all_files:
        try:
            df = pd.read_csv(file, encoding='cp949')
            dataframes.append(df)
            print(f"파일 처리 완료: {file}")
        except Exception as e:
            print(f"오류 발생 (파일: {file}): {e}")

    # 데이터프레임 병합
    combined_df = pd.concat(dataframes, ignore_index=True)

    # 통합 데이터 CSV 저장
    combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"병합 완료, 저장 파일명: {output_file}")

folder_path = "카테고리"
output_file = "카테고리/ETF_CATEGORY.csv"

merge_csv_from_folder(folder_path, output_file)