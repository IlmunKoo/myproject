import requests
from bs4 import BeautifulSoup

# URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190909',headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

# select를 이용해서, tr들을 불러오기
movies = soup.select('#assistant > div:nth-child(1) > ul ')
#assistant > div:nth-child(1) > ul > li.ranking01 > a


# movies (tr들) 의 반복문을 돌리기
i = 0
for movie in movies:

    print(i)
    # movie 안에 a 가 있으면,
    a_tag = movie.select_one('li')


    print(a_tag.text)



