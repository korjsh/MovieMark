import pandas as pd

# CSV 파일 로드
file_path = "scripts/data/TMDB_all_movies.csv"  # 파일 경로를 지정합니다.
movies = pd.read_csv(file_path)

# 유명한 영화를 선정하기 위해 vote_count와 vote_average 기준으로 정렬
movies['popularity_score'] = movies['vote_average'] * movies['vote_count']  # 가중치를 기준으로 점수 계산
top_movies = movies.sort_values(by='popularity_score', ascending=False).head(100)  # 상위 100개 추출

# 결과를 CSV로 저장 (모든 열 포함)
output_file_path = 'top_100_movies_with_all_columns.csv'
top_movies.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"유명한 영화 100편이 모든 열과 함께 '{output_file_path}' 파일로 저장되었습니다.")