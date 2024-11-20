import pandas as pd
import os
import glob

# Directory containing the files
directory = "/Users/korjsh/Downloads"  # Modify to your folder path

# File pattern to match
file_pattern = os.path.join(directory, "KC_KOBIS_BOX_OFFIC_MOVIE_INFO_*.csv")

# Collect all files matching the pattern
file_list = glob.glob(file_pattern)

# excluded_companies = [
#     "(주)영진크리에이티브", "P&미디어", "(주)디에이치미디어",
#     "(주)영화사가을", "(주)컨텐츠 빌리지", "(주)온비즈넷", "(주)로드하우스",
#     "스마일컨텐츠", "주식회사 플릭스코", "주식회사 미콘", "에이원 미디어", "케이엘 픽쳐스",
#     "(주)라온컴퍼니플러스", "(주)가온콘텐츠", "(주)영화사히트", "선셋 시네마", "(주)픽쳐레스크",
#     "(주)씨맥스커뮤니케이션즈", "(주)코빈커뮤니케이션즈", "(주)로드하우스", "(주)디어프로덕션",
#     "(주)이십일세기미디어", "노바엔터테인먼트", "(주)룬컴퍼니", "(주)메이크아트", "(주)케이알씨지",
#     "(주)박수엔터테인먼트", "스마일픽쳐스", "(주)레드언더미디어", "(주)소나무픽쳐스", "주식회사 제이씨엔터웍스",
#     "(주)나우콘텐츠", "두리컴", "(주)트리필름", "제뉴어리이공 현프로"
# ]

# Combine all files
combined_data = pd.DataFrame()
for file in file_list:
    data = pd.read_csv(file)
    # Remove rows where GENRE_NM is "성인물(에로)" or GRAD_NM is "청소년 관람불가"
    data = data[
        (data['GENRE_NM'] != "성인물(에로)") &
        (data['GRAD_NM'] != "청소년관람불가")
    ]
    combined_data = pd.concat([combined_data, data], ignore_index=True)

# Ensure unique NO column
combined_data['NO'] = range(1, len(combined_data) + 1)

# Save the combined file
output_file = os.path.join(directory, "Filtered_Combined_Movie_Info.csv")
combined_data.to_csv(output_file, index=False)

print(f"Filtered data has been combined and saved to: {output_file}")

