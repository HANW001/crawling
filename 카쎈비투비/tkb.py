import math
import requests
from bs4 import BeautifulSoup
import time
import pyperclip

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
chrome_options.add_argument("--disable-gpu")

d = webdriver.Chrome(ChromeDriverManager().install())

print('login')
Main_URL = "https://tikerbell.co.kr/"

# logins = 'https://tkbb2b.co.kr/product/list.html?cate_no=26'
ss = requests.session()

# URLS = "https://tkbb2b.co.kr/product/list.html?cate_no=26"
# URL = 'https://tkbb2b.co.kr/product/list.html?cate_no=26'
username = ''
password = ''

def login():
    login_url = "https://carssenb2b.com/member/login.html"
    d.get(login_url)
    time.sleep(0.5)
    # 로그인 폼 작성 및 제출
    d.find_element(By.NAME, "member_id").send_keys(username)
    d.find_element(By.NAME, "member_passwd").send_keys(password)
    d.find_element(By.XPATH, "/html/body/div[4]/div/div/form/div/div/fieldset/a").click()
    
    # 로그인 성공 확인 (필요시 수정)
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "log"))
    # )
    time.sleep(0.25)
    print('로그인')


def category_id(URLS):
  d.get(URLS)
  id_list = []
  result = ss.get(URLS,headers={'User-Agent': 'Mozilla/5.0'})
  soup = BeautifulSoup(result.text, "html.parser")
  try:
    pages = soup.find('a',{'class':'last'})['href'].split('page=')[1]
  except:
    page = soup.find('div',{'class':'xans-element- xans-product xans-product-normalpaging ec-base-paginate'}).find('ol').find_all('li')
    print(page)
    pages = len(page)

  print(pages)
  max_page = pages
#  https://darem.co.kr/goods/goods_view.php?goodsNo=1000001060
# https://darem.co.kr/goods/goods_view.php?goodsNo=1000001246%27,
# /html/body/div[4]/div/div/div[3]/ul
# /html/body/div[4]/div/div/div[3]/ul/li[1]/div[1]/a
# /html/body/div[4]/div/div/div[3]/ul/li[2]/div[1]/a
# /html/body/div[4]/div/div/div[3]/ul/li[3]/div[1]/a

# /html/body/div[4]/div/div/div[3]/ul/li[6]/div[1]/a
# /html/body/div[4]/div/div/div[3]/ul/li[8]/div[1]/a
# 
  for i in range(int(max_page)):
    hrefs = []
    Category_URL = URLS+f'&page={i+1}'
    print(Category_URL)
    d.get(Category_URL)
    # result = ss.get(Category_URL,headers={'User-Agent': 'Mozilla/5.0'})
    # soup = BeautifulSoup(result.text, "html.parser")
    items = d.find_elements(By.CSS_SELECTOR,'#contents > div.xans-element-.xans-product.xans-product-normalpackage > div.xans-element-.xans-product.xans-product-listnormal.ec-base-product.normal > ul > li')
    lens = len(items)
    print(lens)
    

    for li in items:
      a_tag = li.find_element(By.TAG_NAME, "a")  # li 내부 a 태그 찾기
      hrefs.append(a_tag.get_attribute("href"))  # href 속성 가져오기
    print(len(hrefs))
  
    for href in hrefs:
        datas = category_item(href)
        id_list.append(datas)
    
         
      
  return id_list

def category_item(href):
      Item_URL = href
      print(Item_URL)
      d.get(Item_URL)
    # try:
      result = ss.get(Item_URL,headers={'User-Agent': 'Mozilla/5.0'})
      soup = BeautifulSoup(result.text, "html.parser")
      info_soup = soup.find('div',{'class':'hb_detail_info_top'})
      title = d.find_element(By.CSS_SELECTOR,'#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.buy-wrapper > div.buy-scroll-box > h2').text
      # titles = titles.split('.')[1]
      # title = titles.replace(' ','').replace('★공용★','').replace('/',' ')
      # title = titles.replace('= ','')
      # print(title)
      # pd_num = d.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[3]/div[1]/table/tbody/tr[7]/td/span').text
      # print(pd_num)
      try:
        thum_imgs = d.find_element(By.CSS_SELECTOR,'#contents > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.keyImg.item > div.thumbnail > a > img')
        thum_img = thum_imgs.get_attribute('src')
      except:
         thum_img = title
      print(thum_img)
      

      # 
      center_element = d.find_element(By.CSS_SELECTOR,'#prdDetail > div.cont > center')
      img_elements = center_element.find_elements(By.TAG_NAME, "img")
      detail_description = "".join(
          img.get_attribute("outerHTML") for i, img in enumerate(img_elements))
      # detail_imgss = str(detail_imgs)
      # print('1')
      # if detail_imgss == '<div align="center"><br/><br/></div>':
      #    detail_imgs = soup.select_one("div[align='center']:nth-of-type(2)")
      #    detail_imgss = str(detail_imgs)

      # elif detail_imgss == 'None':
      #       print('2')
      #       detail_imgs = soup.find("p", style="text-align: center")
      #       detail_imgss = str(detail_imgs)

      #       if detail_imgss == 'None':
      #         print('3')
      #         detail_imgs = soup.find("div", style="text-align: center")
      #         detail_imgss = str(detail_imgs)
            
      # print(detail_imgss)
      # detail_imgs = []
      # for d_img in detail_img:
        # detail_imgx=d_img.get('src').replace("//","")
        # detail_imgs.append(detail_imgx)
      #   detail_imgs.append(d_img)
      # detail_imgss = str(detail_imgs).replace('[',"").replace(']','').replace(',','')
      # print(detail_imgss)
      # # # detail_imgss =detail_imgss.replace('[',"").replace(']','')
      # d.find_element('xpath','/html/body/div/section/div/div[1]/div[3]/ul/li[3]/ul/li[2]/div[2]/button').click()
      try:
        price =d.find_element(By.XPATH,'/html/body/div[4]/div/div/div[2]/div[2]/div[3]/div[2]/div[3]/div[1]/table/tbody/tr[4]/td/span/span/span').text
        price = price.split(' (')[0]
        price =price.replace(',','').replace('원','')
      except:
        print('여기')
        # price =d.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[3]/div[1]/table/tbody/tr[2]/td/span/strong').text
        print('price')
        # price =price.replace(',','').replace('원','')
      # print(price)
      price2 = int(price)*1.8
      price3 = int(price)*2
      
      # option = d.find_element(By.XPATH,'/html/body/table/tbody/tr/td/table[4]/tbody/tr/td/form/table[1]/tbody/tr/td[2]/div[4]/table[4]/tbody/tr/td[2]/div/div/div[1]').text
      # option = option.replace(' ','')
      # if option.endswith('|'):  # 마지막 문자가 '|'인지 확인
      #     option = option[:-1]  # 마지막 문자 제거
      # else:
      #     option = option
      # try:
      #   print('hi1')
      #   d.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/table[2]/tbody[2]/tr/td/select').click()
      #   time.sleep(0.3)
      #   print('hi')
      #   options = soup.find("select",{"name":"option1"}).find_all('option')
  
      #   for i in range(2,len(options)):
      #     if i == 2:
      #       option = options[i].text
      #     else:
      #       option +="|{}".format(options[i].text)
      # except:
      #   option = title
      ops ='{'+'단일옵션}'
      # print(option)
     
      return {
        '상품코드':'','자체 상품코드':'','진열상태':'Y','판매상태':"Y",'상품분류 번호':"",'상품분류 신상품영역':'',
        '상품분류 추천상품영역':'',
        '상품명':title,
        '영문 상품명':'','상품명(관리용)':'','공급사 상품명':'','모델명':'','상품 요약설명':'','상품 간략설명':'',
        '상품 상세설명':f'<center>{detail_description}</center>',
        '모바일 상품 상세설명 설정':'',
        '모바일 상품 상세설명':detail_description,
        '검색어설정':'','과세구분':'','소비자가':'',
        '공급가':price,
        '상품가':'',
        '판매가':price2,
        '판매가 대체문구 사용':'','판매가 대체문구':'','주문수량 제한 기준':'','최소 주문수량(이상)':'','최대 주문수량(이하)':'',
        '적립금':'','적립금 구분':'','공통이벤트 정보':'','성인인증':'N','옵션사용':'Y','품목 구성방식':'T','옵션 표시방식':'S',
        '옵션세트명':'',
        '옵션입력':'옵션'+ops,
        '옵션 스타일':'','버튼이미지 설정':'','색상 설정':'','필수여부':'','품절표시 문구':'','추가입력옵션':'','추가입력옵션 명칭':'',
        '추가입력옵션 선택/필수여부':'','입력글자수(자)':'',
        '이미지등록(상세)':thum_img,
        '이미지등록(목록)':thum_img,
        '이미지등록(작은목록)':thum_img,
        '이미지등록(축소)':thum_img,
        '이미지등록(추가)':'','제조사':'','공급사':'','브랜드':'','트렌드':'','자체분류 코드':'','제조일자':'','출시일자':'',
        '유효기간 사용여부':'','유효기간':'','원산지':'','상품부피(cm)':'','상품결제안내':'','상품배송안내':'','교환/반품안내':'',
        '서비스문의/안내':'','배송정보':'','배송방법':'','국내/해외배송':'','배송지역':'','배송비 선결제 설정':'','배송기간':'',
        '배송비 구분':'','배송비입력':'','스토어픽업 설정':'','상품 전체중량(kg)':'','HS코드':'','상품 구분(해외통관)':'','상품소재':'',
        '영문 상품소재(해외통관)':'','옷감(해외통관)':'','검색엔진최적화(SEO) 검색엔진 노출 설정':'','검색엔진최적화(SEO) Title':'',
        '검색엔진최적화(SEO) Author':'','검색엔진최적화(SEO) Description':'','검색엔진최적화(SEO) Keywords':'',
        '검색엔진최적화(SEO) 상품 이미지 Alt 텍스트':'','개별결제수단설정':'','상품배송유형 코드':'','메모':''
        # 필요한 다른 필드들 추가
    }
    # except:
    #   print('pass')
    #   pass



def get_darem(URLS,i):
  if i == 0:
     login()
  datas = category_id(URLS)
  # print(category_page)
  return datas