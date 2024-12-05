import pandas as pd
import requests
import time

# TMDB API 키 설정
API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjOTI5NDZjMjE2NmFiMDhkY2UxMGYxM2U1NDhiZjdmMCIsIm5iZiI6MTYzNjgxODIzOC41MTQsInN1YiI6IjYxOGZkZDNlYTMxM2I4MDA4ZjU0MzQyMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1I5yZw5Nfx14FVpvo4N6uMqlAOkTq7-MoFM6fI2T52I'  # 여기에 발급받은 TMDB API 키를 입력하세요.

# CSV 파일 로드
file_path = 'scripts/data/top_100_movies.csv'  # 파일 경로를 지정하세요.
movies = pd.read_csv(file_path)

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}
# 한국어 제목을 가져오는 함수 정의
def get_korean_title(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ko-KR"
    params = {
        'api_key': API_KEY,
        'language': 'ko-KR'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get('title', None)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for movie ID {movie_id}: {e}")
        return None

# '한국어 제목' 컬럼 추가
movies['korean_title'] = movies['id'].apply(get_korean_title)

# TMDB API의 요청 제한을 피하기 위해 0.3초 대기
time.sleep(0.3)

# 결과를 새로운 CSV 파일로 저장
output_file_path = 'scripts/data/top_100_movies_titles.csv'
movies.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"한국어 제목이 추가된 파일이 '{output_file_path}'에 저장되었습니다.")