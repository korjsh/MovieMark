# app/schemas/movie.py

from pydantic import BaseModel
from typing import Optional

class MovieInfoSchema(BaseModel):
    no: int
    movie_nm: str
    drctr_nm: Optional[str] = None
    makr_nm: Optional[str] = None
    incme_cmpny_nm: Optional[str] = None
    distb_cmpny_nm: Optional[str] = None
    opn_de: Optional[str] = None
    movie_ty_nm: Optional[str] = None
    movie_stle_nm: Optional[str] = None
    nlty_nm: Optional[str] = None
    tot_scrn_co: Optional[float] = None
    sales_price: Optional[float] = None
    viewng_nmpr_co: Optional[float] = None
    seoul_sales_price: Optional[float] = None
    seoul_viewng_nmpr_co: Optional[float] = None
    genre_nm: Optional[str] = None
    grad_nm: Optional[str] = None
    movie_sdiv_nm: Optional[str] = None

    class Config:
        orm_mode = True
