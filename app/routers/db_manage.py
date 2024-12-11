from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

router = APIRouter()

# 프로젝트 최상위 경로에 대한 참조
BASE_DIR = Path(__file__).resolve().parents[2]  # 상위 두 단계로 이동하여 최상위 디렉토리 참조
UPLOAD_DIR = BASE_DIR  # 업로드된 파일을 저장할 폴더 지정

# 업로드 폴더가 없으면 생성
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 허용된 파일 확장자
ALLOWED_EXTENSIONS = {".sqlite", ".db"}

def is_allowed_file(filename: str) -> bool:
    """
    파일 이름에서 확장자를 확인하여 허용 여부를 판단.
    """
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """
    SQLite 파일만 업로드 가능하게 설정
    """
    # 파일 확장자 확인
    if not is_allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Only SQLite files are allowed.")
    
    file_path = UPLOAD_DIR / file.filename

    # 파일 저장
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "path": str(file_path)}
