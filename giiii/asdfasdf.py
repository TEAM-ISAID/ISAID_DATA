import os
import pandas as pd


def process_etf_files_with_codes(input_folder, codes_folder):
    # 날짜별 ETF 정보 폴더 내 파일 확인
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    for file in all_files:
        try:
            # 파일 경로 및 날짜명 추출
            file_path = os.path.join(input_folder, file)
            date_name = os.path.splitext(file)[0]

            # # 날짜명으로 폴더 생성
            # output_folder = os.path.join(input_folder, date_name)
            # os.makedirs(output_folder, exist_ok=True

            # CSV 읽기 (ETF 데이터)
            etf_df = pd.read_csv(file_path, encoding='utf-8-sig')

            # 종목코드를 문자열로 변환
            etf_df['ISU_CD'] = etf_df['ISU_CD'].astype(str).str.zfill(6)

            # 운용사 종목코드 폴더 내 파일 처리
            for code_file in os.listdir(codes_folder):
                if not code_file.endswith(('.txt', '.csv')):
                    continue

                code_file_path = os.path.join(codes_folder, code_file)

                try:
                    # 종목코드 파일 읽기
                    if code_file.endswith('.csv'):
                        code_df = pd.read_csv(code_file_path, encoding='utf-8-sig')
                    else:  # .txt 파일의 경우 처리
                        code_df = pd.read_csv(code_file_path, header=None, names=['종목코드'], encoding='utf-8-sig')

                    # 종목코드를 문자열로 변환 및 필터링
                    code_df['종목코드'] = code_df['종목코드'].astype(str).str.zfill(6)
                    filtered_df = etf_df[etf_df['ISU_CD'].isin(code_df['종목코드'])]

                    # 운용사명을 파일명에서 추출
                    company_name = os.path.splitext(code_file)[0]

                    # 결과 저장 경로
                    output_file = os.path.join(f"{date_name}_{company_name}.csv")
                    filtered_df.to_csv(output_file, index=False, encoding='utf-8-sig')

                    print(f"{date_name} - {company_name}: {len(filtered_df)}개 저장 완료")

                except Exception as e:
                    print(f"{code_file} 처리 중 오류 발생: {e}")

        except Exception as e:
            print(f"{file} 처리 중 오류 발생: {e}")


# 실행 경로 지정
input_folder = "신규"  # 날짜별 파일 저장된 폴더
codes_folder = "카테고리"  # 종목코드 파일 폴더

# 함수 실행
process_etf_files_with_codes(input_folder, codes_folder)
