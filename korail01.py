#코레일 사이트 자동로그인 후 열차예매 페이지까지 진입
from idlelib import browser
from telnetlib import EC

from bs4 import BeautifulSoup
import requests
import time
import datetime
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from click._unicodefun import click
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import wait
from selenium.webdriver.support.select import Select

#시작 전 주의사항: 내 예약내역에 예약하려는 티켓과 동일한 예약대기내역이 없어야 함
KORAIL_ID = '아이디'
KORAIL_PW = '비밀번호'

People_count = '어른 4명'
#인원수:_어른 n명 형식으로 따옴표 안에 넣을 것

TODAY_DEPARTURE = str('용산')
TODAY_ARRIVAL = str('익산')

year = int(2020)
month =int(3)
day = int(15)
hour = str('12:15')

yoil = str('일')

#t = ['월', '화', '수', '목', '금', '토', '일']
#date01 = input( year , month , day)
#r = datetime.datetime(date01).weekday()
#print(t[r])


#0~23


url1 = 'https://www.letskorail.com/korail/com/login.do'  #로그인 페이지
url2 = 'http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do'
# url2 = 'https://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do'  #열차예매 페이지

driver = webdriver.Chrome(
     executable_path = r'/Users/구일문/Downloads/chromedriver_win32/chromedriver.exe')

#브라우져 화면 크기 조정
# driver.set_window_size(1280, 720)    #HD 사이즈로 변경
# driver.set_window_size(1920, 1080)    #FHD 사이즈로 변경
driver.maximize_window()   #전체화면 크기로 변경

driver.get(url1)

#웹 페이지 로딩이 다 끝날때까지 잠시 대기
time.sleep(1)

#로그인 폼에 아이디/비밀번호 입력
userid = driver.find_element_by_id('txtMember')
userid.send_keys(KORAIL_ID)
#time.sleep(1)

userpw = driver.find_element_by_id('txtPwd')
userpw.send_keys(KORAIL_PW)
#time.sleep(1)

#로그인 버튼이 이미지에 a 태그 형태로 작성되어 있음
#따라서, 버튼명.submit() 은 사용할 수 없음
loginbtn = driver.find_element_by_css_selector('img[alt="확인"]')

mouse = webdriver.ActionChains(driver)
mouse.move_to_element(loginbtn).click().perform()

time.sleep(3)
driver.switch_to.window(driver.window_handles[1]) # 최신 팝업창으로 이동
driver.find_element_by_xpath("//span[@class = 'rig']").click()
driver.switch_to.window(driver.window_handles[0]) # 원래 창으로 복귀


#예매시작
driver.get(url2)

driver.find_element_by_name('txtPsgFlg_1').send_keys(People_count)

driver.find_element_by_name('txtGoStart').clear()
driver.find_element_by_name('txtGoStart').send_keys(TODAY_DEPARTURE)
driver.find_element_by_name('txtGoEnd').clear()
driver.find_element_by_name('txtGoEnd').send_keys(TODAY_ARRIVAL)

driver.find_element_by_name('selGoYear').send_keys(year)
driver.find_element_by_name('selGoMonth').send_keys(month)


driver.find_element_by_name('selGoYear').send_keys(year)
driver.find_element_by_name('selGoMonth').send_keys(month)
driver.find_element_by_name('selGoDay').send_keys(day)
driver.find_element_by_name('selGoHour').send_keys(hour)

driver.find_element_by_xpath("//img[@src= '/images/btn_inq_tick.gif']").click()

success = 0 # 취소표 예매 성공 여부 표현
s_time = hour # 출발 시각
while success == 0: # 취소표 예매 성공 못 한 경우 계속 반복
    time_find = 0 # 출발 시각 찾기 성공 여부 표현
    for i in range(1,10): # 첫번째 줄부터 열번째 줄까지 탐색
        time.sleep(1)
        depart = driver.find_element_by_xpath('//tbody/tr[{}]/td[3]'.format(i)).text.split('\n')[1]
        ym = driver.find_element_by_xpath('//tbody/tr[{}]/td[6]//img'.format(i)).get_attribute('alt') # 일반실 조회
        if depart == s_time: # 출발 시각 일치하는 경우
            if ym == '예약하기': # 예약 가능한 경우
                print('기차표가 예매되었습니다')
                success = 1
                driver.find_element_by_xpath('//tbody/tr[{}]/td[6]//img'.format(i)).click() # 예매 클릭
            else:
                driver.find_element_by_xpath("//img[@alt='조회하기']").click() # 조회하기 클릭
                print('아직 자리가 없습니다')
            time_find = 1
        if time_find == 1:
            break
