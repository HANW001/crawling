import math
import requests
from bs4 import BeautifulSoup
import time
# import pyperclip
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

chrome_options = Options()
chrome_options.add_argument('./chromedriver.exe')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu");



d = webdriver.Chrome(ChromeDriverManager().install())
d.maximize_window()
print('login')
# Main_URL = "https://wapam.imweb.me/admin/"

# logins = 'https://tkbb2b.co.kr/product/list.html?cate_no=26'
ss = requests.session()

# URLS = "https://tkbb2b.co.kr/product/list.html?cate_no=26"
# URL = 'https://tkbb2b.co.kr/product/list.html?cate_no=26'


def login(mall_num,username,password):
    login_url = "https://imweb.me/login"
    d.get(login_url)
    time.sleep(1.5)
    # 로그인 폼 작성 및 제출
    d.find_element(By.XPATH, "/html/body/main/io-login-form/io-login-form-container/form/fieldset/io-email-field/input").send_keys(username)
    time.sleep(1)
    d.find_element(By.XPATH, "/html/body/main/io-login-form/io-login-form-container/form/fieldset/io-password-field/input").send_keys(password)
    time.sleep(1)
    d.find_element(By.XPATH, "/html/body/main/io-login-form/io-login-form-container/form/fieldset/io-button/button").click()
    # 로그인 성공 확인 (필요시 수정)
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "log"))
    # )
    time.sleep(1.5)
    print('로그인')

def login2(mall_num,username,password):
    login_url = "https://imweb.me/mysite"
    d.get(login_url)
    urls = d.find_element(By.XPATH, f"/html/body/section/div[1]/div[2]/div/div/div[{mall_num}]/div[4]/a").get_attribute('href')
    time.sleep(0.5)
    d.get(urls)
    time.sleep(0.5)
    # 로그인 폼 작성 및 제출
    d.find_element(By.NAME, "uid").send_keys(username)
    d.find_element(By.NAME, "passwd").send_keys(password)
    d.find_element(By.XPATH, "/html/body/section/div/div/form/div/button").click()
    
    # 로그인 성공 확인 (필요시 수정)
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "log"))
    # )
    time.sleep(0.25)
    print('로그인')


def category_id(URLS):
  
  upload_folder = r"C:\Users\mosad\Desktop\github\crawling\아임웹_리뷰\reviews"
  
  d.get(URLS)
  files = [os.path.join(upload_folder, f) for f in os.listdir(upload_folder) if f.endswith('.xlsx')]
  print(len(files))
  time.sleep(0.25)
  
#   element = d.find_element(By.XPATH, "/html/body/div[2]/header[1]/div/div[2]/ul/scs-partials/main//div[1]/a[2]/div")
#   element.click()
  time.sleep(3.25)
  failed_files = []
  # 파일별 업로드 시도
  user_input = input("파일을 업로드하시겠습니까? (y 입력 시 실행): ")

  if user_input.lower() == "y":
    for file in files:
        max_retries = 3  # 최대 재시도 횟수
        attempt = 0  # 현재 시도 횟수
        
        while attempt < max_retries:
            try:
                file_input = d.find_element(By.CSS_SELECTOR, '#prod_multi_add_upload > input[type=file]')
                time.sleep(1)
                file_input.send_keys(file)  # 파일 업로드
                print(f"✅ {file} 업로드 완료")
                time.sleep(3)  # 업로드 후 대기
                break  # 성공하면 반복문 탈출
            except Exception as e:
                attempt += 1
                print(f"⚠️ {file} 업로드 실패 (시도 {attempt}/{max_retries}): {e}")
                time.sleep(2)  # 재시도 전 대기
                
                if attempt == max_retries:
                    print(f"❌ {file} 업로드 실패 (최대 재시도 초과)")
                    failed_files.append(file)  # 실패한 파일 저장

  # 크롬 종료
  d.quit()

  # 실패한 파일 목록을 엑셀로 저장
  if failed_files:
      failed_df = pd.DataFrame({"Failed Files": failed_files})
      failed_df.to_excel("failed_uploads.xlsx", index=False)
      print("📂 실패한 파일 목록이 'failed_uploads.xlsx'로 저장되었습니다.")
  else:
      print("🎉 모든 파일이 정상적으로 업로드되었습니다!")
  





def get_darem(mall_num,username,password,URLS):
  # if i == 1:
  login(mall_num,username,password)
  login2(mall_num,username,password)
  datas = category_id(URLS)
  # print(category_page)
  return datas