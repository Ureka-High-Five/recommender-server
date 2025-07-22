_genre_mapping = {
    "공포": "Horror",
    "Horror": "Horror",
    "액션": "Action",
    "Action": "Action",
    "스릴러": "Thriller",
    "Thriller": "Thriller",
    "미스터리": "Mystery",
    "Mystery": "Mystery",
    "가족": "Family",
    "Family": "Family",
    "코미디": "Comedy",
    "Comedy": "Comedy",
    "애니메이션": "Animation",
    "Animation": "Animation",
    "SF": "SF",
    "다큐멘터리": "Documentary",
    "Documentary": "Documentary",
    "판타지": "Fantasy",
    "Fantasy": "Fantasy",
    "드라마": "Drama",
    "Drama": "Drama",
    "모험": "Adventure",
    "Adventure": "Adventure",
    "로맨스": "Romance",
    "Romance": "Romance",
    "범죄": "Crime",
    "Crime": "Crime",
    "역사": "History",
    "History": "History",
    "음악": "Music",
    "Music": "Music",
    "전쟁": "War",
    "War": "War",
    "Action & Adventure": "Adventure",
    "Sci-Fi & Fantasy": "Fantasy",
    "Kids": "Children",
    "Children": "Children",
    "War & Politics": "War",
    "Talk": "Talkshow",
    "Talkshow": "Talkshow"
}


def translate_genre(korean_genre: str) -> str:
    return _genre_mapping.get(
        korean_genre, "장르가 아닌 metadata는 건너뜁니다"
    )  # 매핑 없을 경우
