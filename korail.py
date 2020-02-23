#코레일 사이트 자동로그인 후 열차예매 페이지까지 진입
from telnetlib import EC

from bs4 import BeautifulSoup
import requests
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import wait
from selenium.webdriver.support.select import Select

KORAIL_ID = '1469169741'
KORAIL_PW = 'dlfans1564!'

TODAY_DEPARTURE = '서울'
TODAY_ARRIVAL = '익산'

LEAVING_DATE ='2020.2.23'
#2020.2.20 형식으로

LEAVING_TIME ='22'
#0~23


url1 = 'https://www.letskorail.com/korail/com/login.do'  #로그인 페이지
url2 = 'http://www.letskorail.com/index.jsp'
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

#time.sleep(3)

#자바스크립트 경고창 처리
#Alert(driver).dismiss()


#time.sleep(3)

#운송약관 윈도우 자동 닫기 (2018.06.21 기준)
main_window = driver.current_window_handle
#현재 윈도우 객체를 변수에 저장

handles = list(driver.window_handles)
#윈도우들의 객체를 알아냄 - handles 변수에 저장

driver.switch_to.window(driver.window_handles[-1])
#브라우져 위에 뜬 윈도우로 제어 이동
driver.close()     #윈도우 닫기

driver.switch_to.window(main_window)
#이전 윈도우로 제어를 넘김


# 열차 예매 페이지로 이동 - 승차권예매 버튼 클릭후 이동
driver.get(url2)

driver.find_element_by_name('txtGoStart').clear()
driver.find_element_by_name('txtGoStart').send_keys(TODAY_DEPARTURE)
#time.sleep(1)


driver.find_element_by_name('txtGoEnd').clear()
driver.find_element_by_name('txtGoEnd').send_keys(TODAY_ARRIVAL)


driver.find_element_by_id('selGoStartDay').clear()
driver.find_element_by_id('selGoStartDay').send_keys(LEAVING_DATE)


driver.find_element_by_id('time').send_keys(LEAVING_TIME)


date_select01 = wait.until(EC.element_to_be_clickable((By.selt147, 'people_num')))
date_select01.click()
select = Select(driver.find_element_by_id('selt147'))
select.select_by_visible_text('어른 2명')




driver.find_element_by_xpath("//img[@src='/images/btn_reserve.gif").click()

#people_num


