import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('movie.csv', encoding='utf-8', header=None, na_filter=False)

# 모든 컬럼이 빈 값인 행을 찾아서 제거
# 첫 번째 컬럼(인덱스)은 제외하고 검사합니다.
def is_row_empty(row):
    return row.iloc[1:].str.strip().eq('').all()

# 모든 컬럼이 빈 값인 행을 제거한 새로운 데이터프레임 생성
df_cleaned = df[~df.apply(is_row_empty, axis=1)]

# 정제된 데이터프레임을 새로운 CSV 파일로 저장
df_cleaned.to_csv('movies_cleaned.csv', index=False, header=False, encoding='utf-8')
