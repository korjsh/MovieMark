from sqlalchemy.orm import Session
from app.models.movie import Movie
from typing import List
import pandas as pd

def search_movies_by_name(db: Session, keyword: str):
    return db.query(Movie).filter(Movie.movie_nm.like(f"%{keyword}%")).all()

def create_movies_from_csv(db: Session, df: pd.DataFrame):
    movies_to_add = []
    for index, row in df.iterrows():
        # 결측치 처리
        row = row.fillna('')

        # MovieInfo 객체 생성
        movie = Movie(
            no=int(row['NO']),
            movie_nm=row['MOVIE_NM'],
            drctr_nm=row['DRCTR_NM'] if row['DRCTR_NM'] else None,
            makr_nm=row['MAKR_NM'] if row['MAKR_NM'] else None,
            incme_cmpny_nm=row['INCME_CMPNY_NM'] if row['INCME_CMPNY_NM'] else None,
            distb_cmpny_nm=row['DISTB_CMPNY_NM'] if row['DISTB_CMPNY_NM'] else None,
            opn_de=row['OPN_DE'] if row['OPN_DE'] else None,
            movie_ty_nm=row['MOVIE_TY_NM'] if row['MOVIE_TY_NM'] else None,
            movie_stle_nm=row['MOVIE_STLE_NM'] if row['MOVIE_STLE_NM'] else None,
            nlty_nm=row['NLTY_NM'] if row['NLTY_NM'] else None,
            tot_scrn_co=float(row['TOT_SCRN_CO']) if row['TOT_SCRN_CO'] else None,
            sales_price=float(row['SALES_PRICE']) if row['SALES_PRICE'] else None,
            viewng_nmpr_co=float(row['VIEWNG_NMPR_CO']) if row['VIEWNG_NMPR_CO'] else None,
            seoul_sales_price=float(row['SEOUL_SALES_PRICE']) if row['SEOUL_SALES_PRICE'] else None,
            seoul_viewng_nmpr_co=float(row['SEOUL_VIEWNG_NMPR_CO']) if row['SEOUL_VIEWNG_NMPR_CO'] else None,
            genre_nm=row['GENRE_NM'] if row['GENRE_NM'] else None,
            grad_nm=row['GRAD_NM'] if row['GRAD_NM'] else None,
            movie_sdiv_nm=row['MOVIE_SDIV_NM'] if row['MOVIE_SDIV_NM'] else None,
        )
        movies_to_add.append(movie)

    # 데이터베이스에 추가
    db.bulk_save_objects(movies_to_add)
    db.commit()

    return len(movies_to_add)
