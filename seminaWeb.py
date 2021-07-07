from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime

browser = webdriver.Chrome('c:/Users/HaSangWoo/semina web crawling/chromedriver_win32 (1)/chromedriver.exe')

url = "https://sejong.korea.ac.kr/user/boardList.do?handle=99648&siteId=ioec&id=ioec_060100000000"
root = 'table > tbody >tr'
text = '[특강]'

pd.options.display.max_colwidth = 1000

browser.get(url)

# 페이지 정보 가져오기
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# 번호 제목 작성자 작성일 조회
# 필요정보 : 제목, 링크, 작성일

# 공지사항 게시물정보 전체 추출
# tr 태그 찾기
channel_list = soup.select(root)
# print("tr태그 개수 : "+ str(len(channel_list)))

results = []
for channel in channel_list:
    # 게시물 번호
    number = channel.select('td')[0].text.strip()
    # print("number : "+ number)

    # 게시물 제목
    title = channel.select('td')[1].text.strip()
    # print("title : "+ title)

    # 링크 추출
    href = channel.select('td > a')[0]['href']

    link = 'https://sejong.korea.ac.kr/' + href
    # print("link : "+ link)

    # 작성일자 추출
    date = channel.select('td')[3].text.strip()
    # print(date)

    # print(number, title, link, date)
    data_list = [number, title, link, date]
    results.append(data_list)

df = pd.DataFrame(results)
df.columns = ['Number', 'Title', 'Link', 'Date']

# 오늘 날짜
now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')

# 특정날짜 +  특정 워딩이 모두 고려된 colum 고르기
# 날짜 필터링
find_date = '2021-06-02'
same_date_data = df['Date'] == find_date
same_date_df = df[same_date_data]

# 날짜 필터링된 df에서 특강만 고르기
result = pd.DataFrame()

for i in same_date_df.index:
    if text in same_date_df.loc[i]['Title']:
        result = same_date_df.loc[i]

semina_df = pd.DataFrame(result)
semina_df = semina_df.transpose()
print(semina_df)