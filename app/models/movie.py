from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from ..database import Base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movie_info"

    no = Column(Integer, primary_key=True, index=True)  # NO
    movie_nm = Column(String, index=True)  # 영화 제목
    drctr_nm = Column(String)  # 감독 이름
    makr_nm = Column(String)  # 제작사 이름
    incme_cmpny_nm = Column(String)  # 수입사 이름
    distb_cmpny_nm = Column(String)  # 배급사 이름
    opn_de = Column(String)  # 개봉일 (날짜 형식이 불완전하여 String으로 처리)
    movie_ty_nm = Column(String)  # 영화 유형
    movie_stle_nm = Column(String)  # 영화 스타일
    nlty_nm = Column(String)  # 국가명
    tot_scrn_co = Column(Float)  # 총 스크린 수
    sales_price = Column(Float)  # 매출액
    viewng_nmpr_co = Column(Float)  # 관객 수
    seoul_sales_price = Column(Float)  # 서울 매출액
    seoul_viewng_nmpr_co = Column(Float)  # 서울 관객 수
    genre_nm = Column(String)  # 장르명
    grad_nm = Column(String)  # 등급명
    movie_sdiv_nm = Column(String)  # 영화 세부 구분명
