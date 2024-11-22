from sqlalchemy import Column, Integer, String, Float, Date, Text
from ..database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)  # 영화 ID
    title = Column(String, nullable=False)  # 영화 제목
    vote_average = Column(Float)  # 평균 평점
    vote_count = Column(Float)  # 평점 수 (소수점 포함)
    status = Column(String)  # 상영 상태
    release_date = Column(Date)  # 개봉일
    revenue = Column(Float)  # 수익
    runtime = Column(Float)  # 상영 시간 (분)
    budget = Column(Float)  # 제작비
    imdb_id = Column(String)  # IMDb ID
    original_language = Column(String)  # 원어
    original_title = Column(String)  # 원제목
    overview = Column(Text)  # 줄거리
    popularity = Column(Float)  # 인기도
    tagline = Column(Text)  # 태그라인
    genres = Column(Text)  # 장르 (쉼표로 구분된 문자열)
    production_companies = Column(Text)  # 제작사 (쉼표로 구분된 문자열)
    production_countries = Column(Text)  # 제작 국가 (쉼표로 구분된 문자열)
    spoken_languages = Column(Text)  # 사용 언어 (쉼표로 구분된 문자열)
    cast = Column(Text)  # 출연진 (쉼표로 구분된 문자열)
    director = Column(String)  # 감독
    director_of_photography = Column(String)  # 촬영 감독
    writers = Column(Text)  # 작가 (쉼표로 구분된 문자열)
    producers = Column(Text)  # 프로듀서 (쉼표로 구분된 문자열)
    music_composer = Column(String)  # 음악 감독
    imdb_rating = Column(Float)  # IMDb 평점
    imdb_votes = Column(Float)  # IMDb 투표 수 (소수점 포함)
    poster_path = Column(String)  # 포스터 경로