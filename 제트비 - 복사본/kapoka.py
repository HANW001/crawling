import requests
import re
# from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 세션 생성
session = requests.Session()

# 로그인 함수
def login(username, password):
    login_url = "https://dmteckb2b.com/member/login.html"
    driver.get(login_url)
    time.sleep(0.5)
    # 로그인 폼 작성 및 제출
    driver.find_element(By.NAME, "member_id").send_keys(username)
    driver.find_element(By.NAME, "member_passwd").send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div[7]/div/div/form/div/div/fieldset/a").click()
    
    # 로그인 성공 확인 (필요시 수정)
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "log"))
    # )
    time.sleep(0.25)
    print('로그인')

# 카테고리 페이지 크롤링 함수
def crawl_category(url):
    driver.get(url)
    products = []
    
    # try:
    #     max_page = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[10]/td/a[11]").text
    #     max_page =int(max_page.replace('[','').replace(']',''))
    # except:
    #     max_page = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/table/tbody/tr[10]/td")
    #     max_page = max_page.find_elements(By.XPATH, ".//*")
    #     max_page = len(max_page)
    max_page = 33
    print(max_page)

    time.sleep(0.25)
    for page in range(max_page):
        page_url = f"{url}&page={page+1}"
        driver.get(page_url)
        cate_link = []
        # 상품 목록 가져오기
        elements = driver.find_elements(By.CSS_SELECTOR, "ul.prdList.grid4 li div.description div.name a span:nth-child(2)")

        # 텍스트 추출
        for element in elements:
            print(element.text)
            time.sleep(0.5)
            data = {'상품명':element.text}
            products.append(data)
        # product_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div/div[4]/ul/li')
        # time.sleep(0.25)
        # for element in (product_elements):
        #     print(page)
        #     product_url = element.find_element(By.XPATH, f'/html/body/div[2]/div[2]/div/div[4]/ul/li[{i}]/div/div[2]/div[1]/a/span[2]').get_attribute("href")
        #     # print(product_url)
        #     cate_link.append(product_url)
        #     time.sleep(0.25)
        # for links in cate_link:
        #     products.append(crawl_product(links))
        #     print(f'끝 {links}')
        #     time.sleep(0.25)
            
            
    
    return products

# 개별 상품 크롤링 함수
def crawl_product(url):
    driver.get(url)
    print(f'시작 {url}')
    
    
    title = driver.find_element(By.CSS_SELECTOR, "#wrap > div > div.inner > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.infoArea > div.xans-element-.xans-product.xans-product-detaildesign > div > div > h2").text
    # code = re.findall(r'\[(.*?)\]', titles)
    # if code:
    #     code = code[0]  # 첫 번째 요소를 문자열로 변환
    # else:
    #     code = ""
    # title = re.sub(r'\[.*?\]', '', titles).strip()
    # print(code)
    title=title.replace('제트비 ','')
    print(title)
    price = driver.find_element(By.CSS_SELECTOR, "#span_product_price_text").text.replace(',', '').replace('원', '')
    print(price)
    price2 = int(price)*1.8
    # try:
    #     price2 = int(price)*1.8
    # except:
    #     price = 4500
    #     price2 = int(price)*1.8
    img_url = driver.find_element(By.CSS_SELECTOR, "#wrap > div > div.inner > div.xans-element-.xans-product.xans-product-detail > div.detailArea > div.xans-element-.xans-product.xans-product-image.imgArea > div.keyImg > a > img").get_attribute("src")
    print(img_url)
    # 원하는 순번 (0부터 시작하는 인덱스 기준) - 제외할 인덱스 목록
    exclude_indexes = {0, 2}  # 예제: 2번째(1)와 4번째(3) 태그를 제외하고 싶다면 {1, 3}

    # 상세 설명 (HTML 형식)
    center_element = driver.find_element(By.CSS_SELECTOR, "#prdDetail > div > center")
    img_elements = center_element.find_elements(By.TAG_NAME, "img")
    detail_description = "".join(
        img.get_attribute("outerHTML") for i, img in enumerate(img_elements) if i not in exclude_indexes
    )
    print(detail_description)
    # 옵션 (있을 경우)
    options = []
    try:
        # <select> 태그 찾기
        select_element = driver.find_element(By.NAME, 'option1')

        # 모든 <option> 태그 가져오기
        option_elements = select_element.find_elements(By.TAG_NAME, 'option')

        # 첫 번째 <option>은 생략하고, '품절'이라는 단어가 들어간 <option>도 제외
        for option in option_elements[2:]:  # 첫 번째 <option>은 생략
            value = option.text
            options.append(value)

    except:
        options.append(title)
    print(options)
    ops = "{" + "|".join(options) + "}"
    print(ops)
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
        '이미지등록(상세)':img_url,
        '이미지등록(목록)':img_url,
        '이미지등록(작은목록)':img_url,
        '이미지등록(축소)':img_url,
        '이미지등록(추가)':'','제조사':'','공급사':'','브랜드':'','트렌드':'','자체분류 코드':'','제조일자':'','출시일자':'',
        '유효기간 사용여부':'','유효기간':'','원산지':'','상품부피(cm)':'','상품결제안내':'','상품배송안내':'','교환/반품안내':'',
        '서비스문의/안내':'','배송정보':'','배송방법':'','국내/해외배송':'','배송지역':'','배송비 선결제 설정':'','배송기간':'',
        '배송비 구분':'','배송비입력':'','스토어픽업 설정':'','상품 전체중량(kg)':'','HS코드':'','상품 구분(해외통관)':'','상품소재':'',
        '영문 상품소재(해외통관)':'','옷감(해외통관)':'','검색엔진최적화(SEO) 검색엔진 노출 설정':'','검색엔진최적화(SEO) Title':'',
        '검색엔진최적화(SEO) Author':'','검색엔진최적화(SEO) Description':'','검색엔진최적화(SEO) Keywords':'',
        '검색엔진최적화(SEO) 상품 이미지 Alt 텍스트':'','개별결제수단설정':'','상품배송유형 코드':'','메모':''
        # 필요한 다른 필드들 추가
    }

# CSV 저장 함수
def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=products[0].keys())
        writer.writeheader()
        for product in products:
            writer.writerow(product)

# 메인 실행 함수
def main():
    username = ""
    password = "!"
    
    category_url = "https://partsmatch.agency/product/search.html?banner_action=&keyword=%EB%B8%8C%EB%A0%88%EC%9D%B4%ED%81%AC%EC%95%A1+PFB401+DOT4+1L"
    # cate_list = ['033021']
    cate_name = ['브레이크액']
    mall='파츠매치'
    # login(username, password)
    products = crawl_category(category_url)
    save_to_csv(products, f"아임웹_{mall}{cate_name[0]}.csv")
    # for i in range(len(cate_list)):
    #     if i == 0:
    #         login(username, password)
    #     products = crawl_category(category_url+cate_list[i])
    #     save_to_csv(products, f"아임웹_카포카{cate_name[i]}.csv")
    
    # driver.quit()

if __name__ == "__main__":
    main()