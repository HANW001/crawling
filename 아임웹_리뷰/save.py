import csv

def save_to_file(name,jobs):
  print("저장한다")
  file = open("{}.csv".format(name),mode="w",encoding = 'utf-8-sig')
  writer = csv.writer(file)
  # writer.writerow(["title","thum_img","detail_img_1","detail_img_2","detail_img_3","price"])

  writer.writerow(['키워드','클릭수','마지막클릭날짜'])

  
  # print(len(jobs))
  # print(jobs[10])
  # print(jobs[11])
  cnt = 0
  for job in jobs:
    print(cnt)
    try:
      writer.writerow(list(job.values()))
    except:
      pass
    cnt+=1
    # print(list(job.values()))
  print('끝')
  # print(jobs)
  # return

def save_to_ssfile(ss):
  print("저장한다")
  file = open("스스_리뷰.csv",mode="w",encoding = 'utf-8-sig')
  writer = csv.writer(file)
  # writer.writerow(["title","thum_img","detail_img_1","detail_img_2","detail_img_3","price"])

  writer.writerow(['번호','리뷰','주소'])

  
  # print(len(jobs))
  # print(jobs[10])
  # print(jobs[11])
  cnt = 0
  for s in ss:
    print(cnt)
    writer.writerow(list(s.values()))
    cnt+=1
    # print(list(job.values()))
  print('끝')
  # print(jobs)
  # return

def save_to_carpaint(ss,names):
  print("저장한다")
  file = open(f"카페인트_{names}.csv",mode="w",encoding = 'utf-8')
  writer = csv.writer(file)
  # writer.writerow(["title","thum_img","detail_img_1","detail_img_2","detail_img_3","price"])

  writer.writerow(['구분','제조사','적용차종','차량년식','색상코드1','제품번호1','색상명1','스프레이용1','붓펜용1','펄1','색상코드2','제품번호2','색상명2','스프레이용2','붓펜용2','펄2','색상코드3','제품번호3','색상명3','스프레이용3','붓펜용3','펄3'])

  cnt = 0
  for s in ss:
    # print(cnt)
    writer.writerow(list(s.values()))
    # cnt+=1
    # print(list(job.values()))
  print('끝')
  # print(jobs)
  # return